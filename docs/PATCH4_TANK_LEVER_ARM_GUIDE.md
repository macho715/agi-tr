# Patch 4 - 탱크 레버암 방식 밸러스트 계산 가이드

## 🎯 주요 개선 사항

### ✨ 새로운 기능

1. **Tank_Catalog 시트**: 실제 탱크 데이터 (11개 탱크)
2. **좌표 자동 변환**: AP 기준 → Midship 기준
3. **정확한 레버암 계산**: L_b = x_mid - LCF
4. **RORO_Stage_Tank_Ballast**: 탱크 선택 기반 밸러스트 계산
5. **Tank_Selection_Guide**: 시나리오별 탱크 선택 가이드

---

## 🚀 실행 방법

```bash
cd C:\Users\SAMSUNG\Downloads\KZ_measurement_note\scripts
python patch4.py
```

→ 생성: `LCT_BUSHRA_Package_TANK_LEVER_ARM.xlsx`

---

## 📊 좌표 시스템

### Midship 기준 좌표 (x_mid)

```
        BOW (선수)                    STERN (선미)
         ←────────────|────────────→
      -32m         0 (midship)      +32m
                                 
    FWCARGO2.P                    FW1.P
    (x = -3.25)                   (x = +25.52)
    Negative L_b                  Positive L_b
```

### 좌표 변환 공식

```
x_mid = AP_to_midship - LCG_AP
x_mid = 32.00 - LCG_AP

예시:
• FW1.P: LCG_AP = 57.519 → x_mid = 32 - 57.519 = -25.52m (선수)
• VOID3.P: LCG_AP = 27.750 → x_mid = 32 - 27.750 = +4.25m (선미)
• FWCARGO2.P: LCG_AP = 35.250 → x_mid = 32 - 35.250 = -3.25m (선수)
```

---

## 🛢️ 탱크 카탈로그

### 주요 탱크 데이터

| Tank | LCG_AP (m) | x_mid (m) | L_b (m) | Cap (t) | Priority | 용도 |
|------|------------|-----------|---------|---------|----------|------|
| **VOID3.P** | 27.750 | +4.25 | +3.84 | 152.1 | 1 | 대용량 선수 모멘트 |
| **VOID3.S** | 27.750 | +4.25 | +3.84 | 152.1 | 1 | P/S 균형용 |
| **FW1.P** | 57.519 | -25.52 | -25.93 | 50.6 | 2 | 강력한 선미 모멘트 |
| **FW1.S** | 57.519 | -25.52 | -25.93 | 50.6 | 2 | P/S 균형용 |
| **FW2.P** | 50.038 | -18.04 | -18.45 | 110.0 | 3 | 중형 선미 모멘트 |
| **FW2.S** | 50.038 | -18.04 | -18.45 | 110.0 | 3 | P/S 균형용 |
| **VOIDDB2.C** | 30.750 | +1.25 | +0.84 | 49.1 | 4 | 중앙 조정 |
| **FWCARGO2.P** | 35.250 | -3.25 | -3.66 | 148.4 | 5 | 선미 모멘트 |
| **FWCARGO2.S** | 35.250 | -3.25 | -3.66 | 148.4 | 5 | 선미 모멘트 |

### 레버암 (L_b) 의미

```
LCF = +0.41 m (midship 기준, 선미 방향)

L_b = x_mid - LCF

• Positive L_b → LCF보다 선미 → 주입 시 선수 트림 증가
• Negative L_b → LCF보다 선수 → 주입 시 선미 트림 증가
```

**⚠️ 중요**: LCF가 거의 midship에 위치하므로:
- 선미 탱크 (VOID3): L_b 양수 작음 → 주입 시 선수 트림
- 선수 탱크 (FW1, FW2): L_b 음수 큼 → 주입 시 선미 트림

---

## 📐 레버암 방식 계산 흐름

### Step 1: 현재 모멘트 계산

```
TM_current = Σ [W_stage × (x_stage - LCF)]

예시:
Stage 1: W = 217t, x = -5m
LCF = 0.41m
TM = 217 × (-5 - 0.41) = 217 × (-5.41) = -1,174 t·m
```

### Step 2: 목표 모멘트 설정

```
원하는 트림: +0.5m (선미 방향)

TM_target = MTC × 100 × Trim_target
TM_target = 33.95 × 100 × 0.5 = 1,697.5 t·m
```

### Step 3: 필요 모멘트 보정

```
ΔTM = TM_target - TM_current
ΔTM = 1,697.5 - (-1,174) = +2,871.5 t·m
```

### Step 4: 탱크 선택 및 톤수 계산

