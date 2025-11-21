# 탱크 데이터 관리 가이드

## 개요

이 문서는 `Tank Capacity_Plan.xlsx` 파일을 기준으로 표준 `master_tanks.csv` 파일을 생성하고 관리하는 방법을 설명합니다.

## 파일 구조

```
프로젝트 루트/
├── Tank Capacity_Plan.xlsx          # 원본 Excel 파일 (정확한 데이터 소스)
├── bushra_stability/
│   └── data/
│       └── master_tanks.csv         # 표준 탱크 데이터 (생성된 파일)
└── scripts/
    └── tools/
        ├── create_master_tanks_from_excel.py  # Excel → CSV 변환 스크립트
        ├── compare_tank_data.py               # 데이터 비교 스크립트
        ├── analyze_tank_capacity_plan.py      # 분석 스크립트
        └── README.md                          # 도구 설명
```

## 데이터 소스

- **원본 파일**: `Tank Capacity_Plan.xlsx`
  - 이 파일이 정확한 데이터 소스입니다
  - 31개의 탱크 데이터 포함
  - LCG, VCG, TCG, Capacity, SG, FSM 정보 포함

- **생성된 파일**: `bushra_stability/data/master_tanks.csv`
  - 표준 형식의 탱크 데이터
  - bushra_stability 코드에서 사용

## 사용 방법

### 1. master_tanks.csv 생성

Excel 파일을 기준으로 표준 CSV 파일을 생성합니다:

```bash
python scripts/tools/create_master_tanks_from_excel.py
```

**출력**:
- `bushra_stability/data/master_tanks.csv`

**검증**:
- 필수 컬럼 확인
- 데이터 타입 검증
- 누락 데이터 확인

### 2. 탱크 데이터 비교

Excel 기준 master_tanks.csv와 scripts/special의 탱크 데이터를 비교합니다:

```bash
python scripts/tools/compare_tank_data.py
```

**비교 항목**:
- 탱크 ID 일치 여부
- LCG, VCG, TCG 값 비교
- Capacity, SG 값 비교
- 차이점 보고

### 3. 탱크 데이터 분석

Excel 파일을 분석합니다:

```bash
python scripts/tools/analyze_tank_capacity_plan.py
```

**분석 내용**:
- 데이터 구조 분석
- LCG/TCG 값 파싱 (f, p, s 접미사 처리)
- 표준 CSV 형식으로 변환
- 기존 코드베이스와 비교

## master_tanks.csv 형식

### 필수 컬럼

- `Tank_ID`: 탱크 식별자
- `Capacity_m3`: 탱크 용량 (m³)
- `SG_Master`: 비중 (Specific Gravity)
- `LCG_m`: 종방향 무게중심 (m)
- `VCG_m`: 수직 무게중심 (m)
- `TCG_m`: 횡방향 무게중심 (m)
- `FSM_full_tm`: 자유수면 모멘트 (t·m)

### 선택 컬럼

- `Content`: 탱크 내용물 (예: "FRESH WATER (SpGr 1.000)")
- `Location`: 탱크 위치 (예: "Fr.6~21")

## 데이터 검증

### 자동 검증

스크립트 실행 시 자동으로 다음을 검증합니다:

1. **필수 컬럼 확인**: 모든 필수 컬럼이 존재하는지 확인
2. **데이터 타입 검증**: 숫자 컬럼이 올바른 타입인지 확인
3. **누락 데이터 확인**: 필수 값이 누락되지 않았는지 확인
4. **값 범위 검증**: 합리적인 값 범위 내에 있는지 확인

### 수동 검증

생성된 CSV 파일을 직접 확인:

```python
import pandas as pd

df = pd.read_csv('bushra_stability/data/master_tanks.csv')
print(df.head())
print(df.info())
print(df.describe())
```

## 데이터 업데이트

### Excel 파일 수정 시

1. `Tank Capacity_Plan.xlsx` 파일을 수정
2. 스크립트를 재실행:
   ```bash
   python scripts/tools/create_master_tanks_from_excel.py
   ```
3. 생성된 CSV 파일 검증
4. bushra_stability 코드에서 사용

### 주의사항

- **원본 Excel 파일이 정확한 데이터 소스입니다**
- CSV 파일을 직접 수정하지 마세요
- Excel 파일을 수정하고 스크립트를 재실행하세요

## 탱크 데이터 통계

### 전체 통계

- **총 탱크 수**: 31개
- **평균 용량**: 59.35 m³
- **최대 용량**: 178.0 m³ (LRFO.P/S)
- **최소 용량**: 2.3 m³ (VOIDDB4.P)
- **평균 SG**: 0.965

### 탱크 종류

1. **Fuel Oil (SpGr 0.870)**: 9개
   - DO.P, DO.S, FODB1.C, FODB1.P, FODB1.S, FOW1.P, FOW1.S, LRFO.P, LRFO.S

2. **Fresh Water (SpGr 1.000)**: 10개
   - FW1.P, FW1.S, FW2.P, FW2.S, FWB1.P, FWB1.S, FWB2.P, FWB2.S, FWCARGO1.P, FWCARGO1.S, FWCARGO2.P, FWCARGO2.S

3. **Salt Water (SpGr 1.025)**: 11개
   - CL.P, CL.S, VOID3.P, VOID3.S, VOIDDB1.C, VOIDDB2.C, VOIDDB4.P, VOIDDB4.S

4. **기타**: 2개
   - SLUDGE.C, SEWAGE.P

## 문제 해결

### 스크립트 실행 오류

1. **파일을 찾을 수 없음**:
   - `Tank Capacity_Plan.xlsx` 파일이 프로젝트 루트에 있는지 확인
   - 파일 경로를 확인

2. **Import 오류**:
   - 필요한 패키지 설치: `pip install pandas openpyxl`
   - Python 경로 확인

3. **데이터 파싱 오류**:
   - Excel 파일 형식 확인
   - 컬럼명 확인

### 데이터 불일치

1. **Excel과 CSV 값이 다름**:
   - Excel 파일을 다시 확인
   - 스크립트를 재실행

2. **scripts/special과 값이 다름**:
   - Excel 파일이 정확한 데이터 소스입니다
   - scripts/special의 값을 Excel 기준으로 업데이트

## 참고 자료

- `bushra_stability/src/csv_reader.py`: CSV 파일 읽기 모듈
- `bushra_stability/docs/USER_GUIDE.md`: 사용자 가이드
- `scripts/tools/README.md`: 도구 설명

## 업데이트 이력

- 2025-01-XX: 초기 문서 작성
- 2025-01-XX: Tank Capacity_Plan.xlsx 기준 master_tanks.csv 생성
- 2025-01-XX: 파일 정리 및 문서화

