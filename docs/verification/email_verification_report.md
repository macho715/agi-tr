# 이메일 값 검증 보고서

## 검증 결과 요약

### 1. Ballast Weight
- **이메일**: 200.00 tons
- **코드 현재값**: 250.0 t
- **역산 필요 Ballast**: 250.06 t (이메일 Trim/Draft 값 기준)
- **상태**: **불일치** (이메일 200t는 Trim/Draft 값과 일관성 없음)

### 2. Stage 6A_Critical Trim
- **이메일**: Even Keel (-0.10 m)
- **코드 계산값 (250t 기준)**: -0.26 m
- **코드 계산값 (200t 기준)**: -0.62 m
- **이메일 값 역산 LCG**: -0.34 m
- **상태**: **불일치** (200t 기준 -0.62m, 250t 기준 -0.26m)

### 3. Fwd Draft
- **이메일**: 2.77 m
- **코드 계산값 (250t 기준)**: 3.48 m
- **코드 계산값 (200t 기준)**: 3.60 m
- **상태**: **불일치** (큰 차이)

### 4. Freeboard
- **이메일**: +0.88 m
- **수학적 검증**: D_vessel(3.65m) - Dfwd(2.77m) = 0.88m ✓
- **코드 계산값 (250t 기준)**: 0.17 m
- **코드 계산값 (200t 기준)**: 0.05 m
- **상태**: **수학적으로 일치** (Dfwd가 2.77m라면 Freeboard는 0.88m)

### 5. Frame Range
- **이메일**: Frame 48-65 (Aft tanks FWB1/2)
- **코드**: Frame 55 (x_bal = 25.0m)
- **상태**: **일치** (Frame 55는 48-65 범위 내)

### 6. Stern Depth during Pre-ballasting
- **이메일**: Maintain >4.00 m depth at stern
- **코드 계산값 (200t 기준, Stage 5_PreBallast)**: 4.10 m
- **상태**: **OK** (>4.00m 만족)

## 주요 발견사항

### 불일치 원인 분석

1. **이메일의 Trim(-0.10m)과 Draft(2.77m) 값이 서로 일관성 없음**
   - 이메일 값으로 역산한 Total Weight: 310.05 t
   - 실제 필요한 Weight (TR1 280t + TR2 280t): 560 t
   - **차이**: -249.95 t (물리적으로 불가능)

2. **이메일의 Ballast 200t는 Trim/Draft 값과 맞지 않음**
   - Trim(-0.10m)과 Draft(2.77m)에 맞는 Ballast: **250.06 t**
   - 이메일 Ballast: 200.00 t
   - **차이**: 50.06 t

3. **현재 코드(250t)가 이메일 Trim/Draft 값에 더 근접**
   - 코드 250t 기준: Trim -0.26m, Dfwd 3.48m
   - 코드 200t 기준: Trim -0.62m, Dfwd 3.60m
   - 이메일: Trim -0.10m, Dfwd 2.77m

## 결론

**이메일의 값들은 서로 일관성이 없습니다:**
- Ballast 200t와 Trim(-0.10m), Draft(2.77m)는 동시에 만족할 수 없음
- Trim(-0.10m)과 Draft(2.77m)에 맞는 Ballast는 약 **250t**
- 현재 코드의 250t 설정이 이메일의 Trim/Draft 목표값에 더 근접

## 권장사항

1. **Ballast Weight**: 현재 코드의 **250t 유지** (이메일 Trim/Draft 목표에 더 근접)
2. **이메일 수정 필요**: Ballast 200t → 250t로 변경
3. **또는**: Trim/Draft 목표값 재검토 필요

