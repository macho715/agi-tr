# LCT BUSHRA - RORO Calculator & Ballast System

**프로젝트명:** Independent Subsea HVDC – AGI Transformers (TM63)
**선박:** LCT BUSHRA
**부두:** Mina Zayed RORO Jetty
**목적:** AGI Transformer 운송을 위한 선박 계산 및 안정성 분석 통합 시스템

---

## 📋 프로젝트 개요

이 프로젝트는 LCT BUSHRA 선박의 RORO 하역 작업 시 안전한 선수/선미 Draft 계산, 밸러스트 계산, 안정성 분석을 위한 통합 시스템입니다. Excel 기반 계산기, Python 안정성 분석 모듈, 리포트 생성 시스템으로 구성되어 있습니다.

### 주요 성과

- ✅ **RORO Calculator v4 HYBRID**: 744시간 조수 분석, Ramp Angle 계산 (≤6° 제한)
- ✅ **탱크 레버암 밸러스트 시스템**: 정확한 밸러스트 계산 (37% 절감)
- ✅ **안정성 계산 모듈**: IMO A.749 검증, GZ 곡선 분석
- ✅ **Stage 4/6/7 브리지**: Python ↔ Excel ↔ JSON 완전한 데이터 루프
- ✅ **자동화 리포트 생성**: PDF 리포트, 제출 패키지 자동 생성

---

## 🎯 주요 시스템 구성 요소

### 1. RORO Calculator (v4 HYBRID)

**목적:** RORO 하역 작업 시 안전한 Draft 및 Ramp Angle 계산

**핵심 기능:**
- FWD/AFT Draft 계산 (744시간 조수 데이터 기반)
- Ramp Angle 계산 (Harbour Master 승인 한계 ≤6° 준수)
- Stage별 시나리오 분석
- 최근접 매칭 (±30분) 드롭다운 기능
- 자동 검증 테스트 (Formula_Test 시트)

**메인 파일:**
- `output/LCT_BUSHRA_GateAB_v4_HYBRID_with_Dropdown.xlsx`

**문서:**
- 사용자 가이드: [`docs/USER_GUIDE.md`](docs/USER_GUIDE.md)
- 기술 문서: [`docs/TECHNICAL_DOCUMENTATION.md`](docs/TECHNICAL_DOCUMENTATION.md)
- 문서 인덱스: [`docs/README.md`](docs/README.md)

---

### 2. 탱크 레버암 밸러스트 시스템

**목적:** 정확한 레버암 기반 밸러스트 계산

**핵심 기능:**
- 11개 탱크 데이터베이스 (실제 안정성 계산서 기반)
- AP 기준 → Midship 기준 자동 좌표 변환
- 정확한 레버암(L_b) 계산
- 단계별 RORO 밸러스트 계산
- 시나리오별 탱크 선택 가이드

**주요 개선점:**
- Patch 3 (근사식): Ballast ≈ 750t
- Patch 4 (정확): Ballast = 469t
- **절감: 281t (37%)**

**문서:**
- [`docs/TANK_LEVER_ARM_GUIDE.md`](docs/TANK_LEVER_ARM_GUIDE.md)

---

### 3. 안정성 계산 모듈 (bushra_stability/)

**목적:** Python 기반 선박 안정성 분석 시스템

**핵심 기능:**
- 기본 Displacement 계산
- 고급 Stability 계산 (GZ 곡선, Trim, KG 보정)
- Hydrostatic 보간 (2D/3D, SciPy 기반)
- IMO A.749 검증 (안정성 기준 자동 검증)
- Site별 검증 (DAS Island / AGI Site)
- 리포트 생성 (JSON, CSV, Excel, PDF)
- CLI 및 Streamlit 웹 UI

**문서:**
- [`bushra_stability/README.md`](bushra_stability/README.md)
- 기술 아키텍처: [`bushra_stability/docs/TECHNICAL_ARCHITECTURE.md`](bushra_stability/docs/TECHNICAL_ARCHITECTURE.md)

---

### 4. Stage 4/6/7 브리지 시스템 (stage_4_6_7_bridge/)

**목적:** Python ↔ Excel ↔ Stability JSON 완전한 데이터 루프 구축

**핵심 기능:**
- Excel RORO 시트에서 Stage 4/6/7 Trim 값 읽기
- JSON 설정 파일 생성 및 업데이트
- Stage_Tanks 시트 생성 및 채우기
- JSON → Excel 변환 (탱크 좌표, 계획, 합계, Ballast 계산)
- Excel → JSON 검증

