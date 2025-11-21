# RORO_Stage_Scenarios 시트 로직 및 알고리즘 보고서

**작성일:** 2025-01-XX  
**프로젝트:** LCT BUSHRA - AGI Transformers Transportation  
**시트명:** RORO_Stage_Scenarios

---

## Executive Summary

RORO_Stage_Scenarios 시트는 10개의 로딩 스테이지에 대한 선박의 Trim(트림), Draft(흘수), Ballast(밸러스트) 계산을 수행하는 핵심 계산 시트입니다. Lever-arm ballast 계산 모델을 기반으로 하며, 각 스테이지별로 선박의 안정성과 운항 한계를 검증합니다.

---

## 시트 구조

### 1. 기본 레이아웃

| 영역 | 행 범위 | 설명 |
|------|---------|------|
| 제목 | Row 1 | "RORO Stage Scenarios – LCT BUSHRA / AGI TR" |
| Baseline Inputs | Row 5 | Tmean_baseline, Tide_ref 입력 |
| Hydrostatic References | Rows 8-12 | MTC, LCF, Lpp, D_vessel, TPC, Pump rate, X_Ballast |
| 헤더 행 | Row 14 | 컬럼 헤더 (A~AD, 총 30개 컬럼) |
| 데이터 행 | Rows 15-24 | 10개 Stage 데이터 |

### 2. Stage 정의 (10개)

| Stage | 설명 | W_stage_t (기본값) | x_stage_m (기본값) |
|-------|------|-------------------|-------------------|
| Stage 1 | Empty condition (Baseline) | 0.0 | 0.0 |
| Stage 2 | SPMT 1st entry on ramp (~30% reaction) | 65.0 | -10.0 |
| Stage 3 | ~50% on ramp (Half reaction) | 110.0 | -6.85 |
| Stage 4 | Full on ramp / Break-even (1 unit full weight) | 217.0 | -3.85 |
| Stage 5 | Deck full load (217t × 2) | 434.0 | 15.27 |
| Stage 5A-1 (At-Limit) | Ballast at maximum limit | 527.57 | 24.43 |
| Stage 5A-2 (Optimized) | Recommended trim optimization | 579.97 | 24.01 |
| Stage 5A-3 (Max-Safety) | Conservative variation | 606.17 | 25.14 |
| Stage 6 | TR1 @ final + TR2 full on bow ramp | 434.0 | 0.63 |
| Stage 7 | TR1 @ final + TR2 on ramp + AFT ballast | 434.0 | 0.63 |

---

## 핵심 계산 알고리즘

### 3. 기본 Trim 계산 체인

#### 3.1 Column D: TM (t·m) - Trimming Moment
```
=IF(OR(B{row}="", C{row}="", $C$9=""), "", B{row} * (C{row} - $C$9))
```

**물리적 의미:**
- **TM** = W_stage_t × (x_stage_m - LCF)
- 화물 무게와 무게 중심 위치로 인한 트리밍 모멘트 계산
- LCF (Longitudinal Center of Flotation) 기준으로 모멘트 계산

**입력:**
- B{row}: W_stage_t (Stage별 화물 무게, t)
- C{row}: x_stage_m (Stage별 무게 중심 위치, m, midship=0)
- $C$9: LCF (Longitudinal Center of Flotation, m)

**출력:** Trimming Moment (t·m)

---

#### 3.2 Column E: Trim_cm (cm)
```
=IF(OR(D{row}="", OR($C$8="", $C$8=0)), "", D{row} / $C$8)
```

**물리적 의미:**
- **Trim_cm** = TM / MTC
- 트리밍 모멘트를 MTC로 나누어 트림을 센티미터 단위로 계산

**입력:**
- D{row}: TM (t·m)
- $C$8: MTC (Moment to Change Trim, t·m/cm)

**출력:** Trim in centimeters (cm)

---

#### 3.3 Column F: Trim_m (m)
```
=IF(E{row}="", "", E{row} / 100)
```

**물리적 의미:**
- **Trim_m** = Trim_cm / 100
- 센티미터를 미터로 변환

**입력:**
- E{row}: Trim_cm (cm)

**출력:** Trim in meters (m)

---

### 4. Ballast 계산 알고리즘 (Lever-arm Model)

#### 4.1 Column G: Trim_target_cm
**입력 셀** (사용자 입력 또는 기본값)

