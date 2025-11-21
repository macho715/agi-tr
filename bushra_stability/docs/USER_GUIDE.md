# BUSHRA Stability Calculation - 사용자 가이드

## 개요

BUSHRA Stability Calculation은 선박의 안정성 계산을 위한 Python 프로그램입니다. Excel 워크북 또는 CSV 파일을 입력으로 받아 displacement, GZ 곡선, Trim, IMO A.749 검증 등을 수행합니다.

## 주요 기능

### 1. 기본 Displacement 계산
- Excel 워크북에서 무게 항목 읽기
- LCG, VCG, TCG, FSM 집계
- 총 displacement 계산

### 2. 고급 Stability 계산
- Hydrostatic 데이터 보간 (2D/3D)
- GZ 곡선 계산
- Trim 반복 계산
- KG 보정 (FSM 포함)

### 3. IMO A.749 검증
- 안정성 기준 자동 검증
- Area 계산 (Simpson 적분)
- GZ@30°, GZmax 검증

### 4. 리포트 생성
- JSON/CSV 출력
- Excel 리포트 (차트 포함)
- PDF 리포트 (GZ 곡선 플롯)

## 설치

### 필수 요구사항
- Python 3.8 이상
- pip

### 설치 방법

```bash
# 저장소 클론 또는 다운로드
cd bushra_stability

# 의존성 설치
pip install -r requirements.txt
```

### 의존성 패키지
- `pandas >= 2.0.0`: 데이터 처리
- `numpy >= 1.20.0`: 수치 계산
- `scipy >= 1.7.0`: 보간 및 적분
- `matplotlib >= 3.5.0`: 플롯 생성
- `xlsxwriter >= 3.0.0`: Excel 리포트
- `streamlit >= 1.28.0`: 웹 UI
- `xlrd >= 2.0.0`: Excel 읽기
- `openpyxl == 3.1.2`: Excel 읽기/쓰기

## 사용 방법

### CLI 사용

#### 1. 기본 Displacement 계산 (Excel)

```bash
python -m src.cli scripts/BUSHRA\ Stability_Calculation.xls --sheet Volum
```

**출력 예시:**
```json
{
  "total_weight": 1658.71,
  "lcg": 30.377,
  "vcg": 4.314,
  "tcg": 0.003,
  "total_fsm": 1000.25
}
```

#### 2. CSV 파일로 저장

```bash
python -m src.cli scripts/BUSHRA\ Stability_Calculation.xls --format csv --output result.csv
```

#### 3. 고급 Stability 계산

```bash
python -m src.cli scripts/BUSHRA\ Stability_Calculation.xls \
  --stability \
  --hydro hydrostatics.csv \
  --kn kn_table.csv \
  --imo-check \
  --format xlsx \
  --output stability_report.xlsx
```

**필수 파일:**
- `hydrostatics.csv`: Hydrostatic 데이터 (Displacement, Trim, Draft, LCB, KMT, MTC)
- `kn_table.csv`: KN 테이블 (Displacement, Trim, Heel_0, Heel_10, ..., Heel_60)

#### 4. CSV 입력 모드

```bash
python -m src.cli \
  --csv-mode \
  --master master_tanks.csv \
  --mapping tank_mapping.csv \
  --condition condition_001.csv \
  --stability \
  --hydro hydrostatics.csv \
  --kn kn_table.csv \
  --format pdf \
  --output report.pdf
```

### Streamlit 웹 UI 사용

#### 실행

```bash
python scripts/run_streamlit.py
```

또는

```bash
streamlit run src/streamlit_app.py
```

#### 사용 방법

1. **Excel 모드**
   - 사이드바에서 "Excel Workbook" 선택
   - Excel 파일 업로드
   - Sheet 이름 입력 (기본: "Volum")
   - 결과 자동 표시

2. **CSV 모드**
   - 사이드바에서 "CSV Files" 선택
   - Master Tanks CSV, Tank Mapping CSV, Condition CSV 업로드
   - 결과 자동 표시

3. **Stability 계산 활성화**
   - "Enable Stability Calculation" 체크
   - Hydrostatics CSV, KN Table CSV 업로드
   - "IMO A.749 Check" 체크 (선택)
   - GZ 곡선 및 IMO 검증 결과 표시

4. **리포트 다운로드**
   - JSON, CSV, Excel, PDF 형식 지원
   - 다운로드 버튼 클릭

## 입력 파일 형식

### Excel 워크북

**필수 시트:**
- `Volum`: 무게 항목 데이터

**데이터 구조:**
- Column H (7): Weight (t)
- Column I (8): LCG (m)
- Column K (10): VCG (m)
- Column M (12): TCG (m)
- Column Q (16): FSM (t·m)

### CSV 파일 형식

#### 1. Master Tanks CSV

```csv
Tank_ID,Content,Capacity_m3,SG_Master,LCG_m,VCG_m,TCG_m,FSM_full_tm
T001,Fuel Oil,50.0,0.821,20.0,2.0,0.0,100.0
T002,Fresh Water,30.0,1.000,30.0,4.0,0.0,50.0
```

