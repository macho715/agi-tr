# Scripts 폴더 사용 가이드

## 📁 폴더 구조

```
scripts/
├── main/                    # 메인 프로덕션 스크립트
│   ├── build_bushra_gateab_v4_hybrid.py      # v4 HYBRID Excel 생성 (권장)
│   ├── build_bushra_v4_standalone.py         # v4 독립 실행 버전
│   ├── build_bushra_agi_tr_from_scratch_patched.py  # AGI TR Excel 재생성 (최신 패치)
│   └── bushra_operations.py                  # 통합 운영 스크립트
│
├── generate/                # 리포트/패키지 생성
│   ├── generate_height_report_pdf.py         # PDF 리포트 생성
│   ├── generate_vessel_sketch.py             # 선박 측면도 스케치
│   ├── generate_mammoet_package.py           # Mammoet 제출 패키지
│   ├── generate_submission_package.py        # Harbor Master 제출 패키지
│   └── generate_mammoet_submission.py        # 통합 실행 (스케치 + PDF)
│
├── extract/                 # 데이터 추출
│   ├── extract_vessel_depth_from_pdf.py      # PDF에서 D-vessel 추출
│   ├── extract_stage_data_from_pdf.py        # PDF에서 Stage 데이터 추출
│   └── extract_gateab_tide_data.py           # GateAB v3에서 조수 데이터 추출
│
├── utils/                   # 유틸리티
│   ├── pdf_to_excel_converter.py             # PDF → Excel 변환
│   ├── update_stage_values.py                # Stage 값 업데이트
│   └── PATCH1106.py                          # FWD/AFT 리포트 생성
│
├── special/                 # 특수 기능
│   └── patch4.py                             # 탱크 레버암 밸러스트 계산
│
├── docs/                    # 문서
│   ├── coordinate_reference.md               # PDF 좌표 참조
│   └── 함수.patch                            # 수식 패치 가이드
│
└── archive/                 # 구버전 보관
    ├── old_build/           # 구버전 빌드 스크립트
    ├── patches/             # 구버전 패치 (v4에 통합됨)
    ├── verification/        # 검증 스크립트 (검증 완료)
    └── output/              # 구버전 Excel 출력 파일
```

## 🚀 주요 사용 방법

### 1. Excel 파일 생성 (권장)

**v4 HYBRID 버전 (최신, 권장):**
```bash
cd scripts/main
python build_bushra_gateab_v4_hybrid.py
```
- 출력: `../output/LCT_BUSHRA_GateAB_v4_HYBRID.xlsx`
- 특징: v4 표준 + GateAB v3 통합, 한글 시트, 실제 조수 데이터

**v4 Standalone 버전 (JSON 의존성 없음):**
```bash
cd scripts/main
python build_bushra_v4_standalone.py
```
- 출력: `LCT_BUSHRA_GateAB_v4_HYBRID_generated.xlsx` (현재 폴더)
- 특징: JSON 의존성 없음, 독립 실행

**AGI TR 재생성 (LCT_BUSHRA_AGI_TR.xlsx):**
```bash
cd scripts/main
python build_bushra_agi_tr_from_scratch_patched.py
```
- 출력: `../output/LCT_BUSHRA_AGI_TR_from_scratch.xlsx`
- 특징: 원본 파일 구조를 프로그래밍 방식으로 재생성

### 2. 통합 운영

```bash
cd scripts/main
python bushra_operations.py --help

# 주요 옵션:
python bushra_operations.py --patch          # Stage_Heights 시트 패치
python bushra_operations.py --validate       # 기본 검증
python bushra_operations.py --comprehensive  # 종합 검증
python bushra_operations.py --analyze        # 실시간 분석
```

### 3. 리포트 생성

**Mammoet 제출 패키지:**
```bash
cd scripts/generate
python generate_mammoet_submission.py
```

**개별 생성:**
```bash
cd scripts/generate
python generate_height_report_pdf.py    # PDF 리포트
python generate_vessel_sketch.py        # 선박 스케치
python generate_mammoet_package.py      # Mammoet 패키지
python generate_submission_package.py   # Harbor Master 패키지
```

### 4. 데이터 추출

```bash
cd scripts/extract
python extract_vessel_depth_from_pdf.py    # D-vessel 추출
python extract_stage_data_from_pdf.py      # Stage 데이터 추출
python extract_gateab_tide_data.py         # 조수 데이터 추출
```

### 5. 유틸리티

```bash
cd scripts/utils
python pdf_to_excel_converter.py    # PDF → Excel 변환
python update_stage_values.py       # Stage 값 업데이트
python PATCH1106.py                 # FWD/AFT 리포트 생성
```

## 📋 파일 경로 참조

### 입력 파일 (Excel)
- **v4 HYBRID**: `../output/LCT_BUSHRA_GateAB_v4_HYBRID.xlsx`
- **v4 Standalone**: `LCT_BUSHRA_GateAB_v4_HYBRID_generated.xlsx`

### 출력 파일
- Excel: `../output/LCT_BUSHRA_GateAB_v4_HYBRID.xlsx`
- PDF: `../output/LCT_BUSHRA_Height_Report.pdf`
- 스케치: `../output/vessel_sketch_*.png`

### 데이터 파일
- 조수 데이터: `../data/gateab_v3_tide_data.json` (선택적)

## ⚠️ 중요 사항

1. **KminusZ (K-Z) 값**: Excel 생성 후 반드시 `Calc!D10`에 현장 실측값 입력 필요
2. **조수 데이터**: `December_Tide_2025` 시트에 744개 조수 값 입력 필요
3. **파일 경로**: 스크립트 실행 시 현재 디렉토리 확인 필요

## 🔄 버전 정보

- **v4 HYBRID**: 최신 버전, 프로덕션 권장
- **v4 Standalone**: JSON 의존성 없는 독립 버전
- **구버전**: `archive/` 폴더에 보관 (참고용)

## 📝 변경 이력

- 2025-11-18: 프로젝트 전체 파일 정리 완료
  - AGI TR 빌드 스크립트를 `scripts/main/`으로 이동
  - 구버전 파일들을 `archive/` 폴더로 정리
  - Excel 백업 파일들을 `archive/excel_backups/`로 정리
- 2025-11-12: 폴더 구조 재구성, v4 경로로 업데이트
- 2025-11-06: v4 HYBRID 버전 출시
- 2025-11-06: 구버전 패치들 v4에 통합

