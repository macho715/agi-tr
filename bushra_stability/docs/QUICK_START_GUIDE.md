# BUSHRA Stability Calculation - 빠른 시작 가이드

**Version:** 1.0  
**Last Updated:** 2025-11-20  
**대상:** 초보자부터 고급 사용자까지

---

## 목차

1. [프로젝트 소개](#1-프로젝트-소개)
2. [시작하기](#2-시작하기)
3. [기본 사용법](#3-기본-사용법)
4. [고급 기능](#4-고급-기능)
5. [실전 예제](#5-실전-예제)
6. [입력 파일 형식](#6-입력-파일-형식)
7. [출력 형식](#7-출력-형식)
8. [문제 해결](#8-문제-해결)
9. [FAQ](#9-faq)
10. [고급 활용](#10-고급-활용)

---

## 1. 프로젝트 소개

### 1.1 BUSHRA Stability Calculation이란?

BUSHRA Stability Calculation은 선박의 안정성 계산을 위한 Python 프로그램입니다. Excel 워크북 또는 CSV 파일을 입력으로 받아 다음과 같은 계산을 수행합니다:

- **Displacement 계산**: 총 배수량 및 무게 중심 계산
- **Stability 계산**: GZ 곡선, Trim, KG 보정 계산
- **IMO A.749 검증**: 국제해사기구 안정성 기준 자동 검증
- **Site별 검증**: DAS Island / AGI Site 운영 요구사항 검증

### 1.2 주요 특징

- ✅ **Excel 워크북 호환**: 기존 Excel 워크북과 100% 동일한 계산 결과
- ✅ **다양한 입력 형식**: Excel (.xls, .xlsx) 및 CSV 파일 지원
- ✅ **고급 Stability 계산**: Hydrostatic 보간, GZ 곡선, Trim 반복 계산
- ✅ **자동 검증**: IMO A.749 기준 및 Site별 요구사항 자동 검증
- ✅ **다양한 출력 형식**: JSON, CSV, Excel, PDF 리포트 지원
- ✅ **웹 UI**: Streamlit 기반 인터랙티브 인터페이스
- ✅ **Python API**: 프로그래밍 방식 사용 가능

### 1.3 사용 사례

- 선박 안정성 계산 및 검증
- RORO 작업 전 안정성 사전 검토
- IMO 기준 준수 확인
- Site별 운영 요구사항 검증
- 안정성 리포트 생성

---

## 2. 시작하기

### 2.1 시스템 요구사항

#### 필수 요구사항
- **Python**: 3.8 이상
- **운영체제**: Windows, Linux, macOS
- **메모리**: 최소 4GB RAM (대용량 파일 처리 시 8GB 권장)
- **디스크 공간**: 최소 500MB (Python 패키지 및 데이터 포함)

#### 권장 사양
- Python 3.9 이상
- 8GB 이상 RAM
- SSD 저장 장치 (파일 읽기/쓰기 성능 향상)

### 2.2 설치 방법

#### Step 1: Python 설치 확인

터미널(Windows: PowerShell 또는 CMD, Linux/macOS: Terminal)에서 다음 명령어를 실행하여 Python이 설치되어 있는지 확인합니다:

```bash
python --version
```

또는

```bash
python3 --version
```

**예상 출력:**
```
Python 3.9.7
```

Python이 설치되어 있지 않다면 [Python 공식 웹사이트](https://www.python.org/downloads/)에서 다운로드하여 설치하세요.

#### Step 2: 프로젝트 디렉토리로 이동

```bash
cd bushra_stability
```

**Windows 예시:**
```powershell
cd C:\Users\SAMSUNG\Downloads\EXCEL_GEN_03_MATHEMATICS_AND_DATA_FLOW\bushra_stability
```

**Linux/macOS 예시:**
```bash
cd ~/Downloads/EXCEL_GEN_03_MATHEMATICS_AND_DATA_FLOW/bushra_stability
```

#### Step 3: 가상 환경 생성 (권장)

가상 환경을 사용하면 프로젝트별로 패키지를 독립적으로 관리할 수 있습니다.

**Windows:**
```powershell
python -m venv venv
venv\Scripts\activate
```

**Linux/macOS:**
```bash
python3 -m venv venv
source venv/bin/activate
```

가상 환경이 활성화되면 터미널 프롬프트 앞에 `(venv)`가 표시됩니다.

#### Step 4: 의존성 패키지 설치

```bash
pip install -r requirements.txt
```

**설치되는 주요 패키지:**
- `pandas >= 2.0.0`: 데이터 처리
- `numpy >= 1.20.0`: 수치 계산
- `scipy >= 1.7.0`: 보간 및 적분 (Stability 계산 필수)
- `matplotlib >= 3.5.0`: 그래프 생성 (PDF 리포트용)
- `xlsxwriter >= 3.0.0`: Excel 리포트 생성
- `streamlit >= 1.28.0`: 웹 UI
- `xlrd >= 2.0.0`: Excel 파일 읽기 (.xls 형식)
- `openpyxl == 3.1.2`: Excel 파일 읽기/쓰기 (.xlsx 형식)

**설치 시간:** 약 2-5분 (인터넷 속도에 따라 다름)

#### Step 5: 설치 확인

설치가 완료되면 다음 명령어로 확인합니다:

```bash
python -m src.cli --help
```

**예상 출력:**
```
usage: cli.py [-h] [--sheet SHEET] [--output OUTPUT] [--format {json,csv,xlsx,pdf}] ...
BUSHRA Stability Calculation - Calculate displacement from Excel workbook
...
```

### 2.3 첫 실행 테스트

#### 테스트 1: 기본 Displacement 계산 (JSON 출력)

프로젝트에 예제 Excel 파일이 있다면 다음 명령어로 테스트할 수 있습니다:

```bash
python -m src.cli "path/to/workbook.xls" --sheet Volum --format json
```

**예상 출력:**
```json
{
  "total_weight": 1658.71,
  "lcg": 30.377,
  "vcg": 4.314,
  "tcg": 0.003,
  "total_fsm": 1000.25
}
```

#### 테스트 2: 도움말 확인

```bash
python -m src.cli --help
```

모든 사용 가능한 옵션과 인자가 표시됩니다.

---

## 3. 기본 사용법

### 3.1 Excel 파일로 Displacement 계산

#### 3.1.1 파일 준비

Excel 워크북 파일(.xls 또는 .xlsx)을 준비합니다. 파일에는 다음 시트가 있어야 합니다:

- **Volum 시트**: 무게 항목 데이터가 포함된 시트
  - Column H (7): Weight (t)
  - Column I (8): LCG (m)
  - Column K (10): VCG (m)
  - Column M (12): TCG (m)
  - Column Q (16): FSM (t·m)

#### 3.1.2 기본 명령어 실행

**JSON 출력 (기본):**
```bash
python -m src.cli "workbook.xls" --sheet Volum
```

**CSV 파일로 저장:**
```bash
python -m src.cli "workbook.xls" --sheet Volum --format csv --output result.csv
```

**다른 시트 이름 사용:**
```bash
python -m src.cli "workbook.xls" --sheet "Weight Items"
```

#### 3.1.3 결과 해석

**JSON 출력 예시:**
```json
{
  "total_weight": 1658.7092,
  "lcg": 30.376737,
  "vcg": 4.313906,
  "tcg": 0.003057,
  "total_fsm": 1000.25
}
```

**각 필드 의미:**
- `total_weight`: 총 배수량 (tons)
- `lcg`: 종방향 무게 중심 (Longitudinal Center of Gravity, meters)
- `vcg`: 수직 무게 중심 (Vertical Center of Gravity, meters)
- `tcg`: 횡방향 무게 중심 (Transverse Center of Gravity, meters)
- `total_fsm`: 총 자유 수면 모멘트 (Free Surface Moment, t·m)

### 3.2 CSV 파일로 계산

#### 3.2.1 CSV 모드 사용

CSV 모드를 사용하려면 다음 3개의 CSV 파일이 필요합니다:

1. **Master Tanks CSV**: 탱크 마스터 데이터
2. **Tank Mapping CSV**: Condition 이름과 Tank_ID 매핑
3. **Condition CSV**: Condition별 탱크 충전률

**명령어:**
```bash
python -m src.cli \
  --csv-mode \
  --master data/master_tanks.csv \
  --mapping data/tank_mapping.csv \
  --condition data/condition_001.csv \
  --format json \
  --output result.json
```

#### 3.2.2 CSV 파일 형식

**Master Tanks CSV 예시:**
```csv
Tank_ID,Type,Capacity_m3,SG_Master,LCG_m,VCG_m,TCG_m,FSM_full_tm,Content,Location
FWB1.P,FW,50.6,1.0,57.519,2.49,-2.379,74.26,FRESH WATER (SpGr 1.000),Fr.56~FE
FWB1.S,FW,50.6,1.0,57.519,2.49,2.379,74.26,FRESH WATER (SpGr 1.000),Fr.56~FE
```

**Tank Mapping CSV 예시:**
```csv
Condition_Name,Tank_ID
Condition_001,FWB1.P
Condition_001,FWB1.S
Condition_001,FWB2.P
```

**Condition CSV 예시:**
```csv
Condition_Name,Percent_Fill,SG_Override
Condition_001,100.0,
Condition_001,80.0,
```

### 3.3 결과 확인 방법

#### JSON 출력 확인

터미널에서 직접 확인하거나 파일로 저장하여 확인할 수 있습니다:

```bash
# 터미널에 출력
python -m src.cli "workbook.xls" --format json

# 파일로 저장
python -m src.cli "workbook.xls" --format json --output result.json
```

#### CSV 출력 확인

Excel이나 텍스트 에디터로 열어 확인할 수 있습니다:

```bash
python -m src.cli "workbook.xls" --format csv --output result.csv
```

**CSV 파일 내용 예시:**
```csv
Parameter,Value,Unit
Total Weight,1658.7092,t
LCG,30.376737,m
VCG,4.313906,m
TCG,0.003057,m
Total FSM,1000.25,t·m
```

---

## 4. 고급 기능

### 4.1 Stability 계산

Stability 계산을 수행하려면 Hydrostatic 데이터와 KN 테이블이 필요합니다.

#### 4.1.1 필수 파일 준비

1. **Hydrostatics CSV**: Hydrostatic 데이터
   - 컬럼: `Displacement`, `Trim`, `Draft`, `LCB`, `KMT`, `MTC`

2. **KN Table CSV**: KN 테이블 데이터
   - 컬럼: `Displacement`, `Trim`, `Heel_0`, `Heel_10`, `Heel_20`, ..., `Heel_60`

#### 4.1.2 Stability 계산 실행

```bash
python -m src.cli "workbook.xls" \
  --stability \
  --hydro data/hydrostatics.csv \
  --kn data/kn_table.csv \
  --format json \
  --output stability_result.json
```

#### 4.1.3 Stability 결과 해석

**JSON 출력 예시:**
```json
{
  "displacement": 1658.71,
  "lcg": 30.377,
  "vcg": 4.314,
  "tcg": 0.003,
  "total_fsm": 1000.25,
  "kg_corrected": 4.917,
  "kmt": 6.5,
  "gm": 1.583,
  "trim": 0.15,
  "draft_mean": 2.8,
  "draft_fwd": 2.725,
  "draft_aft": 2.875,
  "kn_curve": {
    "0": 0.0,
    "10": 1.2,
    "20": 2.4,
    "30": 3.5,
    "40": 4.0
  },
  "gz_curve": {
    "0": 0.0,
    "10": 0.8,
    "20": 1.6,
    "30": 2.3,
    "40": 2.5
  }
}
```

**주요 Stability 파라미터:**
- `kg_corrected`: FSM 보정된 KG (m)
- `kmt`: 횡방향 메타센터 높이 (Transverse Metacentric Height, m)
- `gm`: 메타센터 높이 (Metacentric Height, m) = KMT - KG
- `trim`: Trim (m, 양수 = 선미 깊음)
- `draft_mean`: 평균 Draft (m)
- `draft_fwd`: 선수 Draft (m)
- `draft_aft`: 선미 Draft (m)
- `kn_curve`: Heel 각도별 KN 값 (m)
- `gz_curve`: Heel 각도별 GZ 값 (m)

### 4.2 IMO A.749 검증

IMO A.749(18) 안정성 기준을 자동으로 검증합니다.

#### 4.2.1 IMO 검증 실행

```bash
python -m src.cli "workbook.xls" \
  --stability \
  --hydro data/hydrostatics.csv \
  --kn data/kn_table.csv \
  --imo-check \
  --format json \
  --output imo_check_result.json
```

#### 4.2.2 IMO 검증 기준

다음 7가지 기준을 모두 만족해야 통과합니다:

1. **GM >= 0.15 m**: 초기 안정성
2. **Area 0-30° >= 0.055 m·rad**: 정적 안정성
3. **Area 0-40° >= 0.090 m·rad**: 전체 안정성
4. **Area 30-40° >= 0.030 m·rad**: 후반 안정성
5. **GZ@30° >= 0.20 m**: 30도에서의 복원력
6. **GZmax >= 0.15 m**: 최대 복원력
7. **Angle@GZmax > 15°**: 최대 복원력 각도

#### 4.2.3 IMO 검증 결과 해석

**JSON 출력 예시:**
```json
{
  "imo_check": {
    "Overall_Pass": true,
    "Area_0_30_mrad": 0.085,
    "Area_0_40_mrad": 0.125,
    "Area_30_40_mrad": 0.040,
    "GZ_30deg_m": 0.25,
    "GZmax_m": 0.30,
    "Angle_GZmax_deg": 35.0,
    "GM_m": 1.583,
    "checks": {
      "gm_sufficient": {"pass": true, "value": 1.583, "limit": 0.15},
      "area_0_30": {"pass": true, "value": 0.085, "limit": 0.055},
      "area_0_40": {"pass": true, "value": 0.125, "limit": 0.090},
      "area_30_40": {"pass": true, "value": 0.040, "limit": 0.030},
      "gz_30deg": {"pass": true, "value": 0.25, "limit": 0.20},
      "gzmax": {"pass": true, "value": 0.30, "limit": 0.15},
      "angle_gzmax": {"pass": true, "value": 35.0, "limit": 15.0}
    }
  }
}
```

**결과 해석:**
- `Overall_Pass: true`: 모든 기준을 만족하여 통과
- 각 `checks` 항목의 `pass: true/false`로 개별 기준 통과 여부 확인 가능

### 4.3 Site별 검증 (DAS Island / AGI Site)

DAS Island 또는 AGI Site 운영을 위한 Site별 요구사항을 검증합니다.

#### 4.3.1 DAS Island 검증

```bash
python -m src.cli "workbook.xls" \
  --stability \
  --hydro data/hydrostatics.csv \
  --kn data/kn_table.csv \
  --site DAS \
  --site-validate \
  --format json \
  --output das_validation.json
```

#### 4.3.2 AGI Site 검증

```bash
python -m src.cli "workbook.xls" \
  --stability \
  --hydro data/hydrostatics.csv \
  --kn data/kn_table.csv \
  --site AGI \
  --site-validate \
  --format json \
  --output agi_validation.json
```

#### 4.3.3 Site별 체크리스트 생성

**DAS Island 체크리스트:**
```bash
python -m src.cli --site DAS --site-checklist
```

**AGI Site 체크리스트:**
```bash
python -m src.cli --site AGI --site-checklist
```

**출력 예시:**
```
======================================================================
RORO OPERATION CHECKLIST: DAS Island
======================================================================

📍 SITE INFORMATION
   Departure Port: Mina Zayed
   Arrival Jetty: DAS Jetty
   Site Code: DAS

📋 PRE-OPERATION REQUIREMENTS
   ☐ PTW submitted ≥48h before operation
   ☐ Hot Work restrictions confirmed
   ☐ Gate Pass obtained (ATLP + DAS Security Clearance)
   ☐ Valid for 24h
   ☐ Pilotage request submitted and confirmed
   ☐ Harbor Master approval obtained

⚓ OPERATIONAL LIMITS
   • Max Ramp Angle: ≤8.0°
   • Lashing Points: 12 points
   • Max Trim: ≤0.50m
   • Min GM: ≥0.15m

📸 DOCUMENTATION REQUIREMENTS
   ☐ Minimum 18 photos with GPS tags
   ☐ Incident report within 1h (if applicable)
   ☐ Final report within 7 days

✓ SITE-SPECIFIC CHECKS
   ☐ DAS Berth Load Chart
   ☐ DAS Pilotage Request Form
   ☐ DAS Security Clearance
   ☐ Ramp Angle Calculation (≤8°)
   ☐ 12-point Lashing with GPS photos

======================================================================
```

#### 4.3.4 Site별 검증 결과 해석

**JSON 출력 예시:**
```json
{
  "site_validation": {
    "trim_within_limit": {
      "pass": true,
      "value": 0.15,
      "limit": 0.50,
      "message": "Trim 0.150m OK limit 0.50m"
    },
    "gm_sufficient": {
      "pass": true,
      "value": 1.583,
      "limit": 0.15,
      "message": "GM 1.583m OK minimum 0.15m"
    },
    "drafts_positive": {
      "pass": true,
      "value": {
        "fwd": 2.725,
        "aft": 2.875,
        "mean": 2.8
      },
      "message": "Drafts OK"
    },
    "overall_pass": true
  },
  "site_name": "DAS Island",
  "site_type": "DAS"
}
```

---

## 5. 실전 예제

### 예제 1: 기본 Displacement 계산 (Excel)

**시나리오:** Excel 워크북에서 기본 Displacement를 계산하고 JSON으로 출력합니다.

**명령어:**
```bash
python -m src.cli "scripts/BUSHRA Stability_Calculation.xls" --sheet Volum --format json
```

**예상 출력:**
```json
{
  "total_weight": 1658.7092,
  "lcg": 30.376737,
  "vcg": 4.313906,
  "tcg": 0.003057,
  "total_fsm": 1000.25
}
```

**결과 해석:**
- 총 배수량: 1658.71 t
- 종방향 무게 중심: 30.38 m (선미 방향)
- 수직 무게 중심: 4.31 m
- 횡방향 무게 중심: 0.003 m (거의 중앙)
- 총 자유 수면 모멘트: 1000.25 t·m

### 예제 2: Stability 리포트 생성 (Excel + Hydrostatic)

**시나리오:** Excel 워크북과 Hydrostatic 데이터를 사용하여 전체 Stability 리포트를 생성합니다.

**명령어:**
```bash
python -m src.cli "scripts/BUSHRA Stability_Calculation.xls" \
  --stability \
  --hydro data/hydrostatics.csv \
  --kn data/kn_table.csv \
  --imo-check \
  --format xlsx \
  --output reports/stability_report_20251120.xlsx
```

**생성되는 Excel 리포트 구조:**
1. **Summary 시트**: 주요 파라미터 요약
2. **GZ_Curve 시트**: GZ 곡선 데이터 및 차트
3. **Weight_Items 시트**: 무게 항목 상세
4. **IMO_Check 시트**: IMO 검증 결과

**결과 확인:**
- Excel 파일이 `reports/stability_report_20251120.xlsx`에 생성됩니다.
- Excel에서 열어 각 시트를 확인할 수 있습니다.

### 예제 3: CSV 모드로 계산

**시나리오:** CSV 파일을 사용하여 Displacement를 계산합니다.

**명령어:**
```bash
python -m src.cli \
  --csv-mode \
  --master data/master_tanks.csv \
  --mapping data/tank_mapping.csv \
  --condition data/condition_001.csv \
  --format json \
  --output csv_result.json
```

**필수 파일:**
- `data/master_tanks.csv`: 탱크 마스터 데이터
- `data/tank_mapping.csv`: Condition-Tank 매핑
- `data/condition_001.csv`: Condition별 충전률

### 예제 4: Site별 검증 (DAS Island)

**시나리오:** DAS Island 운영을 위한 Stability 검증을 수행합니다.

**명령어:**
```bash
python -m src.cli "workbook.xls" \
  --stability \
  --hydro data/hydrostatics.csv \
  --kn data/kn_table.csv \
  --site DAS \
  --site-validate \
  --imo-check \
  --format xlsx \
  --output das_stability_report.xlsx
```

**검증 항목:**
- Trim ≤ 0.50 m
- GM ≥ 0.15 m (IMO 최소값)
- Draft 양수 확인
- DAS Island 특화 요구사항

### 예제 5: Streamlit 웹 UI 사용

**시나리오:** 웹 브라우저를 통해 인터랙티브하게 계산을 수행합니다.

**명령어:**
```bash
python scripts/run_streamlit.py
```

또는

```bash
streamlit run src/streamlit_app.py
```

**사용 방법:**
1. 브라우저가 자동으로 열립니다 (기본: http://localhost:8501)
2. 사이드바에서 입력 모드 선택:
   - **Excel Workbook**: Excel 파일 업로드
   - **CSV Files**: CSV 파일들 업로드
3. Stability 계산 활성화 (선택):
   - "Enable Stability Calculation" 체크
   - Hydrostatics CSV, KN Table CSV 업로드
   - "IMO A.749 Check" 체크 (선택)
4. 결과 확인:
   - 메인 화면에 결과 표시
   - 리포트 다운로드 버튼 클릭 (JSON, CSV, Excel, PDF)

**장점:**
- 파일 드래그 앤 드롭 지원
- 실시간 결과 확인
- 그래프 시각화
- 리포트 다운로드

### 예제 6: Python API 사용

**시나리오:** Python 스크립트에서 직접 API를 사용하여 계산을 수행합니다.

**Python 스크립트 예시:**
```python
from src.displacement import WeightItem, calculate_displacement
from src.stability import calculate_stability
from src.hydrostatic import HydroEngine

# 무게 항목 생성
items = [
    WeightItem(name="Light Ship", weight=770.16, lcg=26.35, vcg=3.88, tcg=0.0, fsm=0.0),
    WeightItem(name="Fuel Oil", weight=100.0, lcg=20.0, vcg=2.0, tcg=0.0, fsm=5.0),
    WeightItem(name="Ballast", weight=200.0, lcg=50.0, vcg=1.5, tcg=0.0, fsm=10.0),
]

# 기본 displacement 계산
result = calculate_displacement(items)
print(f"Displacement: {result.total_weight} t")
print(f"LCG: {result.lcg} m")
print(f"VCG: {result.vcg} m")

# Stability 계산 (hydrostatic 데이터 필요)
hydro = HydroEngine("data/hydrostatics.csv", "data/kn_table.csv")
stability_result = calculate_stability(items, hydro)
print(f"GM: {stability_result.gm} m")
print(f"Trim: {stability_result.trim} m")
print(f"GZ@30°: {stability_result.gz_curve[30]} m")
```

**실행:**
```bash
python my_script.py
```

---

## 6. 입력 파일 형식

### 6.1 Excel 워크북 형식

#### 6.1.1 시트 구조

Excel 워크북에는 다음 시트가 있어야 합니다:

- **Volum 시트** (또는 사용자 지정 시트 이름): 무게 항목 데이터

#### 6.1.2 컬럼 위치 및 의미

**Volum 시트 데이터 구조:**

| 컬럼 | 인덱스 | 의미 | 단위 | 필수 |
|------|--------|------|------|------|
| Description | C (2) | 항목 설명 | - | 예 |
| Weight | H (7) | 무게 | t | 예 |
| LCG | I (8) | 종방향 무게 중심 | m | 예 |
| VCG | K (10) | 수직 무게 중심 | m | 예 |
| TCG | M (12) | 횡방향 무게 중심 | m | 예 |
| FSM | Q (16) | 자유 수면 모멘트 | t·m | 아니오 |

**참고:**
- 컬럼 인덱스는 0부터 시작 (A=0, B=1, C=2, ..., H=7, I=8, K=10, M=12, Q=16)
- 그룹 헤더 행은 무게가 없으면 자동으로 그룹으로 인식됩니다.

#### 6.1.3 데이터 형식

**예시 데이터:**
```
Row 10: LIGHT SHIP (그룹 헤더)
Row 11: Light Ship | 770.16 | 26.35 | 3.88 | 0.0 | 0.0
Row 12: Crew + Effects | 11.0 | 5.5 | 8.174 | 0.0 | 0.0
Row 20: FUEL OIL (그룹 헤더)
Row 21: DAILY OIL TANK (P) | 0.82 | 11.251 | 2.825 | -6.247 | 0.34
```

### 6.2 CSV 파일 형식

#### 6.2.1 Master Tanks CSV

**파일명:** `master_tanks.csv`

**필수 컬럼:**
- `Tank_ID`: 탱크 식별자 (예: "FWB1.P", "FWB1.S")
- `Capacity_m3`: 탱크 용량 (m³)
- `SG_Master`: 비중 (Master 값)
- `LCG_m` 또는 `LCG`: 종방향 무게 중심 (m)
- `VCG_m` 또는 `VCG`: 수직 무게 중심 (m)
- `TCG_m` 또는 `TCG`: 횡방향 무게 중심 (m)
- `FSM_full_tm`: 만충 시 자유 수면 모멘트 (t·m)

**선택 컬럼:**
- `Type`: 탱크 타입 (예: "FW", "FUEL", "SW")
- `Content`: 내용물 설명
- `Location`: 위치 정보

**예시:**
```csv
Tank_ID,Type,Capacity_m3,SG_Master,LCG_m,VCG_m,TCG_m,FSM_full_tm,Content,Location
FWB1.P,FW,50.6,1.0,57.519,2.49,-2.379,74.26,FRESH WATER (SpGr 1.000),Fr.56~FE
FWB1.S,FW,50.6,1.0,57.519,2.49,2.379,74.26,FRESH WATER (SpGr 1.000),Fr.56~FE
FWB2.P,FW,110.0,1.0,50.038,2.059,-4.368,72.01,FRESH WATER (SpGr 1.000),Fr.48~53
```

#### 6.2.2 Tank Mapping CSV

**파일명:** `tank_mapping.csv`

**필수 컬럼:**
- `Condition_Name`: Condition 이름 (예: "Condition_001")
- `Tank_ID`: 탱크 식별자

**예시:**
```csv
Condition_Name,Tank_ID
Condition_001,FWB1.P
Condition_001,FWB1.S
Condition_001,FWB2.P
Condition_001,FWB2.S
```

#### 6.2.3 Condition CSV

**파일명:** `condition_*.csv` (예: `condition_001.csv`)

**필수 컬럼:**
- `Condition_Name`: Condition 이름
- `Percent_Fill`: 충전률 (0.0-100.0)

**선택 컬럼:**
- `SG_Override`: 비중 오버라이드 (비워두면 Master 값 사용)

**예시:**
```csv
Condition_Name,Percent_Fill,SG_Override
Condition_001,100.0,
Condition_001,80.0,
```

#### 6.2.4 Hydrostatics CSV

**파일명:** `hydrostatics.csv`

**필수 컬럼:**
- `Displacement`: 배수량 (t)
- `Trim`: Trim (m, 양수 = 선미 깊음)
- `Draft`: Draft (m)
- `LCB`: 종방향 부력 중심 (Longitudinal Center of Buoyancy, m)
- `KMT`: 횡방향 메타센터 높이 (Transverse Metacentric Height, m)
- `MTC`: Trim 변경 모멘트 (Moment to Change Trim, t·m/cm)

**예시:**
```csv
Displacement,Trim,Draft,LCB,KMT,MTC
1000,0.0,2.0,10.0,5.0,100.0
1000,1.0,2.1,10.1,5.1,101.0
1500,0.0,2.5,10.5,5.5,150.0
1500,1.0,2.6,10.6,5.6,151.0
```

**참고:**
- 데이터는 Displacement와 Trim의 조합으로 정렬되어야 합니다.
- 보간을 위해 충분한 데이터 포인트가 필요합니다 (최소 4-6개 포인트 권장).

#### 6.2.5 KN Table CSV

**파일명:** `kn_table.csv`

**필수 컬럼:**
- `Displacement`: 배수량 (t)
- `Trim`: Trim (m)
- `Heel_0`, `Heel_10`, `Heel_20`, `Heel_30`, `Heel_40`, `Heel_50`, `Heel_60`: 각 Heel 각도별 KN 값 (m)

**예시:**
```csv
Displacement,Trim,Heel_0,Heel_10,Heel_20,Heel_30,Heel_40,Heel_50,Heel_60
1000,0.0,0.0,1.0,2.0,3.0,3.5,3.0,2.0
1000,1.0,0.0,1.1,2.1,3.1,3.6,3.1,2.1
1500,0.0,0.0,1.2,2.4,3.6,4.2,3.8,2.5
```

**참고:**
- Heel 각도는 0도부터 60도까지 10도 간격으로 제공됩니다.
- 데이터는 Displacement와 Trim의 조합으로 정렬되어야 합니다.

---

## 7. 출력 형식

### 7.1 JSON 출력

**기본 Displacement 계산:**
```json
{
  "total_weight": 1658.7092,
  "lcg": 30.376737,
  "vcg": 4.313906,
  "tcg": 0.003057,
  "total_fsm": 1000.25
}
```

**Stability 계산 (IMO 검증 포함):**
```json
{
  "displacement": 1658.71,
  "lcg": 30.377,
  "vcg": 4.314,
  "tcg": 0.003,
  "total_fsm": 1000.25,
  "kg_corrected": 4.917,
  "kmt": 6.5,
  "gm": 1.583,
  "trim": 0.15,
  "draft_mean": 2.8,
  "draft_fwd": 2.725,
  "draft_aft": 2.875,
  "lcb": 30.5,
  "mtc": 33.99,
  "kn_curve": {
    "0": 0.0,
    "10": 1.2,
    "20": 2.4,
    "30": 3.5,
    "40": 4.0,
    "50": 3.8,
    "60": 2.5
  },
  "gz_curve": {
    "0": 0.0,
    "10": 0.8,
    "20": 1.6,
    "30": 2.3,
    "40": 2.5,
    "50": 2.2,
    "60": 1.3
  },
  "imo_check": {
    "Overall_Pass": true,
    "Area_0_30_mrad": 0.085,
    "Area_0_40_mrad": 0.125,
    "Area_30_40_mrad": 0.040,
    "GZ_30deg_m": 0.25,
    "GZmax_m": 0.30,
    "Angle_GZmax_deg": 35.0,
    "GM_m": 1.583
  }
}
```

### 7.2 CSV 출력

**기본 Displacement 계산:**
```csv
Parameter,Value,Unit
Total Weight,1658.7092,t
LCG,30.376737,m
VCG,4.313906,m
TCG,0.003057,m
Total FSM,1000.25,t·m
```

**참고:** Stability 계산 결과는 CSV 형식으로 출력할 수 없습니다. JSON, Excel, 또는 PDF 형식을 사용하세요.

### 7.3 Excel 리포트

**시트 구성:**

1. **Summary 시트**
   - Displacement 파라미터
   - Stability 파라미터
   - IMO 검증 결과 요약

2. **GZ_Curve 시트**
   - Heel 각도별 GZ 값 테이블
   - GZ 곡선 차트 (matplotlib 생성)

3. **Weight_Items 시트**
   - 모든 무게 항목 상세 정보
   - 그룹별 집계

4. **IMO_Check 시트** (IMO 검증 수행 시)
   - IMO A.749 검증 결과 상세
   - 각 기준별 통과/실패 상태

**생성 명령어:**
```bash
python -m src.cli "workbook.xls" \
  --stability \
  --hydro data/hydrostatics.csv \
  --kn data/kn_table.csv \
  --imo-check \
  --format xlsx \
  --output report.xlsx
```

### 7.4 PDF 리포트

**페이지 구성:**

1. **요약 페이지**
   - 모든 파라미터 요약
   - IMO 검증 결과
   - 주요 안정성 지표

2. **GZ 곡선 페이지**
   - GZ 곡선 플롯 (matplotlib 생성)
   - Heel 각도별 GZ 값 테이블

**생성 명령어:**
```bash
python -m src.cli "workbook.xls" \
  --stability \
  --hydro data/hydrostatics.csv \
  --kn data/kn_table.csv \
  --imo-check \
  --format pdf \
  --output report.pdf
```

**참고:** PDF 리포트 생성에는 `matplotlib` 패키지가 필요합니다.

---

## 8. 문제 해결

### 8.1 일반적인 오류 및 해결법

#### 오류 1: "File not found"

**증상:**
```
Error: File not found: workbook.xls
```

**원인:**
- 파일 경로가 잘못되었거나 파일이 존재하지 않음

**해결법:**
1. 파일 경로 확인:
   ```bash
   # Windows
   dir "workbook.xls"
   
   # Linux/macOS
   ls workbook.xls
   ```

2. 절대 경로 사용:
   ```bash
   python -m src.cli "C:\Users\SAMSUNG\Downloads\workbook.xls" --sheet Volum
   ```

3. 상대 경로 확인:
   - 현재 디렉토리에서 파일까지의 상대 경로 확인
   - 예: `python -m src.cli "data/workbook.xls" --sheet Volum`

#### 오류 2: "No weight items found"

**증상:**
```
Error: No weight items found
```

**원인:**
- 시트 이름이 잘못되었거나 데이터 형식이 맞지 않음

**해결법:**
1. 시트 이름 확인:
   ```bash
   # Excel에서 시트 이름 확인 후
   python -m src.cli "workbook.xls" --sheet "올바른시트이름"
   ```

2. 데이터 형식 확인:
   - Column H (7): Weight 값이 숫자 형식인지 확인
   - Column I (8): LCG 값이 숫자 형식인지 확인
   - 빈 행이나 헤더 행이 올바르게 처리되는지 확인

3. Excel 파일 열어서 데이터 확인:
   - Volum 시트의 데이터 구조 확인
   - Weight 컬럼에 유효한 숫자 값이 있는지 확인

#### 오류 3: "scipy is required for stability calculations"

**증상:**
```
Error: scipy is required for stability calculations
```

**원인:**
- `scipy` 패키지가 설치되지 않음

**해결법:**
```bash
pip install scipy
```

또는

```bash
pip install -r requirements.txt
```

#### 오류 4: "Missing column in CSV"

**증상:**
```
Error: Missing column 'LCG_m' in CSV file
```

**원인:**
- CSV 파일에 필수 컬럼이 없거나 컬럼 이름이 다름

**해결법:**
1. CSV 파일 열어서 컬럼 이름 확인
2. 필수 컬럼이 있는지 확인:
   - Master Tanks CSV: `Tank_ID`, `LCG_m` (또는 `LCG`), `VCG_m` (또는 `VCG`), `TCG_m` (또는 `TCG`)
   - Hydrostatics CSV: `Displacement`, `Trim`, `Draft`, `LCB`, `KMT`, `MTC`
   - KN Table CSV: `Displacement`, `Trim`, `Heel_0`, `Heel_10`, ..., `Heel_60`

3. 컬럼 이름 수정 또는 매핑 파일 사용

#### 오류 5: "PermissionError" (Windows)

**증상:**
```
PermissionError: [Errno 13] Permission denied: 'output.xlsx'
```

**원인:**
- 출력 파일이 다른 프로그램(예: Excel)에서 열려 있음

**해결법:**
1. Excel에서 파일 닫기
2. 다른 출력 파일명 사용:
   ```bash
   python -m src.cli "workbook.xls" --output "output_new.xlsx"
   ```

### 8.2 파일 형식 문제

#### Excel 파일이 열리지 않음

**원인:**
- `.xls` 형식 파일이 손상되었거나 호환성 문제

**해결법:**
1. Excel에서 파일을 열어서 `.xlsx` 형식으로 저장
2. `xlrd` 패키지 버전 확인:
   ```bash
   pip install xlrd==2.0.1
   ```

#### CSV 파일 인코딩 문제

**증상:**
- 한글이 깨져서 표시됨

**해결법:**
1. CSV 파일을 UTF-8 인코딩으로 저장
2. Excel에서 저장 시 "CSV UTF-8 (쉼표로 분리)" 형식 선택

### 8.3 성능 최적화 팁

#### 대용량 Excel 파일 처리

**문제:**
- Excel 파일이 크면 처리 시간이 오래 걸림

**해결법:**
1. CSV 모드 사용:
   ```bash
   python -m src.cli --csv-mode --master master.csv --mapping mapping.csv --condition condition.csv
   ```

2. 필요한 데이터만 포함된 시트 사용

#### 반복 계산 시 성능

**문제:**
- 여러 Condition을 반복 계산할 때 시간이 오래 걸림

**해결법:**
1. CLI 사용 (Streamlit보다 빠름):
   ```bash
   # 배치 스크립트 작성
   for condition in condition_*.csv; do
     python -m src.cli --csv-mode --master master.csv --mapping mapping.csv --condition "$condition" --output "result_${condition}.json"
   done
   ```

2. Python API 사용하여 스크립트 작성:
   ```python
   from src.displacement import calculate_displacement
   from src.csv_reader import csv_to_weight_items
   
   for condition_file in condition_files:
       items = csv_to_weight_items(master, mapping, condition_file)
       result = calculate_displacement(items)
       # 결과 저장
   ```

---

## 9. FAQ

### Q1: Excel 워크북과 Python 계산 결과가 다릅니다.

**A:** 다음을 확인하세요:

1. **시트 이름 확인:**
   - `--sheet` 옵션으로 올바른 시트 이름 지정
   - 기본값은 "Volum"입니다.

2. **데이터 범위 확인:**
   - Excel에서 실제 데이터가 있는 행 범위 확인
   - 빈 행이나 헤더 행이 올바르게 처리되는지 확인

3. **컬럼 위치 확인:**
   - Weight: Column H (7)
   - LCG: Column I (8)
   - VCG: Column K (10)
   - TCG: Column M (12)
   - FSM: Column Q (16)

4. **숫자 형식 확인:**
   - Excel에서 숫자가 텍스트로 저장되지 않았는지 확인
   - 쉼표(,)가 포함된 숫자는 제거

### Q2: Stability 계산이 실패합니다.

**A:** 다음을 확인하세요:

1. **필수 파일 확인:**
   - `--hydro` 옵션으로 Hydrostatics CSV 파일 지정
   - `--kn` 옵션으로 KN Table CSV 파일 지정

2. **데이터 범위 확인:**
   - Hydrostatics CSV에 충분한 데이터 포인트가 있는지 확인 (최소 4-6개 권장)
   - 계산하려는 Displacement와 Trim 값이 데이터 범위 내에 있는지 확인

3. **scipy 패키지 확인:**
   ```bash
   pip install scipy
   ```

### Q3: IMO 검증이 실패합니다.

**A:** 다음을 확인하세요:

1. **GM 값 확인:**
   - GM >= 0.15 m이어야 합니다.
   - GM이 너무 낮으면 Ballast를 추가하거나 무게 분배를 조정하세요.

2. **GZ 곡선 확인:**
   - GZ@30° >= 0.20 m
   - GZmax >= 0.15 m
   - GZ 곡선이 충분히 큰 Area를 가지는지 확인

3. **상세 결과 확인:**
   - JSON 출력에서 `imo_check.checks` 항목을 확인하여 어떤 기준이 실패했는지 확인

### Q4: Site별 검증이 실패합니다.

**A:** 다음을 확인하세요:

1. **Site 코드 확인:**
   - `--site DAS` 또는 `--site AGI` 올바르게 지정

2. **검증 기준 확인:**
   - DAS Island: Trim ≤ 0.50 m, GM ≥ 0.15 m
   - AGI Site: Trim ≤ 0.50 m, GM ≥ 0.15 m

3. **체크리스트 확인:**
   ```bash
   python -m src.cli --site DAS --site-checklist
   ```
   - 사전 요구사항이 모두 충족되었는지 확인

### Q5: Streamlit 웹 UI가 실행되지 않습니다.

**A:** 다음을 확인하세요:

1. **Streamlit 패키지 확인:**
   ```bash
   pip install streamlit
   ```

2. **포트 충돌 확인:**
   - 기본 포트 8501이 사용 중이면 다른 포트 사용:
   ```bash
   streamlit run src/streamlit_app.py --server.port 8502
   ```

3. **Python 경로 확인:**
   - `scripts/run_streamlit.py` 스크립트 사용 권장

### Q6: PDF 리포트가 생성되지 않습니다.

**A:** 다음을 확인하세요:

1. **matplotlib 패키지 확인:**
   ```bash
   pip install matplotlib
   ```

2. **파일 권한 확인:**
   - 출력 디렉토리에 쓰기 권한이 있는지 확인

3. **파일 경로 확인:**
   - 출력 파일 경로가 올바른지 확인

---

## 10. 고급 활용

### 10.1 Python API 사용

#### 기본 Displacement 계산

```python
from src.displacement import WeightItem, calculate_displacement

# 무게 항목 생성
items = [
    WeightItem(name="Light Ship", weight=770.16, lcg=26.35, vcg=3.88, tcg=0.0, fsm=0.0),
    WeightItem(name="Fuel Oil", weight=100.0, lcg=20.0, vcg=2.0, tcg=0.0, fsm=5.0),
]

# 계산
result = calculate_displacement(items)
print(f"Displacement: {result.total_weight} t")
print(f"LCG: {result.lcg} m")
```

#### Stability 계산

```python
from src.stability import calculate_stability
from src.hydrostatic import HydroEngine

# Hydrostatic 엔진 초기화
hydro = HydroEngine("data/hydrostatics.csv", "data/kn_table.csv")

# Stability 계산
stability_result = calculate_stability(items, hydro)
print(f"GM: {stability_result.gm} m")
print(f"Trim: {stability_result.trim} m")
print(f"GZ@30°: {stability_result.gz_curve[30]} m")
```

#### IMO 검증

```python
from src.imo_check import check_imo_a749

# IMO 검증
heel_angles = list(stability_result.gz_curve.keys())
gz_values = list(stability_result.gz_curve.values())
imo_check = check_imo_a749(heel_angles, gz_values, stability_result.gm)

print(f"IMO Overall Pass: {imo_check['Overall_Pass']}")
```

#### Site별 검증

```python
from src.site_config import SiteRequirements, validate_stability_for_site

# DAS Island 요구사항
site_req = SiteRequirements.from_site_code("DAS")

# 검증
site_validation = validate_stability_for_site(stability_result, site_req, verbose=True)
print(f"Site Validation Pass: {site_validation['overall_pass']}")
```

### 10.2 배치 처리

#### 여러 Condition 일괄 계산

**Python 스크립트 예시:**
```python
from pathlib import Path
from src.cli import main
import sys

# Condition 파일 목록
condition_files = [
    "data/condition_001.csv",
    "data/condition_002.csv",
    "data/condition_003.csv",
]

# 각 Condition에 대해 계산
for condition_file in condition_files:
    condition_name = Path(condition_file).stem
    output_file = f"results/{condition_name}_result.json"
    
    args = [
        "--csv-mode",
        "--master", "data/master_tanks.csv",
        "--mapping", "data/tank_mapping.csv",
        "--condition", condition_file,
        "--format", "json",
        "--output", output_file,
    ]
    
    result = main(args)
    if result != 0:
        print(f"Error processing {condition_file}")
        sys.exit(1)
    
    print(f"Completed: {condition_name} -> {output_file}")
```

**실행:**
```bash
python batch_process.py
```

### 10.3 자동화 스크립트 작성

#### Excel 파일 모니터링 및 자동 계산

**Python 스크립트 예시:**
```python
import time
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from src.cli import main

class ExcelHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if event.src_path.endswith('.xls') or event.src_path.endswith('.xlsx'):
            print(f"Processing: {event.src_path}")
            output_file = Path(event.src_path).with_suffix('.json')
            args = [
                event.src_path,
                "--format", "json",
                "--output", str(output_file),
            ]
            main(args)

if __name__ == "__main__":
    path = Path("watch_folder")
    event_handler = ExcelHandler()
    observer = Observer()
    observer.schedule(event_handler, str(path), recursive=False)
    observer.start()
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
```

**참고:** `watchdog` 패키지 설치 필요:
```bash
pip install watchdog
```

---

## 부록

### A. 명령어 옵션 전체 목록

```bash
python -m src.cli --help
```

**주요 옵션:**
- `excel_file`: Excel 워크북 파일 경로
- `--sheet SHEET`: 시트 이름 (기본: "Volum")
- `--output OUTPUT`: 출력 파일 경로
- `--format {json,csv,xlsx,pdf}`: 출력 형식 (기본: json)
- `--stability`: Stability 계산 활성화
- `--hydro HYDRO`: Hydrostatics CSV 파일 경로
- `--kn KN`: KN Table CSV 파일 경로
- `--imo-check`: IMO A.749 검증 수행
- `--csv-mode`: CSV 입력 모드 사용
- `--master MASTER`: Master Tanks CSV 파일 경로
- `--mapping MAPPING`: Tank Mapping CSV 파일 경로
- `--condition CONDITION`: Condition CSV 파일 경로
- `--site {DAS,AGI}`: Site 코드 지정
- `--site-validate`: Site별 검증 수행
- `--site-checklist`: Site별 체크리스트 생성

### B. 프로젝트 구조

```
bushra_stability/
├── README.md                    # 프로젝트 개요
├── requirements.txt             # 의존성 패키지
├── src/                         # 소스 코드
│   ├── __init__.py
│   ├── cli.py                   # CLI 인터페이스
│   ├── displacement.py          # Displacement 계산
│   ├── excel_reader.py          # Excel 파일 읽기
│   ├── csv_reader.py            # CSV 파일 읽기
│   ├── stability.py             # Stability 계산
│   ├── hydrostatic.py           # Hydrostatic 보간
│   ├── imo_check.py             # IMO 검증
│   ├── reporting.py             # 리포트 생성
│   ├── site_config.py           # Site별 설정
│   └── streamlit_app.py         # 웹 UI
├── tests/                       # 테스트 파일
│   ├── test_displacement.py
│   ├── test_stability.py
│   ├── test_hydrostatic.py
│   └── test_imo_check.py
├── scripts/                     # 실행 스크립트
│   └── run_streamlit.py
├── data/                        # 데이터 파일
│   ├── master_tanks.csv
│   └── master_tanks.json
└── docs/                        # 문서
    ├── USER_GUIDE.md
    ├── TECHNICAL_ARCHITECTURE.md
    ├── QUICK_START_GUIDE.md     # 이 문서
    └── ...
```

### C. 추가 리소스

- **기술 문서**: `docs/TECHNICAL_ARCHITECTURE.md`
- **사용자 가이드**: `docs/USER_GUIDE.md`
- **통합 설계**: `docs/INTEGRATION_DESIGN.md`
- **구현 상태**: `docs/IMPLEMENTATION.md`

### D. 지원 및 문의

문제가 발생하거나 질문이 있으면:
1. 이 가이드의 [문제 해결](#8-문제-해결) 섹션 확인
2. [FAQ](#9-faq) 섹션 확인
3. 프로젝트 이슈 등록 또는 문서 참조

---

**문서 버전:** 1.0  
**최종 업데이트:** 2025-11-20  
**작성자:** MACHO-GPT v3.4-mini

---

**END OF QUICK START GUIDE**