**주요 파일:**
- 브리지 모듈: `bushra_excel_bridge_v1.py` (루트)
- 설정 파일: `stage_config_sample_4_7.json`
- 출력 파일: `bushra_stability_export.xlsx`

**문서:**
- [`stage_4_6_7_bridge/README.md`](stage_4_6_7_bridge/README.md)

---

### 5. 리포트 생성 시스템 (scripts/generate/)

**목적:** 제출용 리포트 및 패키지 자동 생성

**핵심 기능:**
- PDF 리포트 생성 (FWD/AFT Report)
- Mammoet 제출 패키지 생성
- Harbor Master 제출 패키지 생성
- 선박 측면도 스케치 생성
- 제출 체크리스트 자동 생성

**문서:**
- Mammoet 제출 가이드: [`docs/MAMMOET_SUBMISSION_QUICKSTART.md`](docs/MAMMOET_SUBMISSION_QUICKSTART.md)
- 제출 패키지 가이드: [`docs/SUBMISSION_PACKAGE_GUIDE.md`](docs/SUBMISSION_PACKAGE_GUIDE.md)

---

## 🚀 빠른 시작

### 환경 설정

#### 1. Python 설치 확인
```bash
python --version
# Python 3.7 이상 필요
```

#### 2. 의존성 설치
```bash
pip install -r requirements.txt
```

### 주요 스크립트 실행

#### RORO Calculator 생성 (v4 HYBRID)
```bash
cd scripts/main
python build_bushra_gateab_v4_hybrid.py
```
- 출력: `../output/LCT_BUSHRA_GateAB_v4_HYBRID.xlsx`

#### Stage_Heights 시트 추가
```bash
cd scripts/main
python bushra_operations.py --patch
```
- 출력: `../output/LCT_BUSHRA_GateAB_v4_HYBRID_with_Dropdown.xlsx`

#### 탱크 레버암 밸러스트 계산
```bash
cd scripts/special
python patch4.py
```
- 출력: `LCT_BUSHRA_Package_TANK_LEVER_ARM.xlsx`

#### Stage 4/6/7 브리지 실행
```bash
cd stage_4_6_7_bridge
python run_bridge_tests.py
```
- 출력: `bushra_stability_export.xlsx`

#### 안정성 계산 (CLI)
```bash
cd bushra_stability
python -m src.cli "path/to/workbook.xls" --stability --imo-check
```

#### 리포트 생성
```bash
cd scripts/generate
python generate_mammoet_submission.py
```

---

## 📁 프로젝트 구조

