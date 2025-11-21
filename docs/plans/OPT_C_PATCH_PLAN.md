# Opt C (High Tide + 최대 밸러스트) 전략 패치 계획

**작성일**: 2025-11-19  
**대상 파일**: `agi tr.py`  
**참조 문서**: `AAAAAAAA.PY`

---

## 📋 개요

Opt C 전략은 TR1 Final + TR2 Ramp 위치의 크리티컬한 Bow-trim Stage를 추가하고, 필요한 최소 조위(Tide)를 계산하는 기능입니다.

### 주요 변경사항
1. **새 Stage 추가**: `Stage 6A_Critical (Opt C)` (13번째 Stage)
2. **새 컬럼 추가**: `Required_Tide_m` (AX, 50), `Tide_OK` (AY, 51)
3. **Excel Table 범위 확장**: AW(49) → AY(51)

---

## 🔍 현재 코드 구조 분석

### 1. Stage 정의 구조
- **위치**: `create_roro_sheet()` 함수 내
- **stages 리스트**: 문자열 리스트 (line 1131-1144, 12개 Stage)
- **stage_defaults 딕셔너리**: W, x 값 정의 (line 1167-1191)
- **target_trim_by_stage 딕셔너리**: Trim target 값 정의 (line 1149-1162)

### 2. 컬럼 구조
- **현재 마지막 컬럼**: AW(49) - Von_Mises_Check
- **Phys_Freeboard_m**: Z(26) 컬럼
- **Tide_ref**: B5 셀 (RORO_Stage_Scenarios 시트)

### 3. Stage Notes 위치
- **G4-G15**: Stage 1-12의 Notes
- **F4-F15**: Stage 1-12의 이름

---

## 📝 패치 단계별 계획

### Phase 1: Opt C Stage 생성 함수 추가

**위치**: `create_roro_sheet()` 함수 이전 (line 900 근처)

**추가할 함수**:
```python
def build_opt_c_stage():
    """
    Stage 6A_Critical (Opt C)
    - TR1: final deck position (Fr ≈ 42.0)
    - TR2: ramp tip position (Fr ≈ -5.0)
    - 둘 다 434 t 가정 (TR1/2 동일중량), 합계 868 t
    - target_trim_cm 은 현실적인 bow down 목표값(-100 cm)으로 설정
    """
    fr_tr1 = 42.0        # TR1 final stowage frame
    fr_tr2 = -5.0        # TR2 ramp tip frame (estimated)
    x_tr1 = fr_to_x(fr_tr1)   # ≈ 11.85 m
    x_tr2 = fr_to_x(fr_tr2)   # ≈ -35.15 m

    w_tr1 = 434.0
    w_tr2 = 434.0
    w_total = w_tr1 + w_tr2

    # Combined LCG (x_from_mid_m)
    combined_x = (w_tr1 * x_tr1 + w_tr2 * x_tr2) / w_total

    return {
        "name": "Stage 6A_Critical (Opt C)",
        "weight_t": w_total,          # 868.00 t
        "x_from_mid_m": combined_x,   # ≈ -11.65 m (bow side)
        "target_trim_cm": -100.0,
    }
```

**검증 사항**:
- `fr_to_x()` 함수가 정상 작동하는지 확인
- 계산된 combined_x가 약 -11.65 m인지 확인

---

### Phase 2: create_roro_sheet() 수정

#### 2.1 stages 리스트에 Opt C 추가

**위치**: line 1144 이후

**변경사항**:
```python
stages = [
    "Stage 1",
    # ... 기존 12개 Stage ...
    "Stage 7",
]
# Opt C Stage 추가
stages.append("Stage 6A_Critical (Opt C)")
```

**검증 사항**:
- stages 리스트 길이가 12 → 13으로 변경
- 마지막 요소가 "Stage 6A_Critical (Opt C)"인지 확인

---

#### 2.2 stage_defaults에 Opt C 추가

**위치**: line 1191 이후

**변경사항**:
```python
stage_defaults = {
    # ... 기존 Stage들 ...
    "Stage 7": {"W": 0.0, "x": fr_to_x(30.15)},
    # Opt C Stage 추가
    "Stage 6A_Critical (Opt C)": {
        "W": 868.0,
        "x": (434.0 * fr_to_x(42.0) + 434.0 * fr_to_x(-5.0)) / 868.0
    },
}
```

**검증 사항**:
- x 값이 약 -11.65 m인지 확인
- W 값이 868.0인지 확인

---

#### 2.3 target_trim_by_stage에 Opt C 추가

**위치**: line 1162 이후

**변경사항**:
```python
target_trim_by_stage = {
    # ... 기존 Stage들 ...
    "Stage 7": 0.0,
    # Opt C Stage 추가
    "Stage 6A_Critical (Opt C)": -100.0,
}
```

**검증 사항**:
- target_trim_cm 값이 -100.0인지 확인

---

#### 2.4 Stage Notes에 Opt C 추가

