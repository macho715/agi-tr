# Scripts 및 Stage_4_6_7_Bridge 폴더 정리 계획

**작성일:** 2025-11-19
**목적:** scripts 폴더와 stage_4_6_7_bridge 폴더의 파일 정리 및 구조화

---

## 현재 상태 분석

### Scripts 폴더 현황

#### 루트에 남아있는 파일들 (정리 필요)
1. **메인 스크립트** (main/로 이동 필요)
   - `build_bushra_v4_standalone.py` → `scripts/main/`
   - `bushra_operations.py` → `scripts/main/`

2. **생성 스크립트** (generate/로 이동 필요)
   - `generate_mammoet_package.py` → `scripts/generate/`
   - `generate_mammoet_submission.py` → `scripts/generate/`
   - `generate_submission_package.py` → `scripts/generate/`
   - `generate_vessel_sketch.py` → `scripts/generate/`

3. **추출 스크립트** (extract/로 이동 필요)
   - `extract_gateab_tide_data.py` → `scripts/extract/`

4. **유틸리티 스크립트** (utils/로 이동 필요)
   - `PATCH1106.py` → `scripts/utils/`

5. **문서 파일** (docs/로 이동 필요)
   - `함수.patch` → `scripts/docs/`
   - `p.md` → `scripts/docs/` 또는 `archive/docs/`
   - `정리_완료_보고서.md` → `archive/docs/` (이미 완료된 작업 보고서)

6. **기타 파일**
   - `BUSHRA Stability_Calculation.xls` → `archive/data/` (대용량 파일)
   - `LCT_BUSHRA_FWD_AFT_Report_sample.pdf` → `scripts/SUBMISSION_PACKAGE/01_PDF_Report/` 또는 `docs/reference/`
   - `[HVDC]AGI TRANSFORMER-20251112T040730Z-1-001.zip` → `archive/` (이미 디렉토리로 압축 해제됨)

7. **확장자 없는 파일들** (Python 스크립트로 추정)
   - `generate` (14KB, Python 스크립트로 추정) → `scripts/generate/` 디렉토리 생성 후 이동 또는 `.py` 확장자 추가
   - `extract` (9KB, Python 스크립트로 추정) → `scripts/extract/` 디렉토리 생성 후 이동 또는 `.py` 확장자 추가
   - `utils` (18KB, Python 스크립트로 추정) → `scripts/utils/` 디렉토리 생성 후 이동 또는 `.py` 확장자 추가
   - `special` (26KB, Python 스크립트로 추정) → `scripts/special/` 디렉토리 생성 후 이동 또는 `.py` 확장자 추가
   - `docs` (3.7KB, 문서 파일로 추정) → `scripts/docs/` 디렉토리 생성 후 이동 또는 내용 확인

#### main/ 디렉토리 정리 필요
- 백업 파일들:
  - `build_bushra_agi_tr_from_scratch_patched.py.backup_20251118_155910` → `archive/backups/`
  - `build_bushra_agi_tr_from_scratch_patched.py.backup_20251118_160356` → `archive/backups/`
  - `build_bushra_agi_tr_from_scratch_patched.py.backup_v10_20251118_162215` → `archive/backups/`

#### output/ 디렉토리 정리 필요
- 타임스탬프가 붙은 Excel 파일들 → `archive/output/` 또는 삭제

### Stage_4_6_7_Bridge 폴더 현황

#### 정리 필요 파일
1. **중복 문서**
   - `BRIDGE_EXECUTION_SUMMARY.md` → `archive/docs/` (초기 요약, FINAL이 최종)
   - 또는 `FINAL_BRIDGE_EXECUTION_SUMMARY.md`만 유지

2. **템플릿/샘플 파일** (유지)
   - `Stage_Tanks_template.xlsx` - 유지
   - `stage_config_sample_4_7.json` - 유지
   - `bushra_stability_verification.json` - 유지

3. **출력 파일** (확인 필요)
   - `bushra_stability_export.xlsx` - 최신 버전인지 확인 후 유지 또는 아카이브

---

## 정리 작업 계획

### Phase 1: Scripts 폴더 - 파일 이동

#### 1.1 메인 스크립트 이동
- `build_bushra_v4_standalone.py` → `scripts/main/`
- `bushra_operations.py` → `scripts/main/`

#### 1.2 생성 스크립트 이동
- `generate_mammoet_package.py` → `scripts/generate/`
- `generate_mammoet_submission.py` → `scripts/generate/`
- `generate_submission_package.py` → `scripts/generate/`
- `generate_vessel_sketch.py` → `scripts/generate/`

