# Captain Mail Response - 패치 실행 가이드

**작성일:** 2025-11-18  
**목적:** captain.md에서 설명한 4가지 패치를 실제로 실행하기 위한 단계별 가이드

---

## ✅ 사전 준비사항

### 1. 환경 확인
```bash
# Python 버전 확인 (3.7 이상 필요)
python --version

# 필수 패키지 확인
pip list | grep openpyxl
pip list | grep pandas
```

### 2. 현재 파일 백업
```bash
# Windows PowerShell에서 실행
cd C:\Users\SAMSUNG\Downloads\KZ_measurement_note
copy output\LCT_BUSHRA_AGI_TR.xlsx backup\LCT_BUSHRA_AGI_TR_before_captain_patch_$(Get-Date -Format 'yyyyMMdd_HHmmss').xlsx
```

---

## 📋 패치 항목 요약

| Patch ID | 목적 | 예상 소요시간 |
|----------|------|---------------|
| P1 | Calc 시트 제원 검증 및 업데이트 | 10분 |
| P2 | Stage 5A-2 수식 정합 | 15분 |
| P3 | X_Ballast 탱크 CG 기반 재계산 | 20분 |
| P4 | CAPTAIN_REPORT 시트 자동 생성 | 15분 |
| **총계** | | **60분** |

---

## 🔧 패치 실행 방법

### 방법 1: 자동화 스크립트 (권장)

#### Step 1: 패치 스크립트 생성
```bash
cd scripts\special
```

**파일명:** `patch_captain_response.py`

아래 명령으로 스크립트를 실행하여 4가지 패치를 자동으로 적용:

```bash
python patch_captain_response.py --input ..\..\output\LCT_BUSHRA_AGI_TR.xlsx --output ..\..\output\LCT_BUSHRA_AGI_TR_CAPTAIN_PATCHED.xlsx --verbose
```

**스크립트 옵션:**
- `--input`: 원본 Excel 파일 경로
- `--output`: 패치된 Excel 파일 경로
- `--verbose`: 상세 로그 출력
- `--dry-run`: 실제 수정 없이 미리보기만

#### Step 2: 검증
```bash
cd ..\..
python verify_excel_generation.py --file output\LCT_BUSHRA_AGI_TR_CAPTAIN_PATCHED.xlsx --detailed
```

---

### 방법 2: 수동 패치 (상세 제어 필요시)

#### P1: Calc 시트 제원 업데이트

**파일 열기:** `output\LCT_BUSHRA_AGI_TR.xlsx`

**시트:** `Calc`

**수정 항목:**
1. `D_vessel_m` (셀 D8):
   - 현재값 확인: `=4.85` → 
   - 변경: `=3.65`

2. `MTC_t_m_per_cm` (셀 D15):
   - 현재값 확인: `=0.0` 또는 빈 셀 →
   - 변경: `=33.99`

3. `LCF_from_AP_m` (셀 D17):
   - 현재값 확인
   - Midship 기준인지 검증 (음수 = Forward, 양수 = Aft)

**검증:**
```python
# Python으로 검증
from openpyxl import load_workbook
wb = load_workbook('output/LCT_BUSHRA_AGI_TR.xlsx')
ws = wb['Calc']
print(f"D_vessel: {ws['D8'].value}")  # Should be 3.65
print(f"MTC: {ws['D15'].value}")      # Should be 33.99
```

---

#### P2: Stage 5A-2 수식 정합

**시트:** `RORO_Stage_Scenarios`

**수정 항목:**

1. **Stage 5A-2 행 찾기** (보통 10~15행 근처)

2. **Dfwd_m 셀 수식 확인:**
   - 현재: 하드코딩된 값 (예: `2.32` 또는 `2.92`)
   - 변경: 수식 기반
   ```excel
   =Tmean + (Trim_cm/100)/2
   ```
   (부호는 trim 기준에 따라 조정)

3. **연결 확인:**
   - `Tmean` → 상단 `Tmean_baseline` 참조
   - `Trim_cm` → `TRIM_BY_STAGE` Named Range 참조

**검증:**
```python
ws = wb['RORO_Stage_Scenarios']
# Stage 5A-2 행을 찾아서
stage_5a2_row = None
for row in range(10, 20):
    if ws.cell(row, 1).value == "Stage 5A-2":
        stage_5a2_row = row
        break

if stage_5a2_row:
    dfwd_cell = ws.cell(stage_5a2_row, 5)  # Dfwd_m 컬럼
    print(f"Dfwd formula: {dfwd_cell.value}")
    print(f"Dfwd is formula: {dfwd_cell.data_type == 'f'}")
```

---

#### P3: X_Ballast 탱크 CG 기반 재계산

**필요 데이터:** `bushra_stability/data/master_tanks.json`

**작업:**

