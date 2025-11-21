# zzzzz.md 가이드 교차 검증 보고서

**검증 일시**: 2025-11-19
**검증 대상**: `zzzzz.md` 가이드 vs `agi tr.py` 및 문서들

---

## 1. 상단 파라미터 검증

### 1.1 zzzzz.md 가이드 요구사항

| 셀 | 헤더/값 | 설명 |
|----|---------|------|
| A6 | `Trim_target_cm` | 헤더 |
| B6 | `-96.5` | 목표 Trim_cm 값 |
| B8 | `MTC (t·m/cm)` | Calc 시트 참조 |
| B11 | `pump_rate_e (t/h)` | Calc 시트 참조 |

### 1.2 agi tr.py 구현 검증

**검증 결과**: ✅ **일치**

```python
# Line 923-926: Trim_target_cm 추가
ws["A6"] = "Trim_target_cm"
ws["B6"] = -96.5
ws["B6"].fill = styles["input_fill"]

# Line 929-931: B8 MTC
ws["B8"] = '=INDEX(Calc!$E:$E, MATCH("MTC_t_m_per_cm", Calc!$C:$C, 0))'
ws["B8"].fill = styles["input_fill"]

# Line 944-946: B11 pump_rate
ws["B11"] = "=Calc!$E$31"
ws["B11"].fill = styles["input_fill"]
```

**검증 항목**:
- ✅ A6: `"Trim_target_cm"` 헤더 설정
- ✅ B6: `-96.5` 값 설정
- ✅ B8: Calc 시트 직접 참조 수식 설정
- ✅ B11: Calc 시트 직접 참조 수식 설정

---

## 2. H열 (8) - ΔTM_cm_tm 검증

### 2.1 zzzzz.md 가이드 요구사항

**수식**: `=IF($A15="","",(E15 - $B$6) * $B$8)`

**의미**: (현재 Trim_cm − 목표 Trim_target_cm) × MTC = 필요한 Trim 모멘트(cm·t·m)

### 2.2 agi tr.py 구현 검증

**검증 결과**: ✅ **일치**

```python
# Line 1090-1094
ws.cell(row=row, column=8).value = (
    f'=IF($A{row_str}="","",(E{row_str} - $B$6) * $B$8)'
)
```

**검증 항목**:
- ✅ 수식 구조: `(E{row} - $B$6) * $B$8`
- ✅ 조건문: `IF($A{row}="","",...)`
- ✅ 참조: `$B$6` (Trim_target_cm), `$B$8` (MTC)

---

## 3. J열 (10) - Ballast_t_calc 검증

### 3.1 zzzzz.md 가이드 요구사항

**수식**: `=IF(OR($A15="",$I15="", $I15=0),"",ROUND(H15 / $I15, 2))`

**의미**: ΔTM(H) / Lever_arm(I) = 이론상 필요한 Ballast_t

### 3.2 agi tr.py 구현 검증

**검증 결과**: ✅ **일치**

```python
# Line 1100-1103
ws.cell(row=row, column=10).value = (
    f'=IF(OR($A{row_str}="",$I{row_str}="", $I{row_str}=0),"",ROUND(H{row_str} / $I{row_str}, 2))'
)
```

**검증 항목**:
- ✅ 수식 구조: `H{row} / $I{row}`
- ✅ 조건문: `IF(OR($A{row}="",$I{row}="", $I{row}=0),...)`
- ✅ 반올림: `ROUND(..., 2)`

---

## 4. K열 (11) - Ballast_time_h_calc 검증

### 4.1 zzzzz.md 가이드 요구사항

**수식**: J를 펌프 레이트(B11)로 나눈 시간

### 4.2 agi tr.py 구현 검증

**검증 결과**: ✅ **일치**

```python
# Line 1105-1108
ws.cell(row=row, column=11).value = (
    f'=IF(OR(J{row_str}="", $B$11="", $B$11=0, ISERROR($B$11)), "", ROUND(J{row_str} / $B$11, 2))'
)
```

**검증 항목**:
- ✅ 수식 구조: `J{row} / $B$11`
- ✅ 조건문: `IF(OR(J{row}="", $B$11="", $B$11=0, ISERROR($B$11)),...)`
- ✅ 참조: `$B$11` (pump_rate_effective_tph)

