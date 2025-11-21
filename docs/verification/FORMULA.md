# LCF 좌표계 수정 검증 리포트

## 수정 내용

### 문제점
- MD 파일: LCF는 **F.P. 기준**
- Excel Calc 시트: LCF는 **midship 기준** (LCF_from_mid_m = 15.71 m)
- 기존 Excel 수식이 좌표계 변환 없이 사용하여 오류 발생

### 수정된 수식

#### F 컬럼 (FWD_precise_m)
**MD 파일 공식:**
```
Dfwd = Tmean - Trim_m * (1 - r)
여기서 r = LCF_from_FP / LBP
```

**좌표계 변환:**
```
LCF_from_FP = LCF_from_mid_m + LBP/2
r = (LCF_from_mid_m + LBP/2) / LBP = LCF_from_mid_m/LBP + 1/2
1 - r = 1 - (LCF_from_mid_m/LBP + 1/2) = 1/2 - LCF_from_mid_m/LBP
```

**수정된 Excel 수식:**
```
AVERAGE(O, P) - (E/100) * (0.5 - Calc!$E$41 / Calc!$E$40)
```

#### G 컬럼 (AFT_precise_m)
**MD 파일 공식:**
```
Daft = Tmean + Trim_m * r
여기서 r = LCF_from_FP / LBP
```

**좌표계 변환:**
```
r = LCF_from_mid_m/LBP + 1/2
```

**수정된 Excel 수식:**
```
AVERAGE(O, P) + (E/100) * (Calc!$E$41 / Calc!$E$40 + 0.5)
```

## 검증

### 수치 검증
- LBP = 60.30 m (Calc!$E$40)
- LCF_from_mid_m = 15.71 m (Calc!$E$41)
- LCF_from_FP = 15.71 + 60.30/2 = 15.71 + 30.15 = **45.86 m**
- r = 45.86 / 60.30 = **0.7605**

### 수식 검증
**F 컬럼:**
- 기존: `1 - (15.71 / 60.30) = 1 - 0.2605 = 0.7395` ❌ (잘못됨)
- 수정: `0.5 - (15.71 / 60.30) = 0.5 - 0.2605 = 0.2395` ✓
- 검증: `1 - 0.7605 = 0.2395` ✓ (일치)

**G 컬럼:**
- 기존: `15.71 / 60.30 = 0.2605` ❌ (잘못됨)
- 수정: `15.71 / 60.30 + 0.5 = 0.2605 + 0.5 = 0.7605` ✓
- 검증: `45.86 / 60.30 = 0.7605` ✓ (일치)

## 결론

✅ **수식 수정 완료 및 검증 통과**

Excel 수식이 MD 파일의 공식과 정확히 일치하도록 좌표계 변환이 적용되었습니다.

