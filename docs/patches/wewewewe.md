좋아, 이제 **stage dict 예시 + for 루프 전체 샘플**을 한 번에 쓸 수 있게 묶어줄게.
아래 코드만 `agi_tr.py` 맨 아래나, 별도 테스트 파일에 넣고 돌리면 된다.

> 전제:
>
> * 앞에서 이미 구현한 함수/타입이 같은 파일 안에 있다고 가정
>   (`calc_draft_with_lcf`, `get_gm_bilinear`, `heel_and_gm_check`, `apply_dynamic_loads`, `LoadCase`, `GMGrid`)

---

```python
from typing import Any, Dict, List

# -------------------------------------------------
# 0) 타입 alias (이미 있으면 중복 정의 X)
# -------------------------------------------------
StageDict = Dict[str, Any]

# -------------------------------------------------
# 1) GMGrid 예시 (실전에서는 Aries/BV GM 테이블 로드)
#    Δ–Trim–GM (m) 테이블
# -------------------------------------------------
gm_grid: GMGrid = {
    # Δ = 1227.59 t 일 때 Trim–GM
    1227.59: {
        0.00: 1.60,
        0.50: 1.58,
        1.00: 1.55,
    },
    # Δ = 1658.71 t 일 때 Trim–GM
    1658.71: {
        0.00: 1.55,
        0.50: 1.53,
        1.00: 1.50,
    },
}

LCF_M = 30.91   # m (FP 기준 LCF)
LBP_M = 60.302  # m (LBP)


# -------------------------------------------------
# 2) Stage 입력 예시 (엑셀 Row → dict 로 나왔다고 가정)
#    - 실제로는 CSV/엑셀에서 읽어서 채우면 됨
# -------------------------------------------------
stages: List[StageDict] = [
    {
        "name": "Stage 5A-2",
        "Tmean_m": 2.85,
        "Trim_cm": -96.50,          # 선수침(-), 선미침(+)
        "Disp_t": 1658.71,          # Δ
        "W_stage_t": 217.00,        # 해당 Stage 주요 카고/편심 하중
        "Y_offset_m": 2.50,         # 중심선 기준 횡 편심 (SPMT 등)
        "FSE_t_m": 85.00,           # Free Surface Moment (t·m)
        "Share_Load_t": 210.00,     # Ramp share load (정적)
        "Pin_Stress_MPa": 120.00,   # Pin stress (정적)
        "LoadCase": "B",            # A=STATIC, B=DYNAMIC, C=BRAKING
    },
    {
        "name": "Stage 6B",
        "Tmean_m": 3.10,
        "Trim_cm": -120.00,
        "Disp_t": 1227.59,
        "W_stage_t": 434.00,
        "Y_offset_m": 1.50,
        "FSE_t_m": 40.00,
        "Share_Load_t": 250.00,
        "Pin_Stress_MPa": 135.00,
        "LoadCase": "C",
    },
]


# -------------------------------------------------
# 3) Stage 루프 – 4개 모듈 한 번에 물리기
# -------------------------------------------------
def evaluate_stages(
    stages: List[StageDict],
    gm_grid: GMGrid,
    lcf_m: float = LCF_M,
    lbp_m: float = LBP_M,
) -> List[StageDict]:
    """
    각 Stage에 대해:
      - Dfwd_precise_m / Daft_precise_m (LCF 기반 Draft)
      - GM_calc_m (Δ–Trim 2D 보간)
      - Heel_deg / GM_eff_m / Heel_OK / GM_OK
      - Share_Load_dyn_t / Pin_Stress_dyn_MPa
    필드를 추가해서 반환.
    """

    result: List[StageDict] = []

    for stage in stages:
        # ---- 1) LCF 기반 정밀 Draft ----
        tmean_m = float(stage.get("Tmean_m", 0.0))
        trim_cm = float(stage.get("Trim_cm", 0.0))

        dfwd_m, daft_m = calc_draft_with_lcf(
            tmean_m=tmean_m,
            trim_cm=trim_cm,
            lcf_m=lcf_m,
            lbp_m=lbp_m,
        )
        stage["Dfwd_precise_m"] = round(dfwd_m, 3)
        stage["Daft_precise_m"] = round(daft_m, 3)

        # ---- 2) Δ–Trim 2D GM 보간 ----
        disp_t = float(stage.get("Disp_t", 0.0))
        trim_m = trim_cm / 100.0

        gm_m = get_gm_bilinear(
            disp_t=disp_t,
            trim_m=trim_m,
            gm_grid=gm_grid,
        )
        stage["GM_calc_m"] = round(gm_m, 3)

        # ---- 3) Heel + FSE 반영 GM_eff ----
        weight_t = float(stage.get("W_stage_t", 0.0))
        y_offset_m = float(stage.get("Y_offset_m", 0.0))
        fse_t_m = float(stage.get("FSE_t_m", 0.0))

        heel_deg, gm_eff, heel_ok, gm_ok = heel_and_gm_check(
            weight_t=weight_t,
            y_offset_m=y_offset_m,
            disp_t=disp_t,
            gm_m=gm_m,
            fse_t_m=fse_t_m,
            heel_limit_deg=3.0,
            gm_min_m=1.50,
        )
        stage["Heel_deg"] = round(heel_deg, 3)
        stage["GM_eff_m"] = round(gm_eff, 3)
        stage["Heel_OK"] = heel_ok
        stage["GM_OK"] = gm_ok

        # ---- 4) 동적 / 제동 Load Case ----
        share_static = float(stage.get("Share_Load_t", 0.0))
        pin_static = float(stage.get("Pin_Stress_MPa", 0.0))

        # LoadCase 문자열 → Enum 매핑
        lc_raw = str(stage.get("LoadCase", "A")).upper()
        if lc_raw in ("A", "STATIC"):
            lc = LoadCase.STATIC
        elif lc_raw in ("B", "DYNAMIC"):
            lc = LoadCase.DYNAMIC
        elif lc_raw in ("C", "BRAKE", "BRAKING"):
            lc = LoadCase.BRAKING
        else:
            lc = LoadCase.STATIC

        share_dyn, pin_dyn = apply_dynamic_loads(
            share_load_t=share_static,
            pin_stress_mpa=pin_static,
            load_case=lc,
        )
        stage["Share_Load_dyn_t"] = round(share_dyn, 2)
        stage["Pin_Stress_dyn_MPa"] = round(pin_dyn, 2)
        stage["LoadCase_used"] = lc.name  # "STATIC" / "DYNAMIC" / "BRAKING"

        result.append(stage)

    return result


# -------------------------------------------------
# 4) 데모 실행 (직접 터미널에서 확인용)
# -------------------------------------------------
if __name__ == "__main__":
    enriched_stages = evaluate_stages(stages, gm_grid)

    from pprint import pprint
    print("\n=== Stage 계산 결과 요약 ===")
    for s in enriched_stages:
        print(f"\n[{s['name']}]")
        pprint(
            {
                "Dfwd_precise_m": s["Dfwd_precise_m"],
                "Daft_precise_m": s["Daft_precise_m"],
                "GM_calc_m": s["GM_calc_m"],
                "GM_eff_m": s["GM_eff_m"],
                "Heel_deg": s["Heel_deg"],
                "Heel_OK": s["Heel_OK"],
                "GM_OK": s["GM_OK"],
                "Share_Load_dyn_t": s["Share_Load_dyn_t"],
                "Pin_Stress_dyn_MPa": s["Pin_Stress_dyn_MPa"],
                "LoadCase_used": s["LoadCase_used"],
            }
        )
```

---

### 어떻게 쓰면 되냐면

1. 위 블록을 **그대로** `agi tr.py`에 붙이고
2. 이미 있는 함수 이름/타입이랑 충돌 안 하면 OK,
3. `python "agi tr.py"` 실행하면 마지막 `__main__` 데모가 **Stage별 정밀 Dfwd/Daft, GM, Heel, 동적 Load**를 콘솔에 뿌려줄 거야.

엑셀/CSV 연동까지 붙이고 싶으면, 지금 `stages` 리스트 대신
엑셀에서 읽은 Row들을 dict로 만들어서 `evaluate_stages()`에 넣으면 바로 현장용 루틴으로 쓸 수 있어.
