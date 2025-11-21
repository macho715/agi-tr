좋아, 옵션 A 확정이면 이렇게 하면 된다.
**핵심은 “Q열에 Stage별 Trim_target_cm 컬럼 추가 → H열 수식만 살짝 변경”**이야.

---

## 1. 새 컬럼 구조 (엑셀 작업 순서)

1. `Dfwd_m` / `Daft_m` 오른쪽에 새 컬럼 삽입

   * 현재: `O:Dfwd_m`, `P:Daft_m`, `Q:FWD_Height_m` …
   * **작업:** `Q` 열 전체 선택 → 오른쪽 클릭 → `삽입`
   * 삽입 후 컬럼 매핑:

     * `Q: Trim_target_stage_cm`  ✅ (새 컬럼)
     * `R: FWD_Height_m`
     * `S: AFT_Height_m`
     * `T: Notes`
     * 이후 컬럼들은 한 칸씩 오른쪽으로 밀림 (GM, Freeboard, …, Von_Mises_Check 모두 +1열)

2. 헤더 입력

   * `Q14` 셀에: `Trim_target_stage_cm`

3. 값 입력 (Stage별)

   * **Stage 1, Stage 5, Stage 7 행(Q열)**: `0`
   * 나머지 Stage(2,3,4, 5A-1, 5A-2, 5A-3, 6A, 6B, 6C)는 **비워둔다**
     → 비워둔 Stage는 전역 타깃(B6 = -96.5)을 쓰고,
     1/5/7만 `0 cm`를 Stage별 타깃으로 사용.

---

## 2. H열 수식 변경 (ΔTM_cm_tm)

**기존(전역 타깃만 사용):**

```excel
=IF($A15="","",(E15 - $B$6) * $B$8)
```

**새 수식 (Stage별 타깃 우선, 없으면 B6):**

```excel
=IF($A15="","",
   (E15 - IF($Q15="",$B$6,$Q15)) * $B$8
)
```

* 의미:

  * Q15가 비었으면 → 전역 타깃 `$B$6`(-96.5 cm) 사용
  * Q15에 값이 있으면 → 그 Stage만의 타깃(예: 0 cm) 사용

**적용 방법**

1. `H15` 셀에 위 수식 입력
2. H열 전체(데이터 범위)로 아래로 채우기

→ 결과 기대값:

* Stage 1 / 5 / 7:

  * `Trim_cm = 0`, `Trim_target_stage_cm = 0` → ΔTrim = 0 → **H = 0**,
    J/AM/AN/AO/AP도 0 또는 BLANK → “Baseline은 Fix 대상 아님”
* 5A-1, 5A-2, 6A~6C 등:

  * Q는 공백 → B6(-96.5)를 타깃으로 사용 → **Fix 대상 Stage만 ΔTM 발생**

---

## 3. Python (`agi tr.py`) 패치 가이드

### 3.1 헤더 생성부

헤더 row(14행) 만드는 부분에서, 기존에 FWD/AFT_Height를 바로 쓰던 곳 사이에 새 컬럼을 하나 끼워 넣어야 해.

```python
# 예시: 기존
headers = [
    "Stage", "W_stage_t", "x_stage_m", "TM (t·m)", "Trim_cm",
    "FWD_precise_m", "AFT_precise_m", "ΔTM_cm_tm", "Lever_arm_m",
    "Ballast_t_calc", "Ballast_time_h_calc", "Ballast_t", "Ballast_time_h",
    "Trim_Check", "Dfwd_m", "Daft_m",
    "FWD_Height_m", "AFT_Height_m", "Notes", ...
]

# 수정 후
headers = [
    "Stage", "W_stage_t", "x_stage_m", "TM (t·m)", "Trim_cm",
    "FWD_precise_m", "AFT_precise_m", "ΔTM_cm_tm", "Lever_arm_m",
    "Ballast_t_calc", "Ballast_time_h_calc", "Ballast_t", "Ballast_time_h",
    "Trim_Check", "Dfwd_m", "Daft_m",
    "Trim_target_stage_cm",          # ← 새 컬럼 (Q)
    "FWD_Height_m", "AFT_Height_m", "Notes", ...
]
```

→ 이 순서대로 쓰면 `Trim_target_stage_cm`가 Q열(17열)에 고정된다.

### 3.2 H열 수식 생성부

지금 H열을 만드는 코드가 대략 이런 형태일 거야:

```python
# H (8): ΔTM_cm_tm
ws.cell(row=row, column=8).value = (
    f'=IF($A{row_str}="","",(E{row_str} - $B$6) * $B$8)'
)
```

이걸 **Stage별 타깃 버전**으로 교체:

```python
# H (8): ΔTM_cm_tm = (Trim_cm - Trim_target) * MTC
# Trim_target = IF(Q="", $B$6, Q)
ws.cell(row=row, column=8).value = (
    f'=IF($A{row_str}="","",'
    f'(E{row_str} - IF($Q{row_str}="",$B$6,$Q{row_str})) * $B$8)'
)
ws.cell(row=row, column=8).number_format = "0.00"
```

### 3.3 Stage dict로 타깃 미리 넣고 싶으면 (선택)

`stages = [...]` 리스트에 Stage별 메타를 넣을 때:

```python
stages = [
    {"name": "Stage 1", "trim_target_stage_cm": 0},
    {"name": "Stage 2"},
    {"name": "Stage 3"},
    {"name": "Stage 4"},
    {"name": "Stage 5", "trim_target_stage_cm": 0},
    {"name": "Stage 5A-1 (At-Limit)"},
    {"name": "Stage 5A-2 (Optimized)"},
    {"name": "Stage 5A-3 (Max-Safety)"},
    {"name": "Stage 6A"},
    {"name": "Stage 6B"},
    {"name": "Stage 6C"},
    {"name": "Stage 7", "trim_target_stage_cm": 0},
]
```

그리고 Q열 채우는 루프:

```python
# Q 컬럼 (17): Trim_target_stage_cm
target = stage.get("trim_target_stage_cm")
if target is None:
    ws.cell(row=row, column=17).value = ""      # 공백 → B6 사용
else:
    ws.cell(row=row, column=17).value = float(target)
ws.cell(row=row, column=17).number_format = "0.00"
```

---

## 4. 결과 정리

* **Stage 1/5/7**

  * Q열=0 → “Baseline은 Trim=0이 타깃”
  * H=0, J=0, AM~AP=0 → Fix 계산에서 자연스럽게 빠진다.

* **5A/6 시리즈**

  * Q열 공백 → 전역 타깃(B6=-96.5) 사용
  * H/J/AM/AN/AO/AP만 살아서 “실제 Trim vs 목표 Trim(-96.5) 차이”를 보여준다.

이렇게 패치하면,

> “Baseline/운영상 Stage”와 “Trim Fix 대상 Stage”를 **한 시트 안에서 깔끔하게 분리**하면서도
> 캡틴·Mammoet·Aries한테는 **정확히 어떤 Stage에서 얼마만큼 Ballast 조정이 필요한지 숫자로 설명**할 수 있게 된다.
