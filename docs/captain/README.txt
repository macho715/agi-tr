# README.md 패치 - Captain Mail Response 섹션 추가

**위치:** "## 📖 문서 네비게이션" 섹션 **바로 위**에 다음 섹션을 추가하세요.

---

## 🚨 Captain Mail Response (URGENT)

**상태:** ⚠️ **Action Required**  
**우선순위:** **HIGH**  
**마감:** 48시간 이내

캡틴으로부터 Stage 5A-2 계산 관련 4가지 문제점이 지적되었습니다. 즉시 대응이 필요합니다.

### 빠른 접근 링크

| 문서 | 목적 | 소요시간 |
|------|------|----------|
| 🔥 **[CAPTAIN_QUICK_REFERENCE.md](CAPTAIN_QUICK_REFERENCE.md)** | 문제 요약 및 빠른 참조 | 5분 읽기 |
| 📖 **[captain.md](captain.md)** | 패치 이론 및 상세 설명 | 15분 읽기 |
| 🛠️ **[CAPTAIN_PATCH_EXECUTION_GUIDE.md](CAPTAIN_PATCH_EXECUTION_GUIDE.md)** | 단계별 실행 가이드 | 60분 실행 |

### 지적된 문제점

1. ❌ **Stage 5A-2 전/후흘수 불일치** (파일 2.92m vs 메일 2.32m)
2. ❌ **FWD 탱크를 AFT ballast로 오표기** (FWB1/2, FWCARGO1 P/S)
3. ❌ **모든 Stage에서 Draft ≤ 2.70m 검증 미흡**
4. ❌ **Linkspan freeboard 0.28m 충분성 미확인**

### 패치 실행 프로세스

```
1. 백업 (1분) → 2. 패치 실행 (50분) → 3. 검증 (5분) → 4. 리포트 (4분)
총 소요시간: 약 60분
```

### 빠른 실행
```bash
# 1단계: 백업
copy output\LCT_BUSHRA_AGI_TR.xlsx backup\

# 2단계: 패치 실행
cd scripts\special
python patch_captain_response.py --input ..\..\output\LCT_BUSHRA_AGI_TR.xlsx --output ..\..\output\LCT_BUSHRA_AGI_TR_CAPTAIN_PATCHED.xlsx

# 3단계: 검증
cd ..\..
python verify_excel_generation.py --file output\LCT_BUSHRA_AGI_TR_CAPTAIN_PATCHED.xlsx --detailed
```

### 다음 단계
1. ✅ [CAPTAIN_QUICK_REFERENCE.md](CAPTAIN_QUICK_REFERENCE.md) 읽기 (5분)
2. ✅ [CAPTAIN_PATCH_EXECUTION_GUIDE.md](CAPTAIN_PATCH_EXECUTION_GUIDE.md)의 체크리스트 따라하기 (60분)
3. ✅ 패치 완료 후 프로젝트 매니저에게 보고

---