**Stage별 기본값:**
- Stage 1: 0.0 cm
- Stage 2: -64.12 cm
- Stage 3: -100.16 cm
- Stage 4: -181.89 cm
- Stage 5: -163.68 cm
- Stage 5A-1: -121.0 cm
- Stage 5A-2: -96.5 cm (Optimized)
- Stage 5A-3: -84.34 cm
- Stage 6: -96.5 cm
- Stage 7: -96.5 cm

---

#### 4.2 Column H: ΔTM_cm_tm (t·m)
```
=IF(OR(ISERROR(MTC), ISERROR(TRIM5_CM), G{row}=""), "", 
    ROUND(MTC * (ABS(TRIM5_CM) - ABS(G{row})), 2))
```

**물리적 의미:**
- **ΔTM_cm_tm** = MTC × (|TRIM5_CM| - |Trim_target_cm|)
- Stage 5의 트림과 목표 트림의 차이를 모멘트로 변환
- 필요한 트림 보정량 계산

**입력:**
- MTC: Named range (t·m/cm)
- TRIM5_CM: Named range (Stage 5의 Trim_cm)
- G{row}: Trim_target_cm (목표 트림, cm)

**출력:** Required trimming moment change (t·m)

---

#### 4.3 Column I: Lever_arm_m (m)
```
=IF(OR(ISBLANK($C$12), ISBLANK($C$9), ISERROR($C$9)), "", 
    ROUND($C$12 - $C$9, 2))
```

**물리적 의미:**
- **Lever_arm_m** = X_Ballast - LCF
- 밸러스트 탱크 위치와 LCF 사이의 거리
- 밸러스트 무게가 트림에 미치는 영향의 레버 암

**입력:**
- $C$12: X_Ballast (밸러스트 탱크 무게 중심 위치, m)
- $C$9: LCF (Longitudinal Center of Flotation, m)

**출력:** Lever arm (m)

---

#### 4.4 Column J: Ballast_t_calc (t)
```
=IF(OR(H{row}="", I{row}=""), "", ROUND(H{row} / I{row}, 2))
```

**물리적 의미:**
- **Ballast_t_calc** = ΔTM_cm_tm / Lever_arm_m
- 필요한 트림 보정을 위한 밸러스트 무게 계산
- Lever-arm 모델 기반 정확한 계산

**입력:**
- H{row}: ΔTM_cm_tm (t·m)
- I{row}: Lever_arm_m (m)

**출력:** Required ballast weight (t)

---

#### 4.5 Column K: Ballast_time_h_calc (h)
```
=IF(OR(J{row}="", $C$11="", $C$11=0, ISERROR($C$11)), "", 
    ROUND(J{row} / $C$11, 2))
```

**물리적 의미:**
- **Ballast_time_h_calc** = Ballast_t_calc / PumpRate
- 밸러스트 펌핑에 소요되는 시간 계산

**입력:**
- J{row}: Ballast_t_calc (t)
- $C$11: PumpRate (펌프 속도, t/h)

**출력:** Ballast pumping time (hours)

---

### 5. Rule-of-Thumb Ballast 계산 (비교용)

#### 5.1 Column L: Ballast_t (t)
```
=IF(OR(F{row}="", OR($C$10="", $C$10=0)), "", 
    ROUND(ABS(F{row}) * 50 * $C$10, 2))
```

**물리적 의미:**
- **Ballast_t** = |Trim_m| × 50 × TPC
- 경험식 기반 밸러스트 무게 계산 (Lever-arm 모델과 비교용)
- 50은 Lpp/100의 근사값

**입력:**
- F{row}: Trim_m (m)
- $C$10: TPC (Tons Per Centimeter, t/cm)

**출력:** Estimated ballast weight by rule-of-thumb (t)

---

#### 5.2 Column M: Ballast_time_h (h)
```
=IF(OR(L{row}="", $C$11="", $C$11=0, ISERROR($C$11)), "", 
    ROUND(L{row} / $C$11, 2))
```

**물리적 의미:**
- **Ballast_time_h** = Ballast_t / PumpRate
- 경험식 기반 밸러스트 펌핑 시간

**입력:**
- L{row}: Ballast_t (t)
- $C$11: PumpRate (t/h)

**출력:** Estimated ballast pumping time (hours)

---

### 6. Trim 검증

#### 6.1 Column N: Trim_Check
```
=IF(F{row}="", "", IF(ABS(F{row}) <= ($F$8/50), "OK", "EXCESSIVE"))
```

**물리적 의미:**
- **Trim_Check**: 트림이 허용 한계 내인지 검증
- 기준: |Trim_m| ≤ Lpp / 50
- Lpp/50은 일반적인 트림 한계 기준

