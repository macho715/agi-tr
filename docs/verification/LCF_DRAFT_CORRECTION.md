1) LCF 기반 정밀 Draft 보정 모듈
def calc_draft_with_lcf(tmean_m: float,
                        trim_cm: float,
                        lcf_m: float,
                        lbp_m: float) -> tuple[float, float]:
    """
    LCF 기반 정밀 Dfwd/Daft 계산.

    Parameters
    ----------
    tmean_m : 평균 흘수 (m)
    trim_cm : Trim (cm)  # 가정: +면 선미침(AFT deeper), -면 선수침(FWD deeper)
    lcf_m   : LCF (m), F.P. 기준 길이
    lbp_m   : LBP (m)

    Returns
    -------
    (Dfwd_m, Daft_m) : 선수/선미 흘수 (m)

    공식 (선급/교재 표준형)
    ----------------------
    Trim_m = trim_cm / 100
    Dfwd   = Tmean - Trim_m * (1 - LCF/LBP)
    Daft   = Tmean + Trim_m * (LCF/LBP)
    """
    trim_m = trim_cm / 100.0

    if lbp_m <= 0:
        raise ValueError("LBP must be > 0")

    r = lcf_m / lbp_m  # 무차원 비율 (0~1 근처)

    dfwd_m = tmean_m - trim_m * (1.0 - r)
    daft_m = tmean_m + trim_m * r

    return dfwd_m, daft_m


엑셀에서는 Dfwd_precise, Daft_precise 열에서 이 함수 래핑해서 쓰면 됨 (python → 엑셀 UDF or 사전계산 CSV).

2) GM 2D 보간 (Δ × Trim) – Bilinear Interpolation
from bisect import bisect_left
from typing import Dict

GMGrid = Dict[float, Dict[float, float]]
# 예시:
# gm_grid = {
#   1200.0: {0.0: 1.55, 0.5: 1.53, 1.0: 1.50},
#   1400.0: {0.0: 1.60, 0.5: 1.58, 1.0: 1.55},
# }


def _nearest_two(sorted_vals: list[float], target: float) -> tuple[float, float]:
    """target을 기준으로 아래/위 2개 값을 리턴 (경계면에서는 동일값 반환)."""
    if not sorted_vals:
        raise ValueError("empty axis")

    if target <= sorted_vals[0]:
        return sorted_vals[0], sorted_vals[0]
    if target >= sorted_vals[-1]:
        return sorted_vals[-1], sorted_vals[-1]

    idx = bisect_left(sorted_vals, target)
    low = sorted_vals[idx - 1]
    high = sorted_vals[idx]
    return low, high


def get_gm_bilinear(disp_t: float,
                    trim_m: float,
                    gm_grid: GMGrid) -> float:
    """
    Δ(ton), Trim(m)에 대해 GM(m) 2D 보간 (bilinear).

    gm_grid 형식:
        {disp: {trim: GM, ...}, ...}
    """
    if not gm_grid:
        raise ValueError("gm_grid is empty")

    disp_axis = sorted(gm_grid.keys())
    disp1, disp2 = _nearest_two(disp_axis, disp_t)

    trim_axis = sorted(next(iter(gm_grid.values())).keys())
    trim1, trim2 = _nearest_two(trim_axis, trim_m)

    # 경계선(한 방향 값만 존재)에서는 단순 선형 보간/직접 값 사용
    def gm_at(d: float, tr: float) -> float:
        return gm_grid[d][tr]

    # 네 모서리 값
    q11 = gm_at(disp1, trim1)
    q21 = gm_at(disp2, trim1)
    q12 = gm_at(disp1, trim2)
    q22 = gm_at(disp2, trim2)

    # 축이 collapse 된 경우 처리
    if disp1 == disp2 and trim1 == trim2:
        return q11
    if disp1 == disp2:  # Trim 방향만 보간
        t = (trim_m - trim1) / (trim2 - trim1) if trim2 != trim1 else 0.0
        return q11 + t * (q12 - q11)
    if trim1 == trim2:  # Δ 방향만 보간
        t = (disp_t - disp1) / (disp2 - disp1) if disp2 != disp1 else 0.0
        return q11 + t * (q21 - q11)

    # Bilinear interpolation
    # 참조: 표준 bilinear 공식
    xd = (disp_t - disp1) / (disp2 - disp1)
    yd = (trim_m - trim1) / (trim2 - trim1)

    gm_interp = (
        q11 * (1 - xd) * (1 - yd)
        + q21 * xd * (1 - yd)
        + q12 * (1 - xd) * yd
        + q22 * xd * yd
    )
    return gm_interp


Aries Stability Booklet 표를 gm_grid로 만들어두고, Stage별 GM_calc_m = get_gm_bilinear(Δ, Trim, gm_grid) 형태로 쓰면 됨.