**위치**: line 1089 이후 (stage_notes 딕셔너리)

**변경사항**:
```python
stage_notes = {
    # ... 기존 Stage들 ...
    "Stage 7": "Cargo off (TR removed), symmetric ballast around midship.",
    # Opt C Stage 추가
    "Stage 6A_Critical (Opt C)": "TR1 Final + TR2 Ramp (Critical Bow-trim Stage). Requires high tide + maximum aft ballast.",
}
```

**위치**: line 1091 이후 (G4-G15 배치 루프)

**변경사항**:
- 루프 범위를 `range(12)` → `range(13)`으로 변경
- G16에 Opt C Stage Note 배치

**검증 사항**:
- G16에 Opt C Stage Note가 정상 배치되는지 확인

---

#### 2.5 F4-F15 Stage 이름 복사 로직에 Opt C 추가

**위치**: line 1313 이후

**변경사항**:
- 루프 범위를 `range(12)` → `range(13)`으로 변경
- F16에 Opt C Stage 이름 복사

**검증 사항**:
- F16에 "Stage 6A_Critical (Opt C)"가 정상 복사되는지 확인

---

### Phase 3: extend_roro_structural_opt1() 수정

#### 3.1 컬럼 헤더 추가

**위치**: line 1774 이후 (ramp_stress_cols 정의 후)

**변경사항**:
```python
# Opt C / High Tide 관련 컬럼 (AX-AY)
opt_c_tide_cols = [
    "Required_Tide_m",  # AX (50)
    "Tide_OK",          # AY (51)
]

all_cols = (
    structural_cols
    + dynamic_load_cols
    + opt1_cols
    + heel_fse_cols
    + ramp_stress_cols
    + opt_c_tide_cols  # 추가
)
```

**검증 사항**:
- all_cols 길이가 2 증가하는지 확인
- 마지막 2개 요소가 "Required_Tide_m", "Tide_OK"인지 확인

---

#### 3.2 헤더 Fill 색상 설정

**위치**: line 1814 이후 (Fill 색상 설정 로직)

**변경사항**:
```python
# Opt C Tide 컬럼은 opt1_fill (보라색) 사용
elif i < len(structural_cols) + len(dynamic_load_cols) + len(opt1_cols) + len(heel_fse_cols) + len(ramp_stress_cols) + len(opt_c_tide_cols):
    cell.fill = styles["opt1_fill"]  # Opt C Tide uses opt1 fill
```

**검증 사항**:
- AX, AY 헤더 셀이 opt1_fill 색상으로 설정되는지 확인

---

#### 3.3 데이터 행 수식 추가

**위치**: line 1956 이후 (AW 컬럼 수식 후)

**변경사항**:
```python
# AX (50): Required_Tide_m
# Required_Tide_m = IF(Phys_Freeboard_m>=0, 0, ABS(Phys_Freeboard_m) + 0.30)
# Z{row}: Phys_Freeboard_m (column 26)
ws.cell(row=row, column=50).value = (
    f'=IF(Z{row_str}="", "", IF(Z{row_str}>=0, 0, ABS(Z{row_str})+0.30))'
)
ws.cell(row=row, column=50).number_format = number_format
ws.cell(row=row, column=50).font = styles["normal_font"]

# AY (51): Tide_OK
# Tide_OK = IF(Tide_ref >= Required_Tide_m, "OK", "CHECK")
# Tide_ref는 RORO_Stage_Scenarios!B5
ws.cell(row=row, column=51).value = (
    f'=IF(AX{row_str}="", "", IF($B$5>=AX{row_str}, "OK", "CHECK"))'
)
ws.cell(row=row, column=51).font = styles["normal_font"]
```

**검증 사항**:
- AX(50) 수식이 Z(26) Phys_Freeboard_m을 참조하는지 확인
- AY(51) 수식이 B5 Tide_ref를 참조하는지 확인
- 수식이 모든 Stage 행(18-30)에 적용되는지 확인

---

#### 3.4 컬럼 너비 설정

**위치**: line 1969 이후

**변경사항**:
```python
# Opt C Tide 컬럼 너비 설정
ws.column_dimensions["AX"].width = 15  # Required_Tide_m
ws.column_dimensions["AY"].width = 12  # Tide_OK
```

**검증 사항**:
- AX, AY 컬럼 너비가 정상 설정되는지 확인

---

### Phase 4: create_workbook_from_scratch() 수정

#### 4.1 Excel Table 범위 업데이트

**위치**: line 2296

**변경사항**:
```python
last_col = 51  # Opt C Tide 컬럼 추가로 AW(49) → AY(51)로 이동
```

**검증 사항**:
- last_col이 49 → 51로 변경되는지 확인
- last_col_letter가 "AY"로 계산되는지 확인

---

#### 4.2 Excel Table 헤더 검증 루프

**위치**: line 2305

**변경사항**:
- 루프 범위가 `range(1, 52)`로 자동 확장됨 (last_col + 1)
- T(20) 컬럼은 여전히 건너뛰기

