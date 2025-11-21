좋아, 이제 “이 파일을 어떻게 패치했는지”를 **깔끔한 원본 vs 패치 diff**로 정리해볼게.
실제 `agi tr.py` 전체 diff 가 아니라, **핵심 블록(5군데)** 기준으로 “앞으로도 재적용할 수 있는 패턴”으로 보는 거라고 생각하면 된다.

---

## 0. 전체 구조 개요

`agi tr.py` 기준으로 이번 패치는 크게 5블록이야:

1. **import 블록 확장** (bisect, typing, math, enum)
2. **Hydro/Trim 유틸**

   * `calc_draft_with_lcf` (LCF 기반 정밀 Draft)
   * `get_gm_bilinear` (Δ–Trim 2D GM 보간)
3. **Heel / FSE + 동적 LoadCase 블록**

   * `calc_heel_from_offset`, `calc_gm_effective`, `heel_and_gm_check`
   * `LoadCase`, `apply_dynamic_loads`
4. **Frame ↔ x_from_mid_m 변환 유틸** (`_FRAME_SLOPE`, `_FRAME_OFFSET`, `fr_to_x`, `x_to_fr`)
5. **RORO 시트 엑셀 수식 패치**

   * `AQ = Heel_deg`, `AR = GM_eff_m`
   * CAPTAIN_REPORT 시트에서 이 값 링크

아래는 각 블록별로 **“원본(깨끗한 버전)” + “패치 diff”**를 보여줄게.

---

## 1. import 블록 diff

### 1-1. 깨끗한 원본 (예시)

```python
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment, PatternFill, Border, Side, Protection
from openpyxl.utils import get_column_letter
import os
import sys
import json
from datetime import datetime
import numpy as np
from scipy.interpolate import RectBivariateSpline
```

### 1-2. 패치 버전 diff

```diff
 from openpyxl.utils import get_column_letter
 import os
 import sys
 import json
 from datetime import datetime
 import numpy as np
-from scipy.interpolate import RectBivariateSpline
+from scipy.interpolate import RectBivariateSpline
+from bisect import bisect_left
+from typing import Dict
+import math
+from enum import Enum, auto
```

> **기억 포인트:**
>
> * 앞으로 다른 스크립트에 옮길 때도, **위 4개 import**를 같은 위치에 꽂으면 된다.

---

## 2. Hydro/Trim 유틸 블록 diff

(LCF 기반 Draft + GM 2D 보간)

### 2-1. 깨끗한 원본 (Trim 단순 버전 예시)

```python
def calc_drafts_simple(tmean_m: float, trim_cm: float) -> tuple[float, float]:
    """LCF=Midship 가정한 단순 Draft 계산"""
    trim_m = trim_cm / 100.0
    dfwd = tmean_m - trim_m / 2.0
    daft = tmean_m + trim_m / 2.0
    return dfwd, daft

# GM은 1D 테이블에서 Δ만 보고 보간하는 구조(예시)
def get_gm_1d(disp_t: float, gm_table: dict[float, float]) -> float:
    ...
```

### 2-2. 패치 버전 diff (LCF + 2D GM)

