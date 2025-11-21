# 루트 폴더 파일 정리 계획

**작성일:** 2025-11-19
**목적:** 루트 디렉토리 정리 및 파일 분류

---

## 현재 루트 폴더 파일 현황

### 필수 파일 (유지)
- `agi tr.py` - 메인 스크립트 (CHANGELOG.md 기준)
- `README.md` - 프로젝트 README
- `requirements.txt` - Python 의존성
- `verify_excel_generation.py` - 통합 엑셀 검증 스크립트 (README.md 명시)
- `analyze_excel_structure.py` - 통합 엑셀 구조 분석 도구 (README.md 명시)
- `bushra_excel_bridge_v1.py` - 브리지 시스템 (README.md에 루트 유지 명시)

### 정리 필요 파일

#### 1. 검증 스크립트 (archive/verification/로 이동)
- `comprehensive_formula_verification.py` - 종합 수식 검증 스크립트
- `verify_excel_formulas.py` - Excel 수식 검증 스크립트

**이유:** 이미 `verify_excel_generation.py`가 통합 검증 스크립트로 사용 중이며, 구버전 검증 스크립트들은 `archive/verification/`에 보관되어 있음

#### 2. 변환 스크립트 (scripts/tools/로 이동)
- `convert_tank_coordinates_to_json.py`
- `convert_tank_csv_to_json.py`
- `convert_tank_data_to_json.py`
- `convert_tank_excel_to_json.py`
- `convert_tank_to_json_final.py`

**이유:**
- 탱크 데이터 변환 관련 스크립트들
- `scripts/tools/`에 이미 유사한 스크립트(`convert_tanks_csv_to_json.py`)가 있음
- `scripts/tools/README.md`에 탱크 데이터 관리 도구로 명시됨

#### 3. ZIP 파일 (archive/로 이동)
- `bushra_excel_bridge_v1.zip` - 브리지 시스템 ZIP 파일
- `LCT_BUSHRA_Package_TANK_LEVER_ARM.zip` - 탱크 레버암 패키지 ZIP 파일

**이유:**
- 소스 코드는 이미 있으므로 ZIP 파일은 아카이브로 이동
- `archive/` 디렉토리에 보관

#### 4. Excel 파일 (확인 필요)
- `LCT_BUSHRA_GateAB_v4_HYBRID.xlsx`

**확인 사항:**
- `output/` 디렉토리에 동일한 파일이 있는지 확인
- 최신 버전인지 확인
- 루트에 유지할 필요가 있는지 확인

#### 5. 계획 파일 (docs/plans/로 이동)
- `.plan.md` - 프로젝트 계획 파일

**이유:** 계획 문서는 `docs/plans/` 디렉토리에 보관하는 것이 적절

---

## 정리 작업 계획

### Phase 1: 검증 스크립트 정리
1. `comprehensive_formula_verification.py` → `archive/verification/`
2. `verify_excel_formulas.py` → `archive/verification/`

### Phase 2: 변환 스크립트 정리
1. `convert_tank_*.py` (5개 파일) → `scripts/tools/`
2. `scripts/tools/README.md` 업데이트 (새 스크립트 추가)

### Phase 3: ZIP 파일 정리
1. `bushra_excel_bridge_v1.zip` → `archive/`
2. `LCT_BUSHRA_Package_TANK_LEVER_ARM.zip` → `archive/`

### Phase 4: Excel 파일 확인 및 정리
1. `output/` 디렉토리와 비교
2. 중복이면 루트 파일 삭제 또는 아카이브
3. 최신 버전만 유지

### Phase 5: 계획 파일 정리
1. `.plan.md` → `docs/plans/root-folder-cleanup-plan.md` (이미 생성됨)
2. 기존 `.plan.md`는 삭제 또는 아카이브

### Phase 6: 문서 업데이트
1. `README.md` 업데이트 (필요시)
2. `scripts/tools/README.md` 업데이트

---

## 예상 결과

### 정리 전
- 루트 디렉토리: 17개 파일

### 정리 후
- 루트 디렉토리: 6개 필수 파일만 유지
  - `agi tr.py`
  - `README.md`
  - `requirements.txt`
  - `verify_excel_generation.py`
  - `analyze_excel_structure.py`
  - `bushra_excel_bridge_v1.py`

---

## 주의사항

### 보존 필수 파일
- `agi tr.py` - 메인 스크립트
- `README.md` - 프로젝트 README
- `requirements.txt` - Python 의존성
- `verify_excel_generation.py` - 통합 검증 스크립트 (README.md 명시)
- `analyze_excel_structure.py` - 분석 도구 (README.md 명시)
- `bushra_excel_bridge_v1.py` - 브리지 시스템 (README.md 명시)

### 삭제 전 확인
- Excel 파일 중복 확인
- 변환 스크립트의 의존성 확인
- ZIP 파일의 내용 확인 (필요시)

---

## 검증 체크리스트

- [ ] 모든 파일 이동 완료
- [ ] `scripts/tools/README.md` 업데이트
- [ ] `README.md` 확인 (필요시 업데이트)
- [ ] 루트 디렉토리 파일 수 확인 (6개)
- [ ] 필수 파일 유지 확인