#### 2. Tank Mapping CSV

```csv
Condition_Name,Tank_ID
Condition_001,T001
Condition_001,T002
```

#### 3. Condition CSV

```csv
Condition_Name,Percent_Fill,SG_Override
Condition_001,80.0,
Condition_001,50.0,
```

#### 4. Hydrostatics CSV

```csv
Displacement,Trim,Draft,LCB,KMT,MTC
1000,0.0,2.0,10.0,5.0,100.0
1000,1.0,2.1,10.1,5.1,101.0
1500,0.0,2.5,10.5,5.5,150.0
```

#### 5. KN Table CSV

```csv
Displacement,Trim,Heel_0,Heel_10,Heel_20,Heel_30,Heel_40,Heel_50,Heel_60
1000,0.0,0.0,1.0,2.0,3.0,3.5,3.0,2.0
1000,1.0,0.0,1.1,2.1,3.1,3.6,3.1,2.1
```

## 출력 형식

### JSON

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
  },
  "imo_check": {
    "Overall_Pass": true,
    "Area_0_30_mrad": 0.085,
    "Area_0_40_mrad": 0.125,
    "GZ_30deg_m": 0.25,
    "GZmax_m": 0.30
  }
}
```

### Excel 리포트

**시트 구성:**
1. **Summary**: 주요 파라미터 요약
2. **GZ_Curve**: GZ 곡선 데이터 및 차트
3. **Weight_Items**: 무게 항목 상세

### PDF 리포트

**페이지 구성:**
1. **요약 페이지**: 모든 파라미터 및 IMO 검증 결과
2. **GZ 곡선 페이지**: GZ 곡선 플롯

## IMO A.749 검증 기준

다음 기준을 모두 만족해야 통과:

1. **GM >= 0.15 m**: 초기 안정성
2. **Area 0-30° >= 0.055 m·rad**: 정적 안정성
3. **Area 0-40° >= 0.090 m·rad**: 전체 안정성
4. **Area 30-40° >= 0.030 m·rad**: 후반 안정성
5. **GZ@30° >= 0.20 m**: 30도에서의 복원력
6. **GZmax >= 0.15 m**: 최대 복원력
7. **Angle@GZmax > 15°**: 최대 복원력 각도

## 문제 해결

### 일반적인 오류

#### 1. "File not found"
- 파일 경로 확인
- 상대 경로 대신 절대 경로 사용

#### 2. "No weight items found"
- Excel 시트 이름 확인
- 데이터 형식 확인

#### 3. "scipy is required for stability calculations"
- `pip install scipy` 실행

#### 4. "Missing column in CSV"
- CSV 파일 형식 확인
- 필수 컬럼 존재 확인

### 성능 최적화

- 대용량 Excel 파일: CSV 모드 사용 권장
- 반복 계산: CLI 사용 (Streamlit보다 빠름)

## 예제

### 예제 1: 기본 Displacement 계산

```bash
# Excel 파일에서 displacement 계산
python -m src.cli scripts/BUSHRA\ Stability_Calculation.xls --sheet Volum --format json
```

### 예제 2: 전체 Stability 리포트 생성

```bash
# Stability 계산 + IMO 검증 + Excel 리포트
python -m src.cli scripts/BUSHRA\ Stability_Calculation.xls \
  --stability \
  --hydro data/hydrostatics.csv \
  --kn data/kn_table.csv \
  --imo-check \
  --format xlsx \
  --output reports/stability_report_$(date +%Y%m%d).xlsx
```

### 예제 3: Python API 사용

```python
from src.displacement import WeightItem, calculate_displacement
from src.stability import calculate_stability
from src.hydrostatic import HydroEngine

# 무게 항목 생성
items = [
    WeightItem(name="Light Ship", weight=770.16, lcg=26.35, vcg=3.88, tcg=0.0, fsm=0.0),
    WeightItem(name="Fuel Oil", weight=100.0, lcg=20.0, vcg=2.0, tcg=0.0, fsm=5.0),
]

# 기본 displacement 계산
result = calculate_displacement(items)
print(f"Displacement: {result.total_weight} t")
print(f"LCG: {result.lcg} m")

# Stability 계산 (hydrostatic 데이터 필요)
hydro = HydroEngine("hydrostatics.csv", "kn_table.csv")
stability_result = calculate_stability(items, hydro)
print(f"GM: {stability_result.gm} m")
print(f"GZ@30°: {stability_result.gz_curve[30]} m")
```

## 추가 리소스

- **기술 문서**: `docs/TECHNICAL_ARCHITECTURE.md`
- **통합 설계**: `docs/INTEGRATION_DESIGN.md`
- **구현 상태**: `docs/IMPLEMENTATION.md`

## 지원

문제가 발생하거나 질문이 있으면 이슈를 등록하거나 문서를 참조하세요.