1. **탱크 CG 계산:**
   ```python
   import json
   
   with open('bushra_stability/data/master_tanks.json', 'r') as f:
       tanks = json.load(f)
   
   # Stage 5A-2 탱크 선택
   stage_5a2_tanks = ['FWB1', 'FWB2', 'FWCARGO1_P', 'FWCARGO1_S']
   
   total_weight = 0
   total_moment = 0
   
   for tank_id in stage_5a2_tanks:
       if tank_id in tanks:
           weight = tanks[tank_id]['capacity']  # 또는 실제 적재량
           x_cg = tanks[tank_id]['x_cg']
           total_weight += weight
           total_moment += weight * x_cg
   
   X_Ballast_effective = total_moment / total_weight
   print(f"Calculated X_Ballast: {X_Ballast_effective:.2f} m")
   ```

2. **Excel 업데이트:**
   - 시트: `RORO_Stage_Scenarios`
   - 셀: `X_Ballast_m` (보통 상단 파라미터 영역)
   - 값: 계산된 `X_Ballast_effective`

3. **설명 텍스트 수정:**
   - "AFT ballast 470 t" →
   - "Forward tanks ballast (FWB1/2 + FWCARGO1 P/S) ≈ 470 t"

---

#### P4: CAPTAIN_REPORT 시트 추가

**새 시트 생성:** `CAPTAIN_REPORT`

**구조:**

| Stage | Tmean (m) | Trim (m) | Dfwd (m) | Daft (m) | Dfwd Check | Daft Check | Freeboard (m) | Freeboard Check |
|-------|-----------|----------|----------|----------|------------|------------|---------------|-----------------|
| 5A-1  | 2.50      | 0.20     | 2.60     | 2.40     | OK         | OK         | 0.35          | OK              |
| 5A-2  | 2.70      | 0.22     | 2.81     | 2.59     | **FAIL**   | OK         | 0.28          | OK              |
| ...   | ...       | ...      | ...      | ...      | ...        | ...        | ...           | ...             |

**수식 예시:**

```excel
# Dfwd Check (G열)
=IF(D2<=2.7, "OK", "FAIL")

# Daft Check (H열)
=IF(E2<=2.7, "OK", "FAIL")

# Freeboard Check (J열)
=IF(I2>=0.28, "OK", "FAIL")
```

**Conditional Formatting:**
- "FAIL" → 빨간색 배경
- "OK" → 초록색 배경

---

## 🔍 검증 체크리스트

### ✅ P1 검증
- [ ] `Calc!D8` (D_vessel_m) = 3.65 m
- [ ] `Calc!D15` (MTC_t_m_per_cm) = 33.99
- [ ] `Calc!D17` (LCF_from_AP_m) Midship 기준 확인
- [ ] 파생 계산값들이 자동 업데이트됨

### ✅ P2 검증
- [ ] Stage 5A-2의 `Dfwd_m`이 수식 기반
- [ ] Stage 5A-2의 `Dfwd_m` ≤ 2.70 m
- [ ] 파일 내 값과 이전 메일 값 일치
- [ ] `Tmean`, `Trim_cm`이 상단 파라미터 참조

### ✅ P3 검증
- [ ] `X_Ballast_m`이 FWD 탱크 CG 반영
- [ ] "AFT ballast" 표현 제거됨
- [ ] 탱크 설명이 정확함 (FWB1/2, FWCARGO1 P/S)

### ✅ P4 검증
- [ ] `CAPTAIN_REPORT` 시트 존재
- [ ] 모든 Stage의 Draft Check 컬럼 추가
- [ ] Freeboard Check 컬럼 추가
- [ ] Conditional Formatting 적용
- [ ] 모든 Stage에서 Dfwd, Daft ≤ 2.70 m
- [ ] 모든 Stage에서 Freeboard ≥ 0.28 m

---

## 📊 최종 검증 스크립트

```python
# verify_captain_patches.py
from openpyxl import load_workbook

def verify_all_patches(filepath):
    wb = load_workbook(filepath)
    results = {
        'P1': False,
        'P2': False,
        'P3': False,
        'P4': False
    }
    
    # P1: Calc 시트 검증
    ws_calc = wb['Calc']
    if ws_calc['D8'].value == 3.65 and ws_calc['D15'].value == 33.99:
        results['P1'] = True
        print("✅ P1 PASS: Vessel particulars correct")
    else:
        print("❌ P1 FAIL: Check D_vessel and MTC values")
    
    # P2: Stage 5A-2 검증
    ws_roro = wb['RORO_Stage_Scenarios']
    # (Stage 5A-2 행 찾기 및 수식 검증 로직)
    
    # P3: X_Ballast 검증
    # (X_Ballast 값 확인 로직)
    
    # P4: CAPTAIN_REPORT 시트 존재 확인
    if 'CAPTAIN_REPORT' in wb.sheetnames:
        results['P4'] = True
        print("✅ P4 PASS: CAPTAIN_REPORT sheet created")
    else:
        print("❌ P4 FAIL: CAPTAIN_REPORT sheet missing")
    
    return results

# 실행
results = verify_all_patches('output/LCT_BUSHRA_AGI_TR_CAPTAIN_PATCHED.xlsx')
print(f"\n총 검증 결과: {sum(results.values())}/4 패치 완료")
```

