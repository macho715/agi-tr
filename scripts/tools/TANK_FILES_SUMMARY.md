# 탱크 관련 파일 정리 요약

## ✅ 완료된 작업

### 1. 파일 정리
- ✅ 탱크 관련 스크립트를 `scripts/tools/`로 이동
- ✅ 임시 파일 삭제 (`master_tanks_from_capacity_plan.csv`)
- ✅ 정리 스크립트 삭제 (`organize_tank_files.py`)

### 2. 파일 구조

```
프로젝트 루트/
├── Tank Capacity_Plan.xlsx          # 원본 Excel 파일 (정확한 데이터 소스)
├── bushra_stability/
│   └── data/
│       └── master_tanks.csv         # 표준 탱크 데이터 (31개 탱크)
└── scripts/
    └── tools/
        ├── create_master_tanks_from_excel.py  # Excel → CSV 변환
        ├── compare_tank_data.py               # 데이터 비교
        ├── analyze_tank_capacity_plan.py      # 데이터 분석
        └── README.md                          # 도구 설명
```

### 3. 생성된 파일

- ✅ `bushra_stability/data/master_tanks.csv`: 표준 탱크 데이터
- ✅ `scripts/tools/README.md`: 도구 설명
- ✅ `docs/TANK_DATA_MANAGEMENT.md`: 상세 가이드

## 📋 파일 목록

### 스크립트 파일

1. **create_master_tanks_from_excel.py**
   - 목적: Excel 파일을 표준 CSV로 변환
   - 사용법: `python scripts/tools/create_master_tanks_from_excel.py`
   - 출력: `bushra_stability/data/master_tanks.csv`

2. **compare_tank_data.py**
   - 목적: Excel 기준 CSV와 scripts/special 데이터 비교
   - 사용법: `python scripts/tools/compare_tank_data.py`

3. **analyze_tank_capacity_plan.py**
   - 목적: Excel 파일 분석 및 파싱
   - 사용법: `python scripts/tools/analyze_tank_capacity_plan.py`

### 데이터 파일

1. **Tank Capacity_Plan.xlsx**
   - 위치: 프로젝트 루트
   - 내용: 31개 탱크 데이터 (정확한 데이터 소스)
   - 상태: ✅ 유지

2. **master_tanks.csv**
   - 위치: `bushra_stability/data/`
   - 내용: 표준 형식의 탱크 데이터
   - 상태: ✅ 생성 완료

## 🔍 데이터 검증

### 검증 완료 항목

- ✅ 필수 컬럼 존재 (Tank_ID, Capacity_m3, SG_Master, LCG_m, VCG_m, TCG_m, FSM_full_tm)
- ✅ 데이터 타입 정확
- ✅ 누락 데이터 없음
- ✅ 값 범위 합리적

### 데이터 통계

- 총 탱크 수: 31개
- 평균 용량: 59.35 m³
- 최대 용량: 178.0 m³
- 최소 용량: 2.3 m³
- 평균 SG: 0.965

## 📖 사용 방법

### master_tanks.csv 생성

```bash
python scripts/tools/create_master_tanks_from_excel.py
```

### 데이터 비교

```bash
python scripts/tools/compare_tank_data.py
```

### 데이터 분석

```bash
python scripts/tools/analyze_tank_capacity_plan.py
```

## ⚠️ 주의사항

1. **원본 Excel 파일이 정확한 데이터 소스입니다**
   - `Tank Capacity_Plan.xlsx` 파일을 수정하면 스크립트를 재실행하세요
   - CSV 파일을 직접 수정하지 마세요

2. **파일 경로**
   - 모든 스크립트는 프로젝트 루트에서 실행해야 합니다
   - 상대 경로는 프로젝트 루트 기준입니다

3. **데이터 업데이트**
   - Excel 파일을 수정한 후 스크립트를 재실행하세요
   - 생성된 CSV 파일을 검증하세요

## 📚 관련 문서

- `docs/TANK_DATA_MANAGEMENT.md`: 상세 가이드
- `scripts/tools/README.md`: 도구 설명
- `bushra_stability/docs/USER_GUIDE.md`: 사용자 가이드

## 🎯 다음 단계

1. ✅ master_tanks.csv 생성 완료
2. ⏳ tank_mapping.csv 파일 생성 (필요 시)
3. ⏳ condition_*.csv 파일 생성 (필요 시)
4. ⏳ bushra_stability 코드에서 사용

## 업데이트 이력

- 2025-01-XX: 파일 정리 완료
- 2025-01-XX: master_tanks.csv 생성
- 2025-01-XX: 문서화 완료