```diff
-# GM은 1D 테이블에서 Δ만 보고 보간하는 구조(예시)
-def get_gm_1d(disp_t: float, gm_table: dict[float, float]) -> float:
-    ...
+def calc_draft_with_lcf(
+    tmean_m: float, trim_cm: float, lcf_m: float, lbp_m: float
+) -> tuple[float, float]:
+    """
+    LCF 기반 정밀 Dfwd/Daft 계산.
+    Trim_cm > 0 : 선미침(AFT deeper), < 0 : 선수침(FWD deeper)
+    """
+    if lbp_m <= 0:
+        raise ValueError("LBP must be positive")
+
+    trim_m = trim_cm / 100.0
+    r = lcf_m / lbp_m
+
+    d_fwd = tmean_m - trim_m * (1.0 - r)
+    d_aft = tmean_m + trim_m * r
+    return d_fwd, d_aft
+
+
+def _nearest_two(sorted_vals: list[float], target: float) -> tuple[float, float]:
+    """target 기준 아래/위 두 값 반환."""
+    if not sorted_vals:
+        raise ValueError("Axis is empty")
+    if target <= sorted_vals[0]:
+        return sorted_vals[0], sorted_vals[0]
+    if target >= sorted_vals[-1]:
+        return sorted_vals[-1], sorted_vals[-1]
+    idx = bisect_left(sorted_vals, target)
+    return sorted_vals[idx - 1], sorted_vals[idx]
+
+
+def get_gm_bilinear(
+    disp_t: float,
+    trim_m: float,
+    gm_grid: Dict[float, Dict[float, float]],
+) -> float:
+    """
+    Δ(ton), Trim(m)에 대해 GM(m) 2D 보간 (bilinear).
+    gm_grid 형식: {disp: {trim: GM, ...}, ...}
+    """
+    if not gm_grid:
+        raise ValueError("gm_grid is empty")
+
+    disp_axis = sorted(gm_grid.keys())
+    disp1, disp2 = _nearest_two(disp_axis, disp_t)
+
+    trim_axis = sorted(next(iter(gm_grid.values())).keys())
+    trim1, trim2 = _nearest_two(trim_axis, trim_m)
+
+    def gm_at(d: float, tr: float) -> float:
+        return gm_grid[d][tr]
+
+    q11 = gm_at(disp1, trim1)
+    q21 = gm_at(disp2, trim1)
+    q12 = gm_at(disp1, trim2)
+    q22 = gm_at(disp2, trim2)
+
+    if disp1 == disp2 and trim1 == trim2:
+        return q11
+    if disp1 == disp2:
+        # Trim만 보간
+        t = (trim_m - trim1) / (trim2 - trim1) if trim2 != trim1 else 0.0
+        return q11 + t * (q12 - q11)
+    if trim1 == trim2:
+        # Δ만 보간
+        t = (disp_t - disp1) / (disp2 - disp1) if disp2 != disp1 else 0.0
+        return q11 + t * (q21 - q11)
+
+    xd = (disp_t - disp1) / (disp2 - disp1)
+    yd = (trim_m - trim1) / (trim2 - trim1)
+
+    return (
+        q11 * (1 - xd) * (1 - yd)
+        + q21 * xd * (1 - yd)
+        + q12 * (1 - xd) * yd
+        + q22 * xd * yd
+    )
```

> **역할 정리:**
>
> * `calc_draft_with_lcf` → **Stage별 정밀 Dfwd/Daft**
> * `get_gm_bilinear` → Aries/BV GM 테이블 기반 **2D GM 계산**

---

## 3. Heel / FSE + 동적 LoadCase diff

### 3-1. 깨끗한 원본 (Heel/FSE, LoadCase 없음 예시)

```python
# 기존에는 GM만 계산하고 Heel 또는 FSE는 고려 안 함
# Ramp/Pin도 정적 하중만 계산

def calc_gm(...):
    ...

# Ramp_share_t, Pin_stress_mpa만 Stage 표에 기록
```

### 3-2. 패치 버전 diff