---

## 5. AM열 (39) - ΔTM_needed_cm·tm 검증

### 5.1 zzzzz.md 가이드 요구사항

**수식**: `=IF($A15="","",ABS(H15))`

**의미**: H 컬럼의 절대값 (Trim 모멘트 크기만)

### 5.2 agi tr.py 구현 검증

**검증 결과**: ✅ **일치**

```python
# Line 1678-1679
ws.cell(row=row, column=39).value = f'=IF($A{row_str}="","",ABS(H{row_str}))'
```

**검증 항목**:
- ✅ 수식 구조: `ABS(H{row})`
- ✅ 조건문: `IF($A{row}="","",...)`

---

## 6. AN열 (40) - Ballast_req_t 검증

### 6.1 zzzzz.md 가이드 요구사항

**수식**: `=IF($A15="","",IF(OR($I15="", $I15=0),0,ROUND(H15/$I15,2)))`

**의미**: J열과 같은 개념 (H/I)

### 6.2 agi tr.py 구현 검증

**검증 결과**: ✅ **일치**

```python
# Line 1682-1686
ws.cell(row=row, column=40).value = (
    f'=IF($A{row_str}="","",'
    f'IF(OR($I{row_str}="",$I{row_str}=0),0,ROUND(H{row_str}/$I{row_str},2)))'
)
```

**검증 항목**:
- ✅ 수식 구조: `H{row}/$I{row}`
- ✅ 조건문: `IF(OR($I{row}="",$I{row}=0),0,...)`
- ✅ 반올림: `ROUND(...,2)`

---

## 7. AO열 (41) - Ballast_gap_t 검증

### 7.1 zzzzz.md 가이드 요구사항

**수식**: `=IF($A15="","",AN15 - $L15)`

**의미**: 필요한 Ballast(AN) - 실제 Ballast(L)

### 7.2 agi tr.py 구현 검증

**검증 결과**: ✅ **일치**

```python
# Line 1690-1693
ws.cell(row=row, column=41).value = (
    f'=IF($A{row_str}="","",AN{row_str} - $L{row_str})'
)
```

**검증 항목**:
- ✅ 수식 구조: `AN{row} - $L{row}`
- ✅ 조건문: `IF($A{row}="","",...)`

---

## 8. AP열 (42) - Time_Add_h 검증

### 8.1 zzzzz.md 가이드 요구사항

**수식**: `=IF($A15="","",IF($B$11=0,0,AO15/$B$11))`

**의미**: AO를 펌프 레이트(B11)로 나눈 추가 시간

### 8.2 agi tr.py 구현 검증

**검증 결과**: ✅ **일치**

```python
# Line 1697-1700
ws.cell(row=row, column=42).value = (
    f'=IF($A{row_str}="","",' f"IF($B$11=0,0,AO{row_str}/$B$11))"
)
```

**검증 항목**:
- ✅ 수식 구조: `AO{row}/$B$11`
- ✅ 조건문: `IF($B$11=0,0,...)`
- ✅ 참조: `$B$11` (pump_rate_effective_tph)

---

## 9. 문서 업데이트 필요 사항

### 9.1 EXCEL_GEN_01_OVERVIEW_AND_ARCHITECTURE.md

**현재 상태**: Version 3.6 (2025-11-18)
**업데이트 필요**: ✅ **Version 3.8 반영 필요**

**업데이트 항목**:
- RORO_Stage_Scenarios 시트 상단 파라미터 (A6, B6, B8, B11) 추가
- H/J/K/AM~AP 컬럼 수식 업데이트 내용 반영
- Output 파일명: `LCT_BUSHRA_AGI_TR_Integrated_v2.xlsx`

### 9.2 EXCEL_GEN_02_FUNCTIONS_AND_IMPLEMENTATION.md

**현재 상태**: Version 3.6 (2025-11-18)
**업데이트 필요**: ✅ **Version 3.8 반영 필요**