```
KZ_measurement_note/
├── scripts/                          # 모든 Python 스크립트
│   ├── main/                         # 메인 프로덕션 스크립트
│   │   ├── build_bushra_gateab_v4_hybrid.py      # v4 HYBRID Excel 생성 (권장)
│   │   ├── build_bushra_agi_tr_from_scratch_patched.py  # AGI TR Excel 재생성
│   │   └── bushra_operations.py      # 통합 운영 스크립트
│   ├── generate/                     # 리포트/패키지 생성
│   │   ├── generate_height_report_pdf.py
│   │   ├── generate_vessel_sketch.py
│   │   ├── generate_mammoet_package.py
│   │   └── generate_submission_package.py
│   ├── extract/                      # 데이터 추출
│   │   ├── extract_vessel_depth_from_pdf.py
│   │   ├── extract_stage_data_from_pdf.py
│   │   └── extract_gateab_tide_data.py
│   ├── utils/                        # 유틸리티
│   ├── special/                      # 특수 기능
│   │   └── patch4.py                 # 탱크 레버암 밸러스트 계산
│   ├── tools/                        # 탱크 데이터 관리 도구
│   ├── stage_w_x/                    # Stage Weight/Position 계산
│   └── README.md                     # 스크립트 사용 가이드
│
├── docs/                             # 모든 문서
│   ├── USER_GUIDE.md                 # 사용자 가이드 ⭐
│   ├── TECHNICAL_DOCUMENTATION.md    # 기술 문서 ⭐
│   ├── TANK_LEVER_ARM_GUIDE.md       # 탱크 레버암 가이드
│   ├── README.md                     # 문서 인덱스
│   ├── CHANGELOG.md                  # 변경 이력
│   ├── MAMMOET_SUBMISSION_QUICKSTART.md
│   ├── SUBMISSION_PACKAGE_GUIDE.md
│   ├── patches/                      # 패치 가이드 문서
│   │   ├── README.md                 # 패치 가이드 인덱스
│   │   ├── sdsdds.md                 # Stage별 Trim_target 가이드
│   │   ├── zzzzz.md                  # Trim_target Ballast Fix 가이드
│   │   ├── aaaa.md                   # LCF Draft 보정 가이드
│   │   ├── patcaah.md                # CAPTAIN_REPORT 가이드
│   │   └── wewewewe.md               # Stage Evaluation 가이드
│   ├── captain/                      # Captain 관련 문서
│   │   ├── README.md                 # Captain 문서 인덱스
│   │   ├── QUICK_REFERENCE.md        # 빠른 참조
│   │   ├── PATCH_EXECUTION_GUIDE.md  # 패치 실행 가이드
│   │   ├── GUIDE.md                  # 상세 가이드
│   │   └── README.txt                # README 패치 가이드
│   ├── verification/                 # 검증 리포트
│   │   ├── README.md                 # 검증 리포트 인덱스
│   │   └── (검증 리포트 파일들)
│   ├── plans/                        # 계획 문서
│   ├── reference/                    # 참조 PDF
│   └── ARCHIVE/                      # 원본 문서 백업
│
├── bushra_stability/                 # 안정성 계산 Python 패키지
│   ├── src/                          # 소스 코드
│   │   ├── displacement.py           # Displacement 계산
│   │   ├── stability.py              # Stability 분석
│   │   ├── hydrostatic.py            # Hydrostatic 보간
│   │   ├── imo_check.py              # IMO 검증
│   │   └── cli.py                    # CLI 인터페이스
│   ├── tests/                        # 테스트
│   ├── docs/                         # 모듈 문서
│   └── README.md                     # 모듈 가이드
│
├── stage_4_6_7_bridge/               # Stage 4/6/7 브리지 작업
│   ├── create_stage_tanks_sheet.py
│   ├── fill_stage_tanks.py
│   ├── update_stage_config_with_tanks.py
│   ├── run_bridge_tests.py
│   ├── stage_config_sample_4_7.json
│   └── README.md                     # 브리지 가이드
│
├── output/                           # 생성된 Excel 파일 및 리포트
│   ├── LCT_BUSHRA_GateAB_v4_HYBRID_with_Dropdown.xlsx  # 최종 RORO Calculator
│   ├── LCT_BUSHRA_AGI_TR_from_scratch.xlsx
│   └── (기타 리포트 파일)
│
├── archive/                          # 구버전 파일 보관
│   ├── README.md                     # 아카이브 구조 설명
│   ├── backups/                      # 백업 파일
│   │   └── (agi tr.py 백업 파일들)
│   ├── temp/                         # 임시 파일
│   │   └── python/                   # 임시 Python 스크립트
│   ├── data/                         # 데이터 백업
│   │   └── unused/                   # 미사용 데이터 파일
│   ├── configs/                      # 설정 파일 백업
│   ├── docs/                         # 문서 백업
│   │   └── temp/                     # 임시 문서
│   ├── old_build/                    # 구버전 빌드 스크립트
│   ├── old_utils/                    # 구버전 유틸리티
│   ├── verification/                 # 구버전 검증/분석 스크립트 (통합됨)
│   └── excel_backups/                # Excel 백업 파일
│       └── agi_tr_builds/            # 타임스탬프가 붙은 빌드 파일들
│
├── data/                             # 데이터 파일
│   ├── gateab_v3_tide_data.json      # 조수 데이터 (744시간)
│   └── (기타 데이터 파일)
│
├── bushra_excel_bridge_v1.py         # 브리지 시스템 (루트 유지)
├── verify_excel_generation.py        # 통합 엑셀 검증 스크립트 ⭐
├── analyze_excel_structure.py        # 통합 엑셀 구조 분석 도구 ⭐
├── requirements.txt                  # Python 패키지 의존성
└── README.md                         # 이 파일
```

---

## 📖 문서 네비게이션

### 처음 사용하시나요?

**RORO Calculator 사용:**
1. [`docs/USER_GUIDE.md`](docs/USER_GUIDE.md) - Quick Start 섹션부터 시작
2. [`docs/README.md`](docs/README.md) - 문서 인덱스 참조

**탱크 레버암 밸러스트 계산:**
1. [`docs/TANK_LEVER_ARM_GUIDE.md`](docs/TANK_LEVER_ARM_GUIDE.md) - 탱크 레버암 가이드

**안정성 분석:**
1. [`bushra_stability/README.md`](bushra_stability/README.md) - 안정성 모듈 가이드

### 개발/빌드 작업을 하시나요?

- [`docs/TECHNICAL_DOCUMENTATION.md`](docs/TECHNICAL_DOCUMENTATION.md) - 기술 명세, 빌드 방법, 검증 가이드
- [`scripts/README.md`](scripts/README.md) - 스크립트 사용 가이드
- [`stage_4_6_7_bridge/README.md`](stage_4_6_7_bridge/README.md) - 브리지 시스템 가이드