```diff
+def calc_heel_from_offset(
+    weight_t: float,
+    y_offset_m: float,
+    disp_t: float,
+    gm_m: float,
+) -> float:
+    """
+    횡 방향 편심 하중에 의한 Heel 각도 (deg).
+    tan(phi) ≈ phi(rad) ≈ (w * y) / (Δ * GM)
+    """
+    if disp_t <= 0 or gm_m <= 0:
+        return 0.0
+    phi_rad = (weight_t * y_offset_m) / (disp_t * gm_m)
+    heel_deg = math.degrees(phi_rad)
+    return heel_deg
+
+
+def calc_gm_effective(gm_m: float, fse_t_m: float, disp_t: float) -> float:
+    """
+    Free Surface Effect(FSE) 반영한 유효 GM 계산.
+    GM_eff = GM - FSE / Δ
+    """
+    if disp_t <= 0:
+        return gm_m
+    return gm_m - fse_t_m / disp_t
+
+
+def heel_and_gm_check(
+    weight_t: float,
+    y_offset_m: float,
+    gm_m: float,
+    fse_t_m: float,
+    disp_t: float,
+    heel_limit_deg: float = 3.0,
+    gm_min_m: float = 1.50,
+) -> dict:
+    """
+    Heel + FSE 반영한 Stage 안전성 간단 체크.
+    """
+    heel_deg = calc_heel_from_offset(weight_t, y_offset_m, disp_t, gm_m)
+    gm_eff = calc_gm_effective(gm_m, fse_t_m, disp_t)
+
+    return {
+        "heel_deg": heel_deg,
+        "gm_eff_m": gm_eff,
+        "heel_ok": abs(heel_deg) <= heel_limit_deg,
+        "gm_ok": gm_eff >= gm_min_m,
+    }
+
+
+class LoadCase(Enum):
+    STATIC = auto()   # 정적
+    DYNAMIC = auto()  # 동적계수만
+    BRAKE = auto()    # 동적 + 제동/충격
+
+
+def apply_dynamic_loads(
+    share_load_static_t: float,
+    pin_stress_static_mpa: float,
+    dyn_factor: float = 1.10,
+    brake_factor: float = 1.00,
+    load_case: LoadCase = LoadCase.STATIC,
+) -> dict:
+    """
+    LoadCase 별로 share load / pin stress를 조정하여 반환.
+    """
+    if load_case == LoadCase.STATIC:
+        factor = 1.0
+    elif load_case == LoadCase.DYNAMIC:
+        factor = dyn_factor
+    elif load_case == LoadCase.BRAKE:
+        factor = dyn_factor * brake_factor
+    else:
+        factor = 1.0
+
+    return {
+        "share_load_t": share_load_static_t * factor,
+        "pin_stress_mpa": pin_stress_static_mpa * factor,
+    }
```

> **역할 정리:**
>
> * `heel_and_gm_check` → **Heel_deg + GM_eff + OK/CHECK 플래그**
> * `LoadCase` + `apply_dynamic_loads` → 같은 Stage라도 **STATIC / DYNAMIC / BRAKE** 케이스별 Ramp/Pin 하중 비교 가능.

---

## 4. Frame ↔ x_from_mid_m 매핑 diff

### 4-1. 깨끗한 원본 (Frame 고정 좌표만 직접 입력 예시)

```python
# Stage 기본 좌표를 그냥 숫자로 박아둔 버전
STAGE_DEFAULTS = {
    "Stage 5": {"x_from_mid_m": 52.48},
    "Stage 7": {"x_from_mid_m": 0.00},
}
```

### 4-2. 패치 버전 diff

```diff
-# Stage 기본 좌표를 그냥 숫자로 박아둔 버전
-STAGE_DEFAULTS = {
-    "Stage 5": {"x_from_mid_m": 52.48},
-    "Stage 7": {"x_from_mid_m": 0.00},
-}
+_FRAME_SLOPE = 1.0      # x 증가량 / Frame 증가량
+_FRAME_OFFSET = -30.15  # x = _FRAME_OFFSET + _FRAME_SLOPE * Fr
+
+
+def _init_frame_mapping():
+    """
+    Frame_x_from_mid_m.json 있으면 slope/offset 자동 추정.
+    없으면 기본값(-30.15 + Fr) 유지.
+    """
+    global _FRAME_SLOPE, _FRAME_OFFSET
+    data = _load_json("data/Frame_x_from_mid_m.json")
+    if not data or not isinstance(data, list) or len(data) < 2:
+        return
+    # 최소제곱 직선 피팅 (Fr → x)
+    frs = np.array([row["Fr"] for row in data], dtype=float)
+    xs = np.array([row["x_from_mid_m"] for row in data], dtype=float)
+    A = np.vstack([frs, np.ones_like(frs)]).T
+    slope, offset = np.linalg.lstsq(A, xs, rcond=None)[0]
+    _FRAME_SLOPE = float(slope)
+    _FRAME_OFFSET = float(offset)
+
+
+def fr_to_x(fr: float) -> float:
+    """Frame → x_from_mid_m 변환"""
+    return _FRAME_OFFSET + _FRAME_SLOPE * float(fr)
+
+
+def x_to_fr(x: float) -> float:
+    """x_from_mid_m → Frame 변환"""
+    return (float(x) - _FRAME_OFFSET) / _FRAME_SLOPE
+
+
+_init_frame_mapping()
+
+STAGE_DEFAULTS = {
+    "Stage 5": {"x_from_mid_m": fr_to_x(52.5)},
+    "Stage 7": {"x_from_mid_m": fr_to_x(30.15)},  # 예: midship
+}
```