**입력:**
- F{row}: Trim_m (m)
- $F$8: Lpp (Length between perpendiculars, m)

**출력:** "OK" 또는 "EXCESSIVE"

---

### 7. Draft 계산

#### 7.1 Column O: Dfwd_m (Forward Draft, m)
```
=IF(OR($D$5="", F{row}=""), "", $D$5 - F{row}/2)
```

**물리적 의미:**
- **Dfwd_m** = Tmean_baseline - Trim_m/2
- 평균 흘수에서 트림의 절반을 빼서 선수 흘수 계산
- Trim이 음수(선수 하강)이면 Dfwd 증가

**입력:**
- $D$5: Tmean_baseline (평균 흘수 기준값, m)
- F{row}: Trim_m (m, 음수 = 선수 하강)

**출력:** Forward draft (m)

---

#### 7.2 Column P: Daft_m (Aft Draft, m)
```
=IF(OR($D$5="", F{row}=""), "", $D$5 + F{row}/2)
```

**물리적 의미:**
- **Daft_m** = Tmean_baseline + Trim_m/2
- 평균 흘수에서 트림의 절반을 더해 선미 흘수 계산
- Trim이 음수(선수 하강)이면 Daft 감소

**입력:**
- $D$5: Tmean_baseline (m)
- F{row}: Trim_m (m)

**출력:** Aft draft (m)

---

### 8. Height 계산 (Keel 기준)

#### 8.1 Column Q: FWD_Height_m
```
=IF(O{row}="", "", $F$9 - O{row} + $G$5)
```

**물리적 의미:**
- **FWD_Height_m** = D_vessel - Dfwd_m + Tide_ref
- 선수 갑판 높이 (keel 기준)
- 조석을 고려한 실제 갑판 높이

**입력:**
- $F$9: D_vessel (선박 깊이, m)
- O{row}: Dfwd_m (선수 흘수, m)
- $G$5: Tide_ref (조석 기준값, m)

**출력:** Forward deck height above keel (m)

---

#### 8.2 Column R: AFT_Height_m
```
=IF(P{row}="", "", $F$9 - P{row} + $G$5)
```

**물리적 의미:**
- **AFT_Height_m** = D_vessel - Daft_m + Tide_ref
- 선미 갑판 높이 (keel 기준)

**입력:**
- $F$9: D_vessel (m)
- P{row}: Daft_m (선미 흘수, m)
- $G$5: Tide_ref (m)

**출력:** Aft deck height above keel (m)

---

## Captain Req 확장 컬럼 (v10)

### 9. Column T~AD: Captain Requirements

#### 9.1 Column T (20): GM(m)
```
=IF(D{row}="", "", VLOOKUP(D{row},Hydro_Table!$A:$D,4,1))
```

**물리적 의미:**
- **GM**: Metacentric Height (초심고)
- Hydro_Table에서 Displacement에 따른 GM 값 조회
- 선박 안정성 지표

**입력:**
- D{row}: TM (t·m) - 실제로는 Displacement를 사용해야 하지만 현재는 TM 사용
- Hydro_Table!$A:$D: Displacement, Tmean, Trim, GM 테이블

**출력:** GM (m) 또는 #N/A (테이블에 해당 값이 없을 경우)

**참고:** 현재 수식이 TM을 사용하고 있어 #N/A가 발생할 수 있음. Displacement 값을 사용하도록 수정 필요.

---

#### 9.2 Column U (21): Fwd Draft(m)
```
=IF(O{row}="", "", O{row})
```

**물리적 의미:**
- Column O (Dfwd_m)의 복사본
- Captain 요구사항 검증용

**출력:** Forward draft (m)

---

#### 9.3 Column V (22): vs 2.70m
```
=IF(U{row}="", "", IF(U{row}<=Calc!$E$18,"OK","NG"))
```

**물리적 의미:**
- **Draft Limit Check**: 선수 흘수가 2.70m 이하인지 검증
- Summer draft limit 기준
- Calc!$E$18: Summer draft limit (2.70m)

**입력:**
- U{row}: Fwd Draft(m)
- Calc!$E$18: Summer draft limit (m)

**출력:** "OK" 또는 "NG"

---

#### 9.4 Column W (23): De-ballast Qty(t)
```
=IF(J{row}="", "", J{row})
```

**물리적 의미:**
- Column J (Ballast_t_calc)의 복사본
- De-ballast 필요량 (음수 값은 ballast 추가를 의미)

