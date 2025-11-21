# LCT BUSHRA RORO Calculator — Documentation Index

**최종 버전:** v4 HYBRID with Dropdown  
**생성일:** 2025년 11월 5일  
**상태:** ✅ APPROVED FOR OPERATION  
**문서 버전:** 2.0 (통합 재구성)

---

## 📚 문서 구조

이 프로젝트의 문서는 **2개의 주요 문서**로 통합되었습니다:

### 1. [USER_GUIDE.md](./USER_GUIDE.md) - 사용자 가이드
**독자:** 선장, 운영자, 현장 작업자, 최종 사용자

**포함 내용:**
- Quick Start (3단계/5단계 가이드)
- 사용 방법 (단계별 상세 가이드)
- 좌표 시스템 및 수식 유도
- K-Z 측정 절차
- Troubleshooting
- Safety Limits 및 Emergency Contacts
- 리포트 템플릿 (FWD_AFT_Report_Template)

### 2. [TECHNICAL_DOCUMENTATION.md](./TECHNICAL_DOCUMENTATION.md) - 기술 문서
**독자:** 개발자, 프로젝트 관리자, 기술 검토자, QA 담당자

**포함 내용:**
- 프로젝트 개요 및 이력
- 기술 명세 (셀 매핑, 수식, 좌표 시스템)
- 빌드 방법 (3가지 방법 모두)
- 검증 가이드 및 로그
- 프로젝트 진행 과정 (Phase 1-6)
- 파일 변천사
- v3 vs v4 비교
- 업그레이드 요약
- 부록 (스크립트 목록, 수식 완전 목록)

---

## 🎯 빠른 시작 (Quick Start)

### 메인 파일 위치
```
output/LCT_BUSHRA_GateAB_v4_HYBRID_with_Dropdown.xlsx
```

### 5분 사용 가이드
1. Excel 파일 열기: `output/LCT_BUSHRA_GateAB_v4_HYBRID_with_Dropdown.xlsx`
2. Calc!D10 → K-Z 값 확인 (⚠️ 현장 실측값 필수)
3. Formula_Test → 모든 테스트 PASS 확인
4. Stage_Heights → C열 드롭다운에서 작업 시간 선택
5. D/E/G 자동 조회 값 확인
6. 제출물_검수체크리스트 완료

**자세한 내용:** [USER_GUIDE.md](./USER_GUIDE.md)의 Quick Start 섹션 참조

---

## 📖 문서 네비게이션

### 처음 사용하시나요?
→ [USER_GUIDE.md](./USER_GUIDE.md)부터 시작하세요
1. Quick Start 섹션 읽기
2. STEP 1: Calc Sheet 파라미터 업데이트
3. STEP 2: 조수 데이터 입력
4. STEP 3: 작업 시간대 선택

### 개발/빌드 작업을 하시나요?
→ [TECHNICAL_DOCUMENTATION.md](./TECHNICAL_DOCUMENTATION.md) 참조
1. 기술 명세 섹션 (셀 매핑, 수식)
2. 빌드 방법 섹션 (3가지 방법)
3. 검증 가이드 섹션

### v3에서 v4로 전환하시나요?
→ [TECHNICAL_DOCUMENTATION.md](./TECHNICAL_DOCUMENTATION.md)의 "v3 vs v4 비교" 섹션 참조

### 리포트 템플릿이 필요하신가요?
→ [USER_GUIDE.md](./USER_GUIDE.md)의 "FWD/AFT Report Template" 섹션 참조

---

## 📁 프로젝트 디렉토리 구조