---

## 📄 최종 리포트 생성

### PDF 리포트 생성
```bash
cd scripts\generate
python generate_captain_report_pdf.py --input ..\..\output\LCT_BUSHRA_AGI_TR_CAPTAIN_PATCHED.xlsx --output ..\..\output\reports\BUSHRA_Captain_Response_Report.pdf
```

### 제출 패키지 생성
```bash
python generate_submission_package.py --type captain_response --input ..\..\output\LCT_BUSHRA_AGI_TR_CAPTAIN_PATCHED.xlsx --output ..\..\output\submissions\Captain_Response_Package
```

---

## 📋 패치 완료 보고서 템플릿

```markdown
## Captain Mail Response - Patch Completion Report

**Date:** [현재 날짜]
**Patched By:** [담당자 이름]
**File Version:** LCT_BUSHRA_AGI_TR_CAPTAIN_PATCHED.xlsx
**Verification:** All checks passed

### ✅ Completed Patches

- [x] **P1**: Vessel particulars updated
  - D_vessel: 4.85m → 3.65m
  - MTC: 0.0 → 33.99 t·m/cm
  - LCF: Midship 기준 확인

- [x] **P2**: Stage 5A-2 draft calculation aligned
  - Dfwd: Formula-based (no hardcoded values)
  - Dfwd ≤ 2.70m: PASS
  - File vs Email consistency: VERIFIED

- [x] **P3**: X_Ballast recalculated
  - Based on FWD tanks CG: [계산값]
  - "AFT ballast" terminology: REMOVED
  - Tank description: CORRECTED

- [x] **P4**: CAPTAIN_REPORT sheet added
  - Draft limit checks: ALL OK
  - Freeboard checks: ALL OK
  - Conditional formatting: APPLIED

### 📊 Verification Results

| Verification Item | Status | Details |
|-------------------|--------|---------|
| All Stage drafts ≤ 2.70 m | ✅ PASS | Max draft: [값] m |
| Linkspan freeboard ≥ 0.28 m | ✅ PASS | Min freeboard: [값] m |
| Formula consistency | ✅ PASS | No hardcoded values |
| Tank CG alignment | ✅ PASS | X_Ballast: [값] m |

### 📎 Deliverables

1. **Patched Excel File**
   - Path: `output/LCT_BUSHRA_AGI_TR_CAPTAIN_PATCHED.xlsx`
   - Size: [파일 크기]
   - Sheets: [시트 개수]

2. **Captain Response PDF Report**
   - Path: `output/reports/BUSHRA_Captain_Response_Report.pdf`
   - Pages: [페이지 수]
   - Includes: All verification checks

3. **Verification Log**
   - Path: `output/logs/patch_verification_[timestamp].txt`
   - Timestamp: [시간]
   - Status: All checks passed

### 🎯 Next Steps

- [ ] **Project Manager Review**
  - Review date: [날짜]
  - Reviewer: [이름]
  - Status: Pending

- [ ] **Marine Engineer Approval**
  - Review date: [날짜]
  - Reviewer: [이름]
  - Status: Pending

- [ ] **Submit to Captain**
  - Submission date: [날짜]
  - Method: [Email/Portal]
  - Status: Pending

### 📝 Notes

[추가 메모 또는 특이사항]
```

---

## 🔗 참조 문서

- **captain.md**: 패치 이론 및 배경 설명
- **README.md**: 전체 프로젝트 개요
- **docs/TECHNICAL_DOCUMENTATION.md**: 기술 세부사항
- **docs/TANK_LEVER_ARM_GUIDE.md**: 탱크 계산 가이드

---

## 🆘 문제 해결

### 문제: "openpyxl 없음" 오류
```bash
pip install openpyxl==3.1.2
```

### 문제: Excel 파일이 열려 있음
```bash
# Excel을 닫고 재시도
# 또는 다른 파일명으로 저장
```

### 문제: Stage 5A-2를 찾을 수 없음
```python
# 수동으로 행 번호 확인
ws = wb['RORO_Stage_Scenarios']
for row in range(1, ws.max_row + 1):
    print(f"Row {row}: {ws.cell(row, 1).value}")
```

### 문제: 수식이 깨짐
- 원본 파일 백업에서 복원
- 수식을 수동으로 재입력

---

**패치 실행 준비 완료! 단계별로 진행하세요.** ✅