**출력:** Ballast quantity (t)

---

#### 9.5 Column X (24): Timing
**빈 셀** (사용자 입력용)
- 타이밍 정보 입력

---

#### 9.6 Column Y (25): Linkspan_Freeboard_m
```
=IF(O{row}="", "", Calc!$E$19 - O{row} + $G$5 - Calc!$E$20)
```

**물리적 의미:**
- **Linkspan Freeboard**: 램프 연결부의 여유 높이
- Calc!$E$19: Linkspan deck height (m)
- Calc!$E$20: Linkspan connector height (m)
- $G$5: Tide_ref (m)

**계산식:**
- Linkspan_Freeboard = Linkspan_deck_height - Dfwd + Tide - Connector_height

**입력:**
- O{row}: Dfwd_m (m)
- Calc!$E$19: Linkspan deck height (m)
- Calc!$E$20: Linkspan connector height (m)
- $G$5: Tide_ref (m)

**출력:** Linkspan freeboard (m, 음수 가능)

---

#### 9.7 Column Z (26): Clearance_Check
```
=IF(Y{row}="", "", IF(Y{row}>=Calc!$E$21,"OK","<0.28m CHECK"))
```

**물리적 의미:**
- **Freeboard Limit Check**: Linkspan freeboard가 0.28m 이상인지 검증
- Calc!$E$21: Minimum freeboard limit (0.28m)

**입력:**
- Y{row}: Linkspan_Freeboard_m (m)
- Calc!$E$21: Minimum freeboard limit (m)

**출력:** "OK" 또는 "<0.28m CHECK"

---

#### 9.8 Column AA (27): GM_calc
```
=T{row}
```

**물리적 의미:**
- Column T (GM)의 복사본
- GM 계산값

**출력:** GM (m) 또는 #N/A

---

#### 9.9 Column AB (28): GM_Check
```
=IF(AA{row}="", "", IF(AA{row}>=Calc!$E$22,"OK","NG"))
```

**물리적 의미:**
- **GM Limit Check**: GM이 최소 허용값 이상인지 검증
- Calc!$E$22: Minimum GM limit (m)

**입력:**
- AA{row}: GM_calc (m)
- Calc!$E$22: Minimum GM limit (m)

**출력:** "OK" 또는 "NG"

---

#### 9.10 Column AC (29): Prop Imm(%) (Propeller Immersion)
```
=IF(P{row}="", "", ($P{row}-2.10)/1.25*100)
```

**물리적 의미:**
- **Propeller Immersion**: 프로펠러 침수율 계산
- 2.10m: 프로펠러 축 높이 (keel 기준)
- 1.25m: 프로펠러 직경
- 음수 값은 프로펠러가 수면 위에 있음을 의미

**계산식:**
- Prop_Imm = (Daft - Propeller_axis_height) / Propeller_diameter × 100

**입력:**
- P{row}: Daft_m (선미 흘수, m)
- 2.10: 프로펠러 축 높이 (m)
- 1.25: 프로펠러 직경 (m)

**출력:** Propeller immersion percentage (%, 음수 가능)

---

#### 9.11 Column AD (30): Vent_Time_h (Ventilation Time)
```
=IF(W{row}>0, W{row}/45, "-")
```

**물리적 의미:**
- **Ventilation Time**: 환기 시간 계산
- De-ballast Qty를 환기 속도(45 t/h)로 나눔
- De-ballast Qty가 0 이하이면 "-" 표시

**입력:**
- W{row}: De-ballast Qty(t) (t)
- 45: Ventilation rate (t/h)

**출력:** Ventilation time (hours) 또는 "-"

---

## 데이터 흐름도

