# Captain Mail Response - Quick Reference

**⚠️ URGENT:** 캡틴 메일에서 지적된 4가지 문제점 해결을 위한 빠른 참조 가이드

---

## 🚨 캡틴이 지적한 문제점

1. **Stage 5A-2 전/후흘수 불일치**
   - 파일: 2.92m / 메일: 2.32m
   - 원인: 수식 vs 하드코딩 값 불일치

2. **FWD 탱크인데 AFT ballast로 표기**
   - FWB1, FWB2, FWCARGO1(P/S)는 선수(FWD) 탱크
   - 설명과 위치가 모순

3. **모든 Stage에서 Draft ≤ 2.70m 확인 필요**
   - Summer draft 제한 준수 필요
   - 현재 일부 Stage에서 초과 가능성

4. **Linkspan freeboard 0.28m 충분한지 확인**
   - 링크스팬 접속부 여유고 검증 필요

---

## 📋 해결 방안 요약

| 문제 | 패치 | 해결 방법 | 소요시간 |
|------|------|-----------|----------|
| 1 | P2 | Stage 5A-2 수식 정합 | 15분 |
| 2 | P3 | X_Ballast 탱크 CG 재계산 | 20분 |
| 3 | P4 | Draft Limit Check 추가 | 15분 |
| 4 | P4 | Freeboard Check 추가 | 10분 |

---

## 🔗 상세 가이드 링크

### 📖 이론 및 배경
👉 **[captain.md](captain.md)** - 각 패치 항목의 상세 설명 및 이론

### 🛠️ 실행 가이드
👉 **[CAPTAIN_PATCH_EXECUTION_GUIDE.md](CAPTAIN_PATCH_EXECUTION_GUIDE.md)** - 단계별 실행 방법

---

## ⚡ 빠른 실행 (60분 소요)

### 1단계: 백업 (1분)
```bash
cd C:\Users\SAMSUNG\Downloads\KZ_measurement_note
copy output\LCT_BUSHRA_AGI_TR.xlsx backup\LCT_BUSHRA_AGI_TR_backup_%date:~0,4%%date:~5,2%%date:~8,2%.xlsx
```

### 2단계: 자동 패치 실행 (50분)
```bash
cd scripts\special
python patch_captain_response.py --input ..\..\output\LCT_BUSHRA_AGI_TR.xlsx --output ..\..\output\LCT_BUSHRA_AGI_TR_CAPTAIN_PATCHED.xlsx
```

### 3단계: 검증 (5분)
```bash
cd ..\..
python verify_excel_generation.py --file output\LCT_BUSHRA_AGI_TR_CAPTAIN_PATCHED.xlsx --detailed
```

### 4단계: 리포트 생성 (4분)
```bash
cd scripts\generate
python generate_captain_report_pdf.py --input ..\..\output\LCT_BUSHRA_AGI_TR_CAPTAIN_PATCHED.xlsx
```

---

## ✅ 검증 체크리스트

패치 완료 후 다음 항목을 확인:

- [ ] **P1**: Calc 시트 - D_vessel = 3.65m, MTC = 33.99
- [ ] **P2**: Stage 5A-2 - Dfwd가 수식 기반이고 ≤ 2.70m
- [ ] **P3**: X_Ballast - FWD 탱크 CG 반영, "AFT" 표현 제거
- [ ] **P4**: CAPTAIN_REPORT 시트 생성 및 모든 Check "OK"

---

## 📁 관련 파일

```
KZ_measurement_note/
├── captain.md                              ← 패치 이론 및 배경
├── CAPTAIN_PATCH_EXECUTION_GUIDE.md        ← 실행 가이드
├── CAPTAIN_QUICK_REFERENCE.md              ← 이 파일
├── output/
│   ├── LCT_BUSHRA_AGI_TR.xlsx             ← 원본
│   └── LCT_BUSHRA_AGI_TR_CAPTAIN_PATCHED.xlsx  ← 패치 결과
├── scripts/special/
│   └── patch_captain_response.py           ← 패치 스크립트
└── verify_excel_generation.py              ← 검증 도구
```

---

## 🆘 문제 발생 시

1. **스크립트가 없는 경우**
   - CAPTAIN_PATCH_EXECUTION_GUIDE.md의 "수동 패치" 섹션 참조

2. **검증 실패**
   - backup 폴더에서 원본 복원
   - 수동 패치로 재시도

3. **추가 도움 필요**
   - docs/TECHNICAL_DOCUMENTATION.md 참조
   - 프로젝트 매니저에게 문의

---

**다음 단계:** [CAPTAIN_PATCH_EXECUTION_GUIDE.md](CAPTAIN_PATCH_EXECUTION_GUIDE.md)로 이동하여 상세 실행 방법 확인