```
KZ_measurement_note/
├── docs/                          # 문서 디렉토리
│   ├── README.md                  # 이 파일 (메인 인덱스)
│   ├── USER_GUIDE.md              # 사용자 가이드 ⭐
│   ├── TECHNICAL_DOCUMENTATION.md # 기술 문서 ⭐
│   └── ARCHIVE/                   # 원본 문서 백업
│
├── scripts/                       # 스크립트
│   ├── extract_gateab_tide_data.py
│   ├── build_bushra_gateab_v4_hybrid.py
│   ├── bushra_operations.py
│   └── ...
│
├── data/                          # 데이터
│   ├── gateab_v3_tide_data.json  # 조수 데이터 (빌드 필수)
│   └── ...
│
├── output/                        # 산출물
│   └── LCT_BUSHRA_GateAB_v4_HYBRID_with_Dropdown.xlsx ⭐
│
└── backup/                        # 백업 파일
    └── Bushra_GateAB_Updated_v3.xlsx
```

---

## 🔧 주요 기능 요약

### v4 표준 기능
- Calc 시트: 표준 셀 매핑 (D8~D19)
- December_Tide_2025: 744시간 조수 데이터
- Hourly_FWD_AFT_Heights: 시간별 Draft 계산
- RORO_Stage_Scenarios: Stage별 시나리오 계산
- Formula_Test: 자동 검증 테스트

### GateAB v3 통합 기능
- Stage_Heights: 최근접 매칭 (±30분)
- 드롭다운: 744시간 목록
- Trim 조정: Target Trim 입력 시 자동 계산

### 한글 시트
- Summary_요약
- 실행_방법
- 시트_구성_수식
- 제출물_검수체크리스트
- STANDARD_좌표기준

---

## ⚠️ 중요 사항

### 필수 확인 사항
- **K-Z 값**: `Calc!D10`에 현장 실측값 반드시 입력 (⚠️ 필수)
- **LCF 좌표 기준**: `Calc!D17`이 midship 기준인지 확인
- **Formula_Test**: 모든 테스트 PASS 확인 후 사용
- **조수 데이터**: `December_Tide_2025` 시트에 744시간 데이터 입력

### 필수 파일
- `data/gateab_v3_tide_data.json` - 빌드 체인 필수 파일
- `output/LCT_BUSHRA_GateAB_v4_HYBRID.xlsx` - 중간 파일 (검증/패치용)

---

## 📞 빠른 링크

### 사용자 가이드
- [Quick Start](./USER_GUIDE.md#quick-start)
- [사용 방법](./USER_GUIDE.md#사용-방법)
- [Troubleshooting](./USER_GUIDE.md#troubleshooting)
- [Safety Limits](./USER_GUIDE.md#critical-safety-limits)
- [Report Template](./USER_GUIDE.md#fwd-aft-report-template)

### 기술 문서
- [기술 명세](./TECHNICAL_DOCUMENTATION.md#기술-명세)
- [빌드 방법](./TECHNICAL_DOCUMENTATION.md#빌드-방법)
- [검증 가이드](./TECHNICAL_DOCUMENTATION.md#검증-가이드)
- [프로젝트 이력](./TECHNICAL_DOCUMENTATION.md#프로젝트-개요-및-이력)

---

## 🔄 문서 통합 이력

**v2.0 (현재)**
- 9개 분산 문서를 2개로 통합
- USER_GUIDE.md: 모든 사용자용 내용 통합
- TECHNICAL_DOCUMENTATION.md: 모든 기술적 내용 통합
- 원본 문서는 ARCHIVE/에 보존

**v1.0 (이전)**
- 9개 분산 문서 구조
- README.md, RoRo_Calculator_User_Guide.md, BUSHRA_PROJECT_COMPLETE_DOCUMENTATION.md 등

---

## 📝 문서 작성 규칙

### 문서 버전 관리
- 주요 변경 시 버전 업데이트
- 변경 이력 섹션에 기록

### 링크 형식
- 상대 경로 사용: `[링크 텍스트](./파일명.md)`
- 앵커 링크: `[섹션](./파일명.md#섹션명)`

### 일관성 유지
- 용어 통일 (예: K-Z, KminusZ, KminusZ_m)
- 셀 참조 형식 통일 (예: Calc!D10, Calc!$D$10)

---

**마지막 업데이트:** 2025-01-XX  
**문서 관리자:** MACHO-GPT v3.6-APEX LogiMaster