```
[Inputs]
  ├─ W_stage_t (B) ──┐
  ├─ x_stage_m (C) ──┤
  └─ LCF (C9) ───────┼─→ TM (D) = W × (x - LCF)
                     │
  MTC (C8) ──────────┼─→ Trim_cm (E) = TM / MTC
                     │
                     └─→ Trim_m (F) = Trim_cm / 100
                                        │
                                        ├─→ Dfwd_m (O) = Tmean - Trim_m/2
                                        ├─→ Daft_m (P) = Tmean + Trim_m/2
                                        ├─→ FWD_Height_m (Q) = D_vessel - Dfwd + Tide
                                        └─→ AFT_Height_m (R) = D_vessel - Daft + Tide

[Ballast Calculation]
  TRIM5_CM ──┐
  Trim_target_cm (G) ──┼─→ ΔTM_cm_tm (H) = MTC × (|TRIM5| - |Target|)
                       │
  X_Ballast (C12) ──┐  │
  LCF (C9) ────────┼─→ Lever_arm_m (I) = X_Ballast - LCF
                   │   │
                   └───┼─→ Ballast_t_calc (J) = ΔTM / Lever_arm
                       │
  PumpRate (C11) ──────┼─→ Ballast_time_h_calc (K) = Ballast_t / PumpRate

[Captain Req Checks]
  Dfwd_m (O) ──────────→ vs 2.70m (V) = IF(Dfwd ≤ 2.70, "OK", "NG")
  Linkspan_Freeboard (Y) ─→ Clearance_Check (Z) = IF(Freeboard ≥ 0.28, "OK", "<0.28m CHECK")
  GM (T) ──────────────→ GM_Check (AB) = IF(GM ≥ Min_GM, "OK", "NG")
```

---

## Named Ranges

시트에서 사용되는 Named Ranges:

| Name | 참조 위치 | 설명 |
|------|-----------|------|
| MTC | 'RORO_Stage_Scenarios'!$C$8 | Moment to Change Trim (t·m/cm) |
| LCF | 'RORO_Stage_Scenarios'!$C$9 | Longitudinal Center of Flotation (m) |
| PumpRate | 'RORO_Stage_Scenarios'!$C$11 | Ballast pump rate (t/h) |
| X_Ballast | 'RORO_Stage_Scenarios'!$C$12 | Ballast tank CG position (m) |
| TRIM5_CM | 'RORO_Stage_Scenarios'!$E${trim5_row} | Stage 5의 Trim_cm 값 |

---

## 주요 물리적 관계식

### 1. Trim 계산
```
TM = W × (x - LCF)
Trim_cm = TM / MTC
Trim_m = Trim_cm / 100
```

### 2. Draft 계산
```
Dfwd = Tmean - Trim_m / 2
Daft = Tmean + Trim_m / 2
```

### 3. Ballast 계산 (Lever-arm Model)
```
ΔTM = MTC × (|Trim_current| - |Trim_target|)
Lever_arm = X_Ballast - LCF
Ballast_t = ΔTM / Lever_arm
```

### 4. Height 계산
```
Height = D_vessel - Draft + Tide
```

### 5. Freeboard 계산
```
Freeboard = Deck_height - Draft + Tide - Connector_height
```

### 6. Propeller Immersion
```
Prop_Imm% = (Daft - Prop_axis_height) / Prop_diameter × 100
```

---

## 검증 기준 (Limits)

| 항목 | 컬럼 | 기준값 | 위치 | 설명 |
|------|------|--------|------|------|
| Draft Limit | V | ≤ 2.70m | Calc!$E$18 | Summer draft limit |
| Freeboard Limit | Z | ≥ 0.28m | Calc!$E$21 | Minimum linkspan freeboard |
| GM Limit | AB | ≥ Min_GM | Calc!$E$22 | Minimum metacentric height |
| Trim Limit | N | ≤ Lpp/50 | $F$8/50 | Maximum allowable trim |

---

## 알려진 이슈 및 개선 사항

### 1. GM 계산 이슈
- **문제:** Column T의 GM 계산이 TM 값을 사용하여 VLOOKUP을 수행
- **원인:** Displacement 값이 필요하지만 TM을 사용 중
- **해결:** Displacement 값을 계산하여 사용하도록 수정 필요

### 2. Stage 5A-2 Dfwd 값 불일치
- **문제:** 현재 계산값 2.92m vs 요구값 2.32m
- **원인:** Tmean_baseline 또는 Trim 값 조정 필요
- **해결:** P2 패치 적용 필요

### 3. Excel 수식 계산
- **문제:** Python으로 생성된 파일에서 수식이 계산되지 않음
- **원인:** Excel이 수식을 계산하지 않은 상태
- **해결:** Excel에서 파일을 열어 저장하면 자동 계산됨

---

## 참고 문서

- **구현 파일:** `scripts/main/build_bushra_agi_tr_from_scratch_patched.py`
- **함수:** `create_roro_sheet()` (line 425)
- **확장 함수:** `extend_roro_captain_req()` (line 750)
- **설계 문서:** `patcaah.md`
- **이론 설명:** `captain.md`

---

**작성 완료일:** 2025-01-XX  
**버전:** v10 (Captain Req 확장 포함)