```
필요: 선수 트림 증가 (ΔTM > 0, 양수 모멘트 필요)
선택: VOID3.P (L_b = +3.84 m, 양수)

Ballast_t = ΔTM / L_b
Ballast_t = 2,871.5 / 3.84 = 747.8 t

⚠️ 용량 초과! (152.1t < 747.8t)

올바른 해석:
ΔTM > 0 (선수 모멘트 필요)
→ L_b > 0인 탱크에 주입 (VOID3)
→ 용량 초과이므로 여러 탱크 조합

재계산 (다중 탱크):
1. VOID3.P: 152.1 t (만재)
   TM = 152.1 × 3.84 = 584.1 t·m
   
2. 잔여 ΔTM = 2,871.5 - 584.1 = 2,287.4 t·m

3. VOID3.S: 152.1 t (만재)
   TM = 152.1 × 3.84 = 584.1 t·m
   
4. 잔여 ΔTM = 2,287.4 - 584.1 = 1,703.3 t·m

5. VOIDDB2.C: 1,703.3 / 0.84 = 2,027.7 t
   ⚠️ 용량 초과 (49.1t만 가능)
   
6. 추가 탱크 필요 또는 다른 조합 검토
```

---

## 🎯 시나리오별 탱크 선택

### Scenario 1: 선수 트림 필요 (ΔTM > 0)

```
목표: 선수 trim 증가 (선수가 깊어짐)
방법: 선미 탱크에 주입 (L_b > 0)

추천 탱크:
1. VOID3.P/S (대용량, +3.84m)
2. VOIDDB2.C (중간 조정, +0.84m)

계산 예:
ΔTM = +2,000 t·m
VOID3.P: 2,000 / 3.84 = 520.8 t
→ 용량 초과 (152.1t만 가능)
→ VOID3.P + VOID3.S 조합 필요
```

### Scenario 2: 선미 트림 필요 (ΔTM < 0)

```
목표: 선미 trim 증가 (선미가 깊어짐)
방법: 선수 탱크에 주입 (L_b < 0)

추천 탱크:
1. FW1.P/S (강력, -25.93m)
2. FW2.P/S (중형, -18.45m)
3. FWCARGO2.P/S (소형, -3.66m)

계산 예:
ΔTM = -3,000 t·m
FW1.P: -3,000 / (-25.93) = 115.7 t
→ 용량 초과 (50.6t만 가능)
→ FW1.P + FW2.P 조합
```

### Scenario 3: 미세 조정

```
목표: 작은 트림 보정
방법: 소용량 탱크 사용

추천 탱크:
1. SEWAGE.C (2.8t)
2. D.O.P (2.9t)
```

---

## 📝 Excel 사용법

### 1. Tank_Catalog 시트 확인

```
1. 탱크 위치 (x_mid) 확인
2. 레버암 (L_b) 확인
3. 용량 (Cap_t) 확인
4. 우선순위 (Priority) 확인
```

### 2. RORO_Stage_Tank_Ballast 시트 작성

#### 입력 (노란색 셀):

```
B열: W_stage_t (화물 중량, 톤)
C열: x_stage_m (화물 위치, midship 기준)
H열: TM_target (목표 모멘트, t·m)
     또는 원하는 트림에서 계산
J열: Ballast_Tank (선택할 탱크 이름)
```

#### 자동 계산:

```
D열: TM = W × (x - LCF)
F열: TM_current (현재 모멘트)
I열: ΔTM_need = TM_target - TM_current
K열: Tank_Lb (선택한 탱크의 레버암)
L열: Ballast_t = ΔTM / Tank_Lb
M열: Ballast_time_h = |Ballast_t| / pump_rate
```

### 3. Tank_Selection_Guide 참고

```
시나리오 → 추천 탱크 → 탱크 이름을 J열에 입력
```

---

## 💡 실전 예시

### Example: Stage 1 화물 적재

```
입력:
• W_stage = 217 t
• x_stage = -5 m (선수 쪽)
• 현재 Tmean = 2.33 m

계산:
• TM_current = 217 × (-5 - 0.41) = -1,174 t·m
• 목표: Even-keel (Trim = 0)
• TM_target = 0 t·m
• ΔTM = 0 - (-1,174) = +1,174 t·m (선수 모멘트 필요)

탱크 선택:
• 선수 모멘트 필요 (ΔTM > 0)
• 선택: VOID3.P (L_b = +3.84 m)

밸러스트:
• Ballast_t = 1,174 / 3.84 = 305.7 t
• 용량 체크: 152.1 t < 305.7 t → 초과!

재계산 (2개 탱크):
• VOID3.P: 152.1 t (만재)
  TM_contrib = 152.1 × 3.84 = 584.1 t·m
• 잔여 ΔTM = 1,174 - 584.1 = 589.9 t·m
• VOID3.S: 589.9 / 3.84 = 153.6 t
  → 용량 체크: 152.1 t < 153.6 t → 근소하게 초과
  
최종 조정:
• VOID3.P: 152.1 t
• VOID3.S: 152.1 t
• 총 모멘트: 2 × 152.1 × 3.84 = 1,168.1 t·m ≈ 1,174 t·m ✓
• 총 시간: 15.2 h (병렬 작업)
```

---

## 🔧 수식 참고

### Tank_Catalog 시트

```excel
C열 (x_mid_m):
=32.00 - B[row]

D열 (L_b_m):
=C[row] - 0.41

G열 (Cap_t):
=E[row] * F[row]
```