### 리포트 생성이 필요하신가요?

- [`docs/MAMMOET_SUBMISSION_QUICKSTART.md`](docs/MAMMOET_SUBMISSION_QUICKSTART.md) - Mammoet 제출 가이드
- [`docs/SUBMISSION_PACKAGE_GUIDE.md`](docs/SUBMISSION_PACKAGE_GUIDE.md) - Harbor Master 제출 가이드

### 주요 문서 링크

| 문서 | 설명 | 대상 독자 |
|------|------|----------|
| [`docs/USER_GUIDE.md`](docs/USER_GUIDE.md) | 사용자 가이드 | 선장, 운영자, 현장 작업자 |
| [`docs/TECHNICAL_DOCUMENTATION.md`](docs/TECHNICAL_DOCUMENTATION.md) | 기술 문서 | 개발자, 프로젝트 관리자 |
| [`docs/TANK_LEVER_ARM_GUIDE.md`](docs/TANK_LEVER_ARM_GUIDE.md) | 탱크 레버암 가이드 | 밸러스트 계산 담당자 |
| [`bushra_stability/README.md`](bushra_stability/README.md) | 안정성 모듈 가이드 | 안정성 분석 담당자 |
| [`stage_4_6_7_bridge/README.md`](stage_4_6_7_bridge/README.md) | 브리지 시스템 가이드 | 데이터 동기화 담당자 |
| [`scripts/README.md`](scripts/README.md) | 스크립트 사용 가이드 | 개발자, 자동화 담당자 |

---

## ⚠️ 필수 사항 및 주의사항

### 안전 기준 (CRITICAL LIMITS)

```
⚠️ CRITICAL LIMITS:
- Maximum Ramp Angle: 6.0° (Harbour Master approved)
- FWD Draft Range: 1.5m ~ 3.5m (operational)
- Maximum Wind: 15 knots
- Operations: Daylight only (06:00-18:00)
- Tide Datum: Chart Datum
```

### 필수 확인 사항

1. **K-Z 값**: `Calc!D10`에 현장 실측값 반드시 입력 (⚠️ 필수)
   - 기본값(3.0m)은 플레이스홀더일 뿐
   - 잘못된 K-Z 값은 위험한 Ramp Angle 초과 가능

2. **LCF 좌표 기준**: `Calc!D17`이 midship 기준인지 확인
   - Midship 기준: 음수(-) = Forward, 양수(+) = Aft

3. **Formula_Test**: 모든 테스트 PASS 확인 후 사용

4. **조수 데이터**: `December_Tide_2025` 시트에 744시간 데이터 입력
   - 공식 출처(AD Ports 또는 ADNOC) 데이터 사용 필수

5. **Excel 파일**: 스크립트 실행 전 Excel 파일 닫기

### 필수 파일

- `data/gateab_v3_tide_data.json` - 빌드 체인 필수 파일
- `bushra_stability/data/master_tanks.json` - 탱크 마스터 데이터
- `output/LCT_BUSHRA_GateAB_v4_HYBRID.xlsx` - 중간 파일 (검증/패치용)

---

## 🔧 기술 스택

### 필수 요구사항
- **Python**: 3.7 이상
- **운영체제**: Windows, Linux, macOS

### 주요 라이브러리
- `openpyxl` (3.1.2) - Excel 파일 처리
- `pandas` (≥2.0.0) - 데이터 분석
- `xlrd` (≥2.0.0) - Excel 읽기
- `streamlit` (≥1.28.0) - 웹 UI (안정성 모듈)
- `pytest` (≥7.4.0) - 테스트 프레임워크

### 설치
```bash
pip install -r requirements.txt
```

---

## 🎯 시작하기

### 처음 사용하시나요?

1. **RORO Calculator 사용**
   - [`docs/USER_GUIDE.md`](docs/USER_GUIDE.md)의 Quick Start 섹션 읽기
   - `output/LCT_BUSHRA_GateAB_v4_HYBRID_with_Dropdown.xlsx` 파일 열기
   - K-Z 값 현장 측정 후 입력

2. **밸러스트 계산**
   - [`docs/TANK_LEVER_ARM_GUIDE.md`](docs/TANK_LEVER_ARM_GUIDE.md) 참조
   - `scripts/special/patch4.py` 실행

3. **안정성 분석**
   - [`bushra_stability/README.md`](bushra_stability/README.md) 참조
   - CLI 또는 Streamlit 웹 UI 사용