**검증 사항**:
- AX(50), AY(51) 헤더가 정상 검증되는지 확인
- T(20)은 여전히 건너뛰어지는지 확인

---

#### 4.3 Excel Table 범위 문자열

**위치**: line 2320

**변경사항**:
- Table ref가 자동으로 `A17:AY{last_row}`로 확장됨

**검증 사항**:
- Table 범위가 AY까지 포함하는지 확인
- last_row가 13개 Stage를 포함하는지 확인 (first_data_row + 12)

---

## ⚠️ 주의사항

### 1. Tide_ref 셀 참조
- **현재 위치**: RORO_Stage_Scenarios!B5
- **수식에서 사용**: `$B$5` (절대 참조)
- **확인 필요**: AAAAAAAAA.PY에서는 B3으로 언급되었으나, 실제 코드는 B5 사용

### 2. Phys_Freeboard_m 컬럼
- **현재 위치**: Z(26)
- **수식**: `=IF(O{row}="", "", $B$9 - O{row})`
- **Required_Tide_m 수식**: `=IF(Z{row}>=0, 0, ABS(Z{row})+0.30)`

### 3. Stage 개수 변경 영향
- **기존**: 12개 Stage (Rows 18-29)
- **변경 후**: 13개 Stage (Rows 18-30)
- **영향받는 함수들**:
  - `create_captain_report_sheet()`: `len(stages)` 자동 반영
  - `extend_roro_captain_req()`: `num_stages` 파라미터 자동 반영
  - `extend_roro_structural_opt1()`: `num_stages` 파라미터 자동 반영

### 4. Excel Table 범위
- **기존**: `A17:AW{last_row}` (49 columns)
- **변경 후**: `A17:AY{last_row}` (51 columns, T(20) 제외 시 50 columns)
- **주의**: T(20)은 빈 컬럼으로 유지되므로 Excel Table은 연속 범위로 처리됨

---

## ✅ 검증 체크리스트

### 코드 수정 전
- [ ] `fr_to_x()` 함수가 정상 작동하는지 확인
- [ ] Tide_ref가 B5에 있는지 확인
- [ ] Phys_Freeboard_m이 Z(26)에 있는지 확인

### 코드 수정 후
- [ ] `build_opt_c_stage()` 함수가 정상 작동하는지 확인
- [ ] stages 리스트에 Opt C Stage가 추가되었는지 확인
- [ ] stage_defaults에 Opt C Stage가 추가되었는지 확인
- [ ] target_trim_by_stage에 Opt C Stage가 추가되었는지 확인
- [ ] G16에 Opt C Stage Note가 배치되었는지 확인
- [ ] F16에 Opt C Stage 이름이 복사되었는지 확인
- [ ] AX(50), AY(51) 헤더가 정상 생성되었는지 확인
- [ ] AX(50), AY(51) 수식이 모든 Stage 행에 적용되었는지 확인
- [ ] Excel Table 범위가 AY까지 확장되었는지 확인
- [ ] 스크립트가 정상 실행되는지 확인
- [ ] Excel 파일이 정상 생성되는지 확인
- [ ] Opt C Stage 행의 값들이 정상 계산되는지 확인

### Excel 파일 검증
- [ ] Stage 6A_Critical (Opt C) 행이 Row 30에 있는지 확인
- [ ] AX(50) Required_Tide_m 수식이 정상 작동하는지 확인
- [ ] AY(51) Tide_OK 수식이 정상 작동하는지 확인
- [ ] Opt C Stage의 Phys_Freeboard_m 값이 음수인 경우 Required_Tide_m이 계산되는지 확인
- [ ] Tide_ref(B5) 값에 따라 Tide_OK가 "OK" 또는 "CHECK"로 표시되는지 확인

---

## 📊 예상 결과

### Opt C Stage 예상 값
- **W_stage_t**: 868.00 t
- **x_stage_m**: ≈ -11.65 m (bow side)
- **target_trim_cm**: -100.0 cm
- **Phys_Freeboard_m**: 예상 -1.20 m (음수)
- **Required_Tide_m**: 예상 1.50 m (ABS(-1.20) + 0.30)
- **Tide_OK**: Tide_ref(B5) ≥ 1.50 m이면 "OK", 아니면 "CHECK"

---

## 🔄 롤백 계획

패치 실패 시:
1. Git을 사용하는 경우: `git checkout agi tr.py`로 원본 복원
2. 백업 파일이 있는 경우: 백업 파일로 복원
3. 수동 롤백: 변경사항을 역순으로 제거

---

## 📝 다음 단계

1. 패치 적용
2. 스크립트 실행
3. Excel 파일 검증
4. Opt C Stage 값 확인
5. CHANGELOG.md 업데이트 (Version 3.9.4)

---

**작성자**: MACHO-GPT  
**검토 필요**: Opt C Stage의 target_trim_cm 값(-100.0)이 적절한지 확인