### RORO_Stage_Tank_Ballast 시트

```excel
D열 (TM):
=IF(OR(B[r]="",C[r]=""),"", B[r]*(C[r]-$B$4))

I열 (ΔTM_need):
=IF(OR(F[r]="",H[r]=""),"", H[r]-F[r])

K열 (Tank_Lb):
=IF(J[r]="","", VLOOKUP(J[r],Tank_Catalog!$A:$D,4,FALSE))

L열 (Ballast_t):
=IF(OR(I[r]="",K[r]="",K[r]=0),"", I[r]/K[r])

M열 (Ballast_time_h):
=IF(OR(L[r]="",J[r]=""),"", ABS(L[r])/VLOOKUP(J[r],Tank_Catalog!$A:$H,8,FALSE))
```

---

## ⚠️ 주의사항

### 1. 좌표계 일치

```
⚠️ CRITICAL: x_stage와 LCF는 같은 좌표계여야 함!

현재 시스템:
• x: midship = 0, + aft, - forward
• LCF: +0.41 m (aft of midship)
• Tank x_mid: 자동 변환 (AP → midship)
```

### 2. 레버암 부호

```
L_b = x_mid - LCF

• L_b > 0: 탱크가 LCF보다 선미 쪽
  → 주입 시 선수 트림 증가
• L_b < 0: 탱크가 LCF보다 선수 쪽
  → 주입 시 선미 트림 증가

현재 LCT BUSHRA:
• LCF = +0.41 m (거의 midship)
• 선미 탱크: L_b > 0 (VOID3, VOIDDB2)
• 선수 탱크: L_b < 0 (FW1, FW2, FWCARGO2)
```

### 3. 계산 결과 해석

```
Ballast_t = ΔTM / L_b

부호 규칙:
• ΔTM > 0, L_b > 0 → Ballast_t > 0 → 주입
• ΔTM > 0, L_b < 0 → Ballast_t < 0 → 제거
• ΔTM < 0, L_b > 0 → Ballast_t < 0 → 제거
• ΔTM < 0, L_b < 0 → Ballast_t > 0 → 주입

실무 해석:
• 양수 = 주입
• 음수 = 제거
• 절댓값 = 톤수
```

### 4. 용량 초과

```
계산된 Ballast_t > Tank capacity:
→ 여러 탱크 조합 필요

해결 방법:
1. 우선순위 높은 탱크부터 만재
2. 잔여 ΔTM 계산
3. 다음 탱크 선택
4. 반복
```

---

## 🎓 학습 예제

### 문제: 선미 트림 2.0m 달성

```
초기 상태:
• Tmean = 2.33 m
• 화물: 없음 (TM_current = 0)

목표:
• Trim = +2.0 m (선미 방향)

계산:
1. TM_target = MTC × 100 × Trim
   = 33.95 × 100 × 2.0
   = 6,790 t·m

2. ΔTM = 6,790 - 0 = 6,790 t·m (음수 모멘트)

3. 탱크 선택: FW1.P (L_b = -25.93 m)
   Ballast_t = 6,790 / (-25.93) = -261.9 t
   → 261.9 톤 제거 또는
   → ΔTM이 음수이므로 선미 트림 증가 위해
      L_b < 0인 탱크에 주입

재해석:
   선미 트림 증가 = ΔTM < 0
   → L_b < 0인 탱크 주입
   
4. 탱크 조합:
   FW1.P: 50.6 t (만재)
     TM = 50.6 × (-25.93) = -1,312 t·m
   
   FW2.P: 110.0 t (만재)
     TM = 110.0 × (-18.45) = -2,030 t·m
   
   FWCARGO2.P: 148.4 t (만재)
     TM = 148.4 × (-3.66) = -543 t·m
     
   총 TM = -1,312 - 2,030 - 543 = -3,885 t·m

5. 아직 부족: 6,790 - 3,885 = 2,905 t·m
   
   FW1.S: 50.6 t
   FW2.S: 110.0 t
   → 추가 -3,143 t·m
   
   총: -7,028 t·m ≈ -6,790 t·m ✓
```

---

## 🔄 기존 시스템과 비교

### Patch 3 (근사식):

```
Ballast_t ≈ |Trim_m| × 50 × TPC
Ballast_t ≈ 2.0 × 50 × 7.5 = 750 t
```

### Patch 4 (정확한 레버암):

```
실제 필요량: 469.0 t (탱크 조합)
차이: 750 - 469 = 281 t (37% 과다!)
```

**결론**: 레버암 방식이 훨씬 정확하고 경제적!

---

## 📞 문의

문제 발생 시:
1. Tank_Catalog 시트의 좌표 확인
2. Calc 시트의 LCF 값 확인
3. 좌표계 일치 여부 확인

기술 지원:
- MACHO-GPT System
- Samsung C&T Logistics Team

---

**모든 준비 완료!** patch4.py를 실행하여 정확한 탱크 기반 밸러스트 계산을 시작하세요. 🚀