### 개발자 가이드

1. **빌드 시스템**
   - [`docs/TECHNICAL_DOCUMENTATION.md`](docs/TECHNICAL_DOCUMENTATION.md) - 빌드 방법 섹션
   - [`scripts/README.md`](scripts/README.md) - 스크립트 사용 가이드

2. **브리지 시스템**
   - [`stage_4_6_7_bridge/README.md`](stage_4_6_7_bridge/README.md) 참조
   - `bushra_excel_bridge_v1.py` 모듈 사용

3. **리포트 생성**
   - [`docs/MAMMOET_SUBMISSION_QUICKSTART.md`](docs/MAMMOET_SUBMISSION_QUICKSTART.md) 참조
   - `scripts/generate/` 폴더의 스크립트 사용

4. **엑셀 파일 검증 및 분석**
   - **검증**: `python verify_excel_generation.py [--quick] [--detailed] [--formulas]`
     - 원본 vs 생성 파일 종합 비교
     - 시트/컬럼/헤더/값/수식 검증
     - 자동으로 최신 생성 파일 감지
   - **분석**: `python analyze_excel_structure.py [--file PATH] [--sheet SHEET] [--all]`
     - 엑셀 파일 구조 분석
     - 시트별 상세 정보
     - 수식 참조 분석

---

## 📊 주요 기능 요약

### RORO Calculator
- ✅ 744시간 조수 데이터 분석
- ✅ 시간별 Draft 계산
- ✅ Ramp Angle 계산 (≤6° 제한)
- ✅ Stage별 시나리오 분석
- ✅ 드롭다운 기반 시간 선택
- ✅ 자동 검증 테스트

### 밸러스트 계산
- ✅ 레버암 기반 정확한 계산
- ✅ 11개 탱크 데이터베이스
- ✅ 좌표 변환 자동화
- ✅ 시나리오별 탱크 선택 가이드

### 안정성 분석
- ✅ Displacement 계산
- ✅ Stability 분석 (GZ 곡선)
- ✅ IMO A.749 검증
- ✅ Hydrostatic 보간
- ✅ Site별 검증 (DAS/AGI)

### 리포트 생성
- ✅ PDF 리포트 자동 생성
- ✅ 제출 패키지 자동 생성
- ✅ 선박 스케치 생성
- ✅ 체크리스트 자동 생성

---

## 🔄 프로젝트 이력

### 2025-11-19: 프로젝트 파일 정리 완료 (v3.9.1)
- 패치 가이드 문서를 `docs/patches/`로 이동 및 인덱스 생성
- Captain 관련 문서를 `docs/captain/`로 이동 및 인덱스 생성
- 검증 리포트를 `docs/verification/`로 이동 및 인덱스 생성
- 아카이브 구조 정리 (`archive/backups/`, `archive/temp/`, `archive/data/unused/`, `archive/configs/`)
- Excel 파일 정리 (최신만 루트 유지, 나머지 아카이브)
- 데이터 파일 정리 (루트 JSON → data/, 미사용 → archive/)
- 임시 Python 파일 및 설정 파일 아카이브
- 모든 디렉토리에 README.md 인덱스 생성

### 2025-11-18: 프로젝트 파일 정리 완료
- AGI TR 빌드 스크립트를 `scripts/main/`으로 이동
- 구버전 파일들을 `archive/` 폴더로 정리
- Excel 백업 파일들을 `archive/excel_backups/`로 정리
- 문서 정리 및 구조화

### 2025-11-12: v4 HYBRID 버전 출시
- v4 표준 셀 매핑 (D8~D19) 적용
- GateAB v3 조수 데이터 통합
- Stage_Heights 시트 추가
- 드롭다운 기능 추가

### 2025-11-06: 탱크 레버암 시스템 도입
- Patch 4: 레버암 기반 정확한 계산
- 37% 밸러스트 절감 달성

---

## 📞 지원 및 문의

### 기술 문의
- MACHO-GPT System
- Samsung C&T Logistics Team

### 문서 버그 리포트
프로젝트 관리자에게 문의

---

## 📝 라이선스

Samsung C&T Corporation - Internal Use Only
HVDC Project - LCT BUSHRA Operations

---

## 🎓 참고 자료

### 입력 문서
- LCT BUSHRA 안정성 계산서
- 밸러스트 배치도
- 선박 일반 배치도
- Vessel Stability Booklet

### 관련 표준
- IMO 안정성 기준 (A.749)
- 항만 규정
- RORO 운영 절차

---

**성공적인 변압기 운송을 기원합니다!** 🚢⚡

