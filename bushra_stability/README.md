# BUSHRA Stability Calculation

Python implementation of the BUSHRA Stability Calculation Excel workbook with advanced stability analysis capabilities.

## 주요 기능

- ✅ **기본 Displacement 계산**: Excel 워크북에서 무게 항목 읽기 및 집계
- ✅ **고급 Stability 계산**: GZ 곡선, Trim, KG 보정
- ✅ **Hydrostatic 보간**: 2D/3D 보간 (SciPy 기반)
- ✅ **IMO A.749 검증**: 안정성 기준 자동 검증
- ✅ **리포트 생성**: JSON, CSV, Excel, PDF 형식 지원
- ✅ **CSV 입력 지원**: Master tanks, Condition 파일 지원
- ✅ **웹 UI**: Streamlit 기반 인터랙티브 인터페이스
- 🆕 **Site Configuration**: DAS Island / AGI Site 구분 지원
- 🆕 **Site Validation**: 사이트별 운영 요구사항 자동 검증
- 🆕 **Enhanced Trim**: 향상된 Trim 계산 안정성 및 수렴 검증

## 설치

### 필수 요구사항
- Python 3.8 이상

### 설치 방법

```bash
# 저장소 클론 또는 다운로드
cd bushra_stability

# 의존성 설치
pip install -r requirements.txt
```

## 빠른 시작

### 1. 기본 Displacement 계산

```bash
# Excel 파일에서 displacement 계산
python -m src.cli scripts/BUSHRA\ Stability_Calculation.xls --sheet Volum
```

### 2. 고급 Stability 계산

```bash
# Stability 계산 + IMO 검증 + Excel 리포트
python -m src.cli scripts/BUSHRA\ Stability_Calculation.xls \
  --stability \
  --hydro hydrostatics.csv \
  --kn kn_table.csv \
  --imo-check \
  --format xlsx \
  --output stability_report.xlsx
```

### 3. Streamlit 웹 UI

```bash
python scripts/run_streamlit.py
```

### 4. 사이트별 검증 (DAS Island / AGI Site)

```bash
# DAS Island 운영 체크리스트 생성
python -m src.cli --site DAS --site-checklist

# AGI Site 운영 체크리스트 생성
python -m src.cli --site AGI --site-checklist

# DAS Island 기준 Stability 검증
python -m src.cli "workbook.xls" \
  --stability \
  --hydro hydrostatics.csv \
  --kn kn_table.csv \
  --imo-check \
  --site DAS \
  --site-validate \
  --format xlsx \
  --output das_stability_report.xlsx

# AGI Site 기준 Stability 검증
python -m src.cli "workbook.xls" \
  --stability \
  --hydro hydrostatics.csv \
  --kn kn_table.csv \
  --site AGI \
  --site-validate \
  --output agi_report.json
```

## 사용 방법

### CLI 사용

#### 기본 Displacement 계산
```bash
# JSON 출력
python -m src.cli "path/to/workbook.xls" --format json

# CSV 출력
python -m src.cli "path/to/workbook.xls" --format csv --output results.csv
```

#### 고급 Stability 계산
```bash
# Stability 계산 (hydrostatic 데이터 필요)
python -m src.cli "path/to/workbook.xls" \
  --stability \
  --hydro hydrostatics.csv \
  --kn kn_table.csv \
  --imo-check \
  --format xlsx \
  --output report.xlsx
```

#### CSV 입력 모드
```bash
# CSV 파일로부터 계산
python -m src.cli \
  --csv-mode \
  --master master_tanks.csv \
  --mapping tank_mapping.csv \
  --condition condition_001.csv \
  --stability \
  --hydro hydrostatics.csv \
  --kn kn_table.csv
```

### Python API 사용

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

# Stability 계산
hydro = HydroEngine("hydrostatics.csv", "kn_table.csv")
stability_result = calculate_stability(items, hydro)
print(f"GM: {stability_result.gm} m")
print(f"GZ@30°: {stability_result.gz_curve[30]} m")
```

## 테스트

```bash
# 모든 테스트 실행
python -m pytest tests/ -v

# 특정 테스트 실행
python -m pytest tests/test_displacement.py -v
python -m pytest tests/test_stability.py -v
python -m pytest tests/test_hydrostatic.py -v
python -m pytest tests/test_imo_check.py -v
```

## 프로젝트 구조

```
bushra_stability/
├── README.md               # 프로젝트 개요 및 사용 가이드
├── requirements.txt        # 의존성 패키지
├── BUSHRA_report_1659t.xlsx # 예제 리포트 파일
├── src/                    # 소스 코드
│   ├── __init__.py
│   ├── displacement.py     # 기본 displacement 계산
│   ├── excel_reader.py     # Excel 워크북 읽기
│   ├── csv_reader.py       # CSV 파일 읽기
│   ├── hydrostatic.py      # Hydrostatic 보간 엔진
│   ├── stability.py        # GZ/Trim 계산
│   ├── imo_check.py        # IMO A.749 검증
│   ├── reporting.py        # 리포트 생성
│   ├── cli.py              # CLI 인터페이스
│   └── streamlit_app.py    # 웹 UI
├── tests/                  # 테스트 파일
│   ├── test_displacement.py
│   ├── test_stability.py
│   ├── test_hydrostatic.py
│   └── test_imo_check.py
├── docs/                   # 문서
│   ├── IMPLEMENTATION.md
│   ├── TECHNICAL_ARCHITECTURE.md
│   ├── INTEGRATION_DESIGN.md
│   ├── USER_GUIDE.md
│   └── PATCH_NOTES.md      # 패치 노트 (참고용)
└── scripts/                # 실행 스크립트
    └── run_streamlit.py
```

## 문서

- **[사용자 가이드](docs/USER_GUIDE.md)**: 상세한 사용 방법 및 예제
- **[기술 문서](docs/TECHNICAL_ARCHITECTURE.md)**: 아키텍처 및 알고리즘 설명
- **[통합 설계](docs/INTEGRATION_DESIGN.md)**: 시스템 통합 설계 문서
- **[구현 상태](docs/IMPLEMENTATION.md)**: 구현 상태 및 검증 결과
- **[패치 노트](docs/PATCH_NOTES.md)**: 통합 작업 시 패치 내용 (참고용)
- **[PDF 데이터 요구사항](docs/PDF_DATA_REQUIREMENTS.md)**: PDF에서 추출해야 할 데이터 체크리스트

## 주요 특징

### 모듈화 설계
- 각 기능이 독립적인 모듈로 분리
- 선택적 기능 지원 (scipy 없이도 기본 기능 동작)
- 하위 호환성 유지

### 정확한 계산
- Excel 워크북과의 일치성 검증
- SciPy 기반 고정밀 보간
- IMO 기준 준수

### 다양한 인터페이스
- CLI: 배치 처리 및 자동화
- Streamlit UI: 인터랙티브 웹 인터페이스
- Python API: 프로그래밍 방식 사용

## 라이선스

이 프로젝트는 내부 사용을 위한 것입니다.

## 기여

버그 리포트나 기능 제안은 이슈로 등록해주세요.