#### 1.3 추출 스크립트 이동
- `extract_gateab_tide_data.py` → `scripts/extract/`

#### 1.4 유틸리티 스크립트 이동
- `PATCH1106.py` → `scripts/utils/`

#### 1.5 문서 파일 이동
- `함수.patch` → `scripts/docs/`
- `p.md` → `scripts/docs/` (또는 내용 확인 후 결정)
- `정리_완료_보고서.md` → `archive/docs/` (이미 완료된 작업)

#### 1.6 기타 파일 이동
- `BUSHRA Stability_Calculation.xls` → `archive/data/`
- `LCT_BUSHRA_FWD_AFT_Report_sample.pdf` → `scripts/SUBMISSION_PACKAGE/01_PDF_Report/` (이미 존재하는지 확인)
- `[HVDC]AGI TRANSFORMER-20251112T040730Z-1-001.zip` → `archive/` (디렉토리와 중복)

#### 1.7 확장자 없는 파일 처리 (확인 완료 - 모두 Python 스크립트)
- `generate` → `scripts/generate/generate_height_report_pdf.py` (PDF 리포트 생성 스크립트)
- `extract` → `scripts/extract/extract_vessel_depth_from_pdf.py` (D-vessel 추출 스크립트)
- `utils` → `scripts/utils/pdf_to_excel_converter.py` (PDF→Excel 변환 스크립트)
- `special` → `scripts/special/patch4.py` (탱크 레버암 밸러스트 계산 스크립트)
- `docs` → `scripts/docs/coordinate_reference.md` (좌표 참조 문서)
- 각 파일을 적절한 이름과 확장자로 변경 후 해당 디렉토리로 이동

### Phase 2: Scripts/main/ 디렉토리 정리

#### 2.1 백업 파일 이동
- `build_bushra_agi_tr_from_scratch_patched.py.backup_*` (3개) → `archive/backups/`

### Phase 3: Scripts/output/ 디렉토리 정리

#### 3.1 타임스탬프 파일 정리
- 타임스탬프가 붙은 Excel 파일들 → `archive/output/` 또는 삭제
- 최신 파일만 유지: `LCT_BUSHRA_AGI_TR_from_scratch.xlsx`

### Phase 4: Stage_4_6_7_Bridge 폴더 정리

#### 4.1 중복 문서 정리
- `BRIDGE_EXECUTION_SUMMARY.md` → `archive/docs/` (FINAL이 최종 버전)
- 또는 두 문서 모두 유지 (초기/최종 구분)

#### 4.2 출력 파일 확인
- `bushra_stability_export.xlsx` - 최신 버전 확인 후 결정

### Phase 5: 문서 업데이트

#### 5.1 Scripts/README.md 업데이트
- 파일 이동 반영
- 경로 업데이트

#### 5.2 Stage_4_6_7_Bridge/README.md 업데이트
- 문서 정리 반영 (필요시)

---

## 예상 결과

### Scripts 폴더 정리 후
- 루트: README.md, 디렉토리들만 유지
- main/: 메인 스크립트만 (백업 파일 제거)
- generate/: 생성 스크립트만
- extract/: 추출 스크립트만
- utils/: 유틸리티 스크립트만
- special/: 특수 기능 스크립트만
- docs/: 문서 파일만
- archive/: 백업 및 구버전 파일

### Stage_4_6_7_Bridge 폴더 정리 후
- Python 스크립트: 6개 유지
- 설정/템플릿 파일: 3개 유지
- 문서: 1-2개 유지 (FINAL만 또는 초기+최종)
- 출력 파일: 최신만 유지

---

## 주의사항

### 보존 필수 파일
- 모든 Python 스크립트 (기능 파일)
- 설정/템플릿 파일 (JSON, Excel 템플릿)
- README.md 파일들

### 삭제 전 확인
- 파일명만 있는 파일들 (generate, extract 등)의 내용 확인
- 출력 파일의 최신성 확인
- 중복 문서의 내용 비교

### 경로 참조 확인
- 스크립트 내부의 import 경로
- 상대 경로 참조
- README.md의 경로 설명

---

## 검증 체크리스트

- [ ] 모든 파일 이동 완료
- [ ] scripts/README.md 업데이트
- [ ] stage_4_6_7_bridge/README.md 확인
- [ ] 스크립트 실행 테스트 (경로 확인)
- [ ] 디렉토리 구조 확인
- [ ] 백업 파일 아카이브 확인

