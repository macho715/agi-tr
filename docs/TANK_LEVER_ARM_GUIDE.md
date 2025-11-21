# LCT BUSHRA - 탱크 레버암 방식 밸러스트 계산 시스템

## 📋 프로젝트 개요

LCT BUSHRA 선박의 RORO 운송 시 정확한 밸러스트 계산을 위한 탱크별 레버암 기반 시스템입니다.

### 주요 기능

- ✅ 11개 탱크 데이터베이스 (실제 안정성 계산서 기반)
- ✅ AP 기준 → Midship 기준 자동 좌표 변환
- ✅ 정확한 레버암(L_b) 계산
- ✅ 단계별 RORO 밸러스트 계산
- ✅ 시나리오별 탱크 선택 가이드
- ✅ 실전 예시 및 계산 공식

---

## 🚀 빠른 시작

### 1. 환경 설정

#### Python 설치 확인
```bash
python --version
# Python 3.7 이상 필요
```

#### 의존성 설치
```bash
cd C:\Users\SAMSUNG\Downloads\KZ_measurement_note
pip install -r requirements.txt
```

### 2. 실행

```bash
cd scripts
python patch4.py
```

### 3. 결과 확인

생성된 Excel 파일을 열어서 사용:
```
C:\Users\SAMSUNG\Downloads\KZ_measurement_note\LCT_BUSHRA_Package_TANK_LEVER_ARM.xlsx
```

---

## 📁 프로젝트 구조

```
KZ_measurement_note/
├── scripts/
│   ├── main/                        # 메인 프로덕션 스크립트
│   │   ├── build_bushra_gateab_v4_hybrid.py      # v4 HYBRID Excel 생성 (권장)
│   │   ├── build_bushra_agi_tr_from_scratch_patched.py  # AGI TR Excel 재생성
│   │   └── bushra_operations.py    # 통합 운영 스크립트
│   ├── generate/                    # 리포트/패키지 생성
│   ├── extract/                     # 데이터 추출
│   ├── utils/                       # 유틸리티
│   └── special/                     # 특수 기능
├── stage_4_6_7_bridge/              # Stage 4/6/7 브리지 작업
├── bushra_stability/                # 안정성 계산 모듈
├── output/                          # 생성된 Excel 파일
├── archive/                         # 구버전 파일 보관
│   ├── old_build/                   # 구버전 빌드 스크립트
│   ├── old_utils/                   # 구버전 유틸리티
│   └── excel_backups/               # Excel 백업 파일
├── docs/                            # 문서
│   ├── plans/                       # 계획 문서
│   └── reference/                   # 참조 PDF
├── bushra_excel_bridge_v1.py        # 브리지 시스템 (루트 유지)
├── requirements.txt                 # Python 패키지
└── docs/TANK_LEVER_ARM_GUIDE.md     # 이 문서 (탱크 레버암 가이드)
```

---

## 📊 Excel 시트 구성

### 1. Calc
- 기본 계산 파라미터
- LCF, MTC, TPC 등

### 2. Tank_Catalog
- 11개 탱크 데이터베이스
- LCG_AP, x_mid, L_b, 용량 등
- 우선순위 및 용도

### 3. RORO_Stage_Tank_Ballast
- 단계별 화물 적재 입력
- 자동 밸러스트 계산
- 목표 트림 달성

### 4. Tank_Selection_Guide
- 시나리오별 추천 탱크
- 선미/선수 트림 조정
- 미세 조정 가이드

### 5. Example_Calculation
- 실전 계산 예시
- 217t 화물 적재
- 2.0m 트림 달성

---

## 💡 사용 방법

### 기본 워크플로우

1. **Excel 파일 열기**
   ```
   LCT_BUSHRA_Package_TANK_LEVER_ARM.xlsx
   ```

2. **Tank_Catalog 확인**
   - 사용 가능한 탱크 목록
   - 각 탱크의 레버암(L_b) 확인
   - 용량 제한 확인

3. **RORO_Stage_Tank_Ballast 입력**
   - 노란색 셀에 데이터 입력:
     - W_stage(t): 화물 중량
     - x_stage(m): 화물 위치
     - TM_target(t·m): 목표 모멘트
     - Ballast_Tank: 탱크 선택

4. **자동 계산 확인**
   - ΔTM_need: 필요 모멘트
   - Ballast_t: 주입/제거 톤수
   - Ballast_time: 소요 시간
   - Check: 용량 초과 여부

5. **Tank_Selection_Guide 참고**
   - 시나리오에 맞는 탱크 선택
   - 우선순위 확인

---

## 🔧 핵심 개념

### 좌표 시스템

```
Midship 기준 (x_mid):
  BOW (선수) ←─────|─────→ STERN (선미)
              -32m   0   +32m

LCF = +0.41m (거의 midship)
```

### 레버암 (L_b)

```
L_b = x_mid - LCF

• L_b > 0: 선미 쪽 탱크 → 주입 시 선수 트림 증가
• L_b < 0: 선수 쪽 탱크 → 주입 시 선미 트림 증가
```

### 밸러스트 계산

```
1. TM_current = W × (x - LCF)
2. ΔTM = TM_target - TM_current
3. Ballast_t = ΔTM / L_b
4. Time = |Ballast_t| / Pump_rate
```

---

## 🎯 주요 탱크

| Tank | L_b (m) | Cap (t) | 용도 |
|------|---------|---------|------|
| VOID3.P/S | +3.84 | 152.1 | 대용량 선수 모멘트 |
| FW1.P/S | -25.93 | 50.6 | 강력한 선미 모멘트 |
| FW2.P/S | -18.45 | 110.0 | 중형 선미 모멘트 |
| VOIDDB2.C | +0.84 | 49.1 | 중앙 조정 |
| FWCARGO2.P/S | -3.66 | 148.4 | 선미 모멘트 |

---

## 📖 상세 문서

전체 사용 가이드는 다음 문서를 참고하세요:
```
docs/PATCH4_TANK_LEVER_ARM_GUIDE.md
```

### 주요 내용:
- 좌표 변환 상세 설명
- 시나리오별 탱크 선택
- 실전 계산 예시
- 수식 참고
- 주의사항
- 문제 해결

---

## ⚠️ 주의사항

### 1. 좌표계 일치
```
x_stage와 LCF는 반드시 같은 좌표계(midship 기준)
```

### 2. 용량 제한
```
계산된 Ballast_t가 탱크 용량 초과 시:
→ 여러 탱크 조합 사용
→ 우선순위 따라 순차 적용
```

### 3. P/S 균형
```
횡경사 방지를 위해:
→ P/S 탱크 쌍으로 균형있게 주입
```

### 4. 펌프 용량
```
LCT BUSHRA 펌프 용량: 10 t/h
→ 대용량 밸러스트 시 충분한 시간 확보
```

---

## 🔄 버전 히스토리

### Patch 4 (2025-11-06)
- ✅ 탱크 레버암 방식 도입
- ✅ 실제 LCT BUSHRA 탱크 데이터 반영
- ✅ 자동 좌표 변환
- ✅ 단계별 계산 시스템
- ✅ 시나리오 가이드
- ✅ 예시 계산

### 주요 개선점
```
Patch 3 (근사식):  Ballast ≈ 750t
Patch 4 (정확):    Ballast = 469t
절감:              281t (37%)
```

---

## 📞 지원

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

### 관련 표준
- IMO 안정성 기준
- 항만 규정
- RORO 운영 절차

---

**성공적인 변압기 운송을 기원합니다!** 🚢⚡