3) Ramp / Pin 동적 Load Case 확장
from enum import Enum, auto

class LoadCase(Enum):
    STATIC = auto()   # A: 정적
    DYNAMIC = auto()  # B: 동적계수만
    BRAKE = auto()    # C: 동적 + 제동/수평력


def apply_dynamic_loads(share_load_static_t: float,
                        pin_stress_static_mpa: float,
                        dyn_factor: float = 1.10,
                        brake_factor: float = 1.30,
                        horiz_factor: float = 0.20,
                        load_case: LoadCase = LoadCase.STATIC
                        ) -> dict:
    """
    Ramp/Pin 동적 Load Case 적용.

    Parameters
    ----------
    share_load_static_t      : Ramp에 작용하는 정적 분담하중 (t)
    pin_stress_static_mpa    : 핀 정적 응력 (MPa)
    dyn_factor               : 동적 계수 (예: 1.10)
    brake_factor             : 제동/충격 계수 (예: 1.30)
    horiz_factor             : 수평력 비율 (수직 하중 대비, 예: 0.20)
    load_case                : STATIC / DYNAMIC / BRAKE

    Returns
    -------
    dict with:
        'share_load_t'
        'pin_stress_mpa'
        'horiz_load_t'
    """

    if load_case == LoadCase.STATIC:
        share = share_load_static_t
        stress = pin_stress_static_mpa
    elif load_case == LoadCase.DYNAMIC:
        share = share_load_static_t * dyn_factor
        stress = pin_stress_static_mpa * dyn_factor
    elif load_case == LoadCase.BRAKE:
        factor = dyn_factor * brake_factor
        share = share_load_static_t * factor
        stress = pin_stress_static_mpa * factor
    else:
        raise ValueError(f"Unknown load_case: {load_case}")

    horiz_load_t = share * horiz_factor

    return {
        "share_load_t": share,
        "pin_stress_mpa": stress,
        "horiz_load_t": horiz_load_t,
    }


Stage 시트에 LoadCase 열(A/B/C) 만들어서, Python 쪽에서 enum 매핑 후 동적하중 계산 → 허용값과 비교만 하면 됨.

4) Heel + FSE 기반 GM_eff 계산
import math

def calc_heel_from_offset(weight_t: float,
                          y_offset_m: float,
                          disp_t: float,
                          gm_m: float) -> float:
    """
    횡 방향 편심 하중에 의한 Heel 각도 (deg) 계산.
    Small-angle 가정: tan(φ) ≈ φ(rad)

    Parameters
    ----------
    weight_t   : 편심 하중 (t)
    y_offset_m : 중심선 기준 횡방향 거리 (m)
    disp_t     : 총 배수중량 Δ (t)
    gm_m       : GM (m)

    Returns
    -------
    heel_deg   : Heel 각도 (deg)
    """
    if disp_t <= 0 or gm_m <= 0:
        return 0.0

    phi_rad = (weight_t * y_offset_m) / (disp_t * gm_m)
    heel_deg = math.degrees(phi_rad)
    return heel_deg


def calc_gm_effective(gm_m: float,
                      fse_t_m: float,
                      disp_t: float) -> float:
    """
    Free Surface Effect(FSE) 반영한 유효 GM 계산.

    GM_eff = GM - FSE / Δ

    Parameters
    ----------
    gm_m    : 원래 GM (m)
    fse_t_m : FSE (t·m)  # 탱크별 FSE 합
    disp_t  : 배수중량 Δ (t)
    """
    if disp_t <= 0:
        raise ValueError("disp_t must be > 0")

    return gm_m - (fse_t_m / disp_t)


def heel_and_gm_check(weight_t: float,
                      y_offset_m: float,
                      gm_m: float,
                      fse_t_m: float,
                      disp_t: float,
                      heel_limit_deg: float = 3.0,
                      gm_min_m: float = 1.50) -> dict:
    """
    Heel + FSE 반영한 Stage 안전성 간단 체크.

    Returns
    -------
    dict with:
        'heel_deg'
        'gm_eff_m'
        'heel_ok'  (bool)
        'gm_ok'    (bool)
    """
    heel_deg = calc_heel_from_offset(weight_t, y_offset_m, disp_t, gm_m)
    gm_eff = calc_gm_effective(gm_m, fse_t_m, disp_t)

    return {
        "heel_deg": heel_deg,
        "gm_eff_m": gm_eff,
        "heel_ok": abs(heel_deg) <= heel_limit_deg,
        "gm_ok": gm_eff >= gm_min_m,
    }


Stage별로 weight_t=y_TR, y_offset_m(SPMT 편심), FSE는 탱크별 사전계산 합산해서 넣으면, Heel_deg/GM_eff/OK 여부를 바로 뽑을 수 있음.
