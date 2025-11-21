좋아, 이제 **실제 셀 주소(B8·B11, A14 헤더)** 기준으로 딱 쓸 수 있는 수식/코드 세트를 줄게.

---

## 1. 상단 파라미터 셋업 (한 번만)

시트 상단을 이렇게 맞춰 쓰면 된다.

* **B5** : `Tmean_baseline (m)`  → **이미 있음**
* **B8** : `MTC (t·m/cm)`        → 33.99 (이미 있음)
* **B11**: `pump_rate_e (t/h)`   → 45 (이미 있음)

여기에 **Trim 목표값만 하나 추가**:

* **A6** : `Trim_target_cm`
* **B6** : 예: `-96.5`  (선장/엔지니어가 합의한 목표 Trim_cm)

이제 아래 수식들이 전부 이 파라미터를 참조하게 된다.

---

## 2. 데이터 구간 위치

* 헤더 행: **14행** (`A14 = "Stage"`)
* 첫 데이터: **15행 (Stage 1)**

아래 `{row}` 자리에 15,16,... 들어간다고 보면 된다.

---

## 3. H열 `ΔTM_cm_tm` 수식 (핵심)

**의미:**
(현재 Trim_cm − 목표 Trim_target_cm) × MTC = 필요한 Trim 모멘트(cm·t·m)

### 엑셀 수식 (H열, 예: H15)

```excel
=IF($A15="","",(E15 - $B$6) * $B$8)
```

→ H15 입력 후, 아래로 드래그/복사.

### openpyxl 패치 (col=8)

```python
# H (8): ΔTM_cm_tm
ws.cell(row=row, column=8).value = (
    f'=IF($A{row_str}="","",(E{row_str} - $B$6) * $B$8)'
)
ws.cell(row=row, column=8).number_format = "0.00"
```

---

## 4. J열 `Ballast_t_calc` (이미 구조 OK, 값만 살리기)

**의미:**
ΔTM(H) / Lever_arm(I) = 이론상 필요한 Ballast_t

### 엑셀 수식 (J15)

```excel
=IF(OR($A15="",$I15="", $I15=0),"",ROUND(H15 / $I15, 2))
```

(지금도 비슷하게 있을 텐데, H가 0이어서 죽어있던 것만 H 수식으로 살리는 개념)

### openpyxl (참고)

```python
ws.cell(row=row, column=10).value = (
    f'=IF(OR($A{row_str}="",$I{row_str}="",$I{row_str}=0),"",'
    f'ROUND(H{row_str}/$I{row_str},2))'
)
ws.cell(row=row, column=10).number_format = "0.00"
```

---

## 5. 보라색 블록(AM~AP) – Option 1 Ballast Fix

컬럼 매핑 다시 정리:

* **AM**(39열): `ΔTM_needed_cm·tm`
* **AN**(40열): `Ballast_req_t`
* **AO**(41열): `Ballast_gap_t`
* **AP**(42열): `Time_Add_h`

### 5.1 AM `ΔTM_needed_cm·tm` (절대값)

```excel
=IF($A15="","",ABS(H15))
```

```python
# AM (39)
ws.cell(row=row, column=39).value = (
    f'=IF($A{row_str}="","",ABS(H{row_str}))'
)
ws.cell(row=row, column=39).number_format = "0.00"
```

---

### 5.2 AN `Ballast_req_t` (필요 Ballast)

J열과 같은 개념을 보라색 블록에서 명시:

```excel
=IF($A15="","",
   IF(OR($I15="", $I15=0),0,
      ROUND(H15/$I15,2)
   )
)
```

```python
# AN (40)
ws.cell(row=row, column=40).value = (
    f'=IF($A{row_str}="","",'
    f'IF(OR($I{row_str}="",$I{row_str}=0),0,ROUND(H{row_str}/$I{row_str},2)))'
)
ws.cell(row=row, column=40).number_format = "0.00"
```

---

### 5.3 AO `Ballast_gap_t` (필요 vs 실제 차이)

* 실제 투입 Ballast = **L열 Ballast_t**

```excel
=IF($A15="","",AN15 - $L15)
```

```python
# AO (41)
ws.cell(row=row, column=41).value = (
    f'=IF($A{row_str}="","",AN{row_str} - $L{row_str})'
)
ws.cell(row=row, column=41).number_format = "0.00"
```

---

### 5.4 AP `Time_Add_h` (추가 펌핑 시간)

* 펌프 레이트 = **B11 (pump_rate_e)**

```excel
=IF($A15="","",
   IF($B$11=0,0,
      AO15 / $B$11
   )
)
```

```python
# AP (42)
ws.cell(row=row, column=42).value = (
    f'=IF($A{row_str}="","",'
    f'IF($B$11=0,0,AO{row_str}/$B$11))'
)
ws.cell(row=row, column=42).number_format = "0.00"
```

---

## 6. 어떻게 쓰이면 되나?

* **H열**: “현재 Trim vs 목표 Trim” → 필요한 ΔTM
* **J/AN열**: ΔTM & Lever_arm로 계산한 “필요 Ballast_t”
* **AO열**: 필요한 Ballast − 실제 Ballast(L열) → “얼마나 더/덜 빼야 하는지”
* **AP열**: AO를 펌프 레이트(B11)로 나눈 추가 시간(h)

즉, Stage별로:

> “이 Stage에서 Trim을 목표값(B6)으로 맞추려면
> Ballast를 몇 톤 조정해야 하고, 펌프를 몇 시간 더 돌려야 하는지”

가 숫자로 바로 떨어지게 된다.

이대로 넣어보고, 특정 Stage(예: 5A-2, 6B)에서 결과가 감정상 안 맞는 느낌이 있으면
그 Stage 값 하나 잡고 같이 역산해서 미세 조정(부호·목표 Trim)까지 맞춰보자.