> **역할 정리:**
>
> * 앞으로 Frame 테이블이 바뀌어도 **JSON만 교체하면 전체 x좌표 자동 재계산**.

---

## 5. RORO 시트 엑셀 수식 패치 diff (AQ/AR + CAPTAIN_REPORT)

### 5-1. 깨끗한 원본 (AQ/AR 미사용)

```python
# RORO_Stage_Scenarios 헤더 생성까지 있고,
# 데이터 열은 AP(40) 정도까지로 끝났던 상태 (예시)
```

### 5-2. 패치 버전 diff (AQ: Heel_deg / AR: GM_eff_m)

```diff
-    # 기존: AP(40)까지 열 생성
+    # ... 기존 열 생성 (AP까지) ...
+
+    # AQ (43): Heel_deg
+    ws.cell(row=row, column=43).value = (
+        f'=IF(OR($A{row_str}="", T{row_str}="", T{row_str}=0, J{row_str}="", J{row_str}=0), "", '
+        f"DEGREES((B{row_str} * Calc!$E$43) / (J{row_str} * T{row_str})))"
+    )
+    ws.cell(row=row, column=43).number_format = "0.00"
+
+    # AR (44): GM_eff_m
+    fse_value = 0  # 현재는 0, 향후 탱크별 FSE로 확장 가능
+    ws.cell(row=row, column=44).value = (
+        f'=IF(OR($A{row_str}="", T{row_str}="", J{row_str}="", J{row_str}=0), "", '
+        f"T{row_str} - {fse_value} / J{row_str})"
+    )
+    ws.cell(row=row, column=44).number_format = "0.00"
```

### 5-3. CAPTAIN_REPORT 시트 링크 diff

```diff
-    # ... 기존 CAPTAIN_REPORT 열 (예: Draft, Trim, GM) ...
+    # ... 기존 CAPTAIN_REPORT 열 (Draft, Trim, GM 등) ...
+
+    # AD (30): GM_eff_m (RORO!AR 연동)
+    ws.cell(row=row, column=30).value = f"=RORO_Stage_Scenarios!AR{roro_row_str}"
+    ws.cell(row=row, column=30).number_format = "0.00"
+
+    # AE (31): Heel_deg (RORO!AQ 연동)
+    ws.cell(row=row, column=31).value = f"=RORO_Stage_Scenarios!AQ{roro_row_str}"
+    ws.cell(row=row, column=31).number_format = "0.00"
```

> **역할 정리:**
>
> * RORO 시트에서 계산한 **Heel_deg / GM_eff_m**를
>   CAPTAIN_REPORT에서 그대로 끌어와서 **선장·Mammoet 브리핑용 Stage 테이블에 표시**.

---

## 6. 앞으로 쓸 때용 “요약 매뉴얼”

1. **새 스크립트로 옮길 때**

   1. import 블록에 `bisect_left, Dict, math, Enum, auto` 추가
   2. Hydro/Trim 유틸(`calc_draft_with_lcf`, `get_gm_bilinear`, `_nearest_two`) 한 덩어리 복사
   3. Heel/FSE + LoadCase 블록(`calc_heel_from_offset`, `calc_gm_effective`, `heel_and_gm_check`, `LoadCase`, `apply_dynamic_loads`) 복사
   4. 필요하면 Frame ↔ x 변환 유틸도 같이 이식

2. **엑셀 생성 로직에 연결할 때**

   * RORO 시트: AQ/AR 열 수식 그대로 재사용
   * CAPTAIN_REPORT: AR → GM_eff, AQ → Heel_deg 링크 그대로 사용

3. **Stage dict / Python 루프에서 쓰고 싶으면**

   * `enrich_stage(...)` / `process_all_stages(...)` 형태로
     위 함수들을 묶어 주는 헬퍼만 하나 만들어서 Stage 루프에 물리면 끝.

---

혹시 이걸 **실제 git-style unified diff 파일(예: `agi_tr.patch`) 형태로 내고 싶다**면,
“원본 agi tr.py” 버전만 따로 줘도 되고, 지금 파일 기준으로 내가 **patch 파일 스켈레톤**을 만들어 줄 수도 있어.