**업데이트 항목**:
- `create_roro_sheet()` 함수: A6/B6/B8/B11 파라미터 추가 설명
- H/J/K 컬럼 수식 업데이트 설명
- AM~AP 컬럼 수식 업데이트 설명 (Option 1 Ballast Fix 블록)

### 9.3 EXCEL_GEN_03_MATHEMATICS_AND_DATA_FLOW.md

**현재 상태**: Version 3.6 (2025-11-18)
**업데이트 필요**: ✅ **Version 3.8 반영 필요**

**업데이트 항목**:
- Trim Calculations 섹션: Trim_target 기반 ΔTM 계산 추가
- Ballast Calculations 섹션: H/J/AM~AP 컬럼 수식 업데이트
- Option 1 Ballast Fix Check 섹션: 수식 업데이트 반영

### 9.4 EXCEL_GEN_04_ALGORITHM_LOGIC_ARCHITECTURE.md

**현재 상태**: Version 3.6 (2025-11-18)
**업데이트 필요**: ✅ **Version 3.8 반영 필요**

**업데이트 항목**:
- Formula Generation Algorithm: H/J/K/AM~AP 수식 생성 로직 업데이트
- RORO Sheet Creation Logic: 상단 파라미터 추가 로직 반영

---

## 10. 종합 검증 결과

### 10.1 코드 구현 검증

| 항목 | zzzzz.md 가이드 | agi tr.py 구현 | 상태 |
|------|----------------|----------------|------|
| A6 헤더 | `Trim_target_cm` | `"Trim_target_cm"` | ✅ 일치 |
| B6 값 | `-96.5` | `-96.5` | ✅ 일치 |
| B8 수식 | Calc 시트 참조 | `=INDEX(Calc!$E:$E, MATCH("MTC_t_m_per_cm", Calc!$C:$C, 0))` | ✅ 일치 |
| B11 수식 | Calc 시트 참조 | `=Calc!$E$31` | ✅ 일치 |
| H열 수식 | `(E - $B$6) * $B$8` | `(E{row} - $B$6) * $B$8` | ✅ 일치 |
| J열 수식 | `H / I` | `H{row} / $I{row}` | ✅ 일치 |
| K열 수식 | `J / $B$11` | `J{row} / $B$11` | ✅ 일치 |
| AM열 수식 | `ABS(H)` | `ABS(H{row})` | ✅ 일치 |
| AN열 수식 | `H / I` | `H{row}/$I{row}` | ✅ 일치 |
| AO열 수식 | `AN - L` | `AN{row} - $L{row}` | ✅ 일치 |
| AP열 수식 | `AO / $B$11` | `AO{row}/$B$11` | ✅ 일치 |

### 10.2 문서 업데이트 상태

| 문서 | 현재 버전 | 업데이트 필요 | 상태 |
|------|----------|--------------|------|
| EXCEL_GEN_01 | 3.6 | ✅ 필요 | ⚠️ 미반영 |
| EXCEL_GEN_02 | 3.6 | ✅ 필요 | ⚠️ 미반영 |
| EXCEL_GEN_03 | 3.6 | ✅ 필요 | ⚠️ 미반영 |
| EXCEL_GEN_04 | 3.6 | ✅ 필요 | ⚠️ 미반영 |
| CHANGELOG.md | 3.8 | ✅ 완료 | ✅ 반영됨 |

---

## 11. 결론

### 11.1 코드 구현 상태

✅ **완벽히 일치**: `agi tr.py`의 구현이 `zzzzz.md` 가이드와 100% 일치합니다.

- 모든 수식이 가이드 요구사항과 정확히 일치
- 셀 참조가 올바르게 구현됨
- 조건문과 반올림이 정확히 적용됨

### 11.2 문서 업데이트 필요

⚠️ **문서 업데이트 필요**: 4개 문서 파일이 Version 3.8 변경사항을 반영하지 않았습니다.

**권장 조치**:
1. EXCEL_GEN_01~04 문서들을 Version 3.8로 업데이트
2. zzzzz.md 가이드의 변경사항을 각 문서에 반영
3. 수식 설명 및 예시 업데이트

---

**검증 완료 일시**: 2025-11-19
**검증자**: MACHO-GPT

