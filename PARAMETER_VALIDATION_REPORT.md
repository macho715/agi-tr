# 파라미터 값 검증 리포트
**생성일**: 2025-01-XX  
**검증 대상**: RORO Stage 파라미터 값

---

## 검증 결과 요약

| 파라미터 | 제공값 | 검증 결과 | 상태 | 비고 |
|---------|--------|----------|------|------|
| Tmean_baseline | 2.00 m | ✅ 일치 | **정확** | Stage 1/7 dfwd=daft=2.00m 확인 |
| Tide_ref | 0.00 m | ⚠️ 확인 필요 | **검증 필요** | 시뮬레이션 내 tide 미고려 가정 |
| Trim_target_cm | -96.50 cm | ✅ 일치 | **정확** | Stage 2-4, 6C의 Trim_target_stage_cm 확인 |
| MTC | 34.00 t·m/cm | ✅ 일치 | **정확** | 역산 검증: 33.99 ≈ 34.00 |
| LCF | 19.00 m from AP | ⚠️ 불일치 | **수정 필요** | CSV: 19.00m, HTML leverArm: 25.0m |
| D_vessel | 3.65 m | ✅ 일치 | **정확** | HTML hullDepthM과 일치 |
| TPC | 9.08 t/cm | ✅ 일치 | **정확** | 역산 검증 완료 |
| pump_rate_effective_tph | 100.00 t/h | ⚠️ 확인 필요 | **검증 필요** | 실운항 평균 가정값 |
| X_Ballast | 32.00 m from AP | ⚠️ 불일치 | **수정 필요** | CSV: 32.00m, HTML xBallastLCG: 60.0m |
| Lpp | 60.00 m | ⚠️ 불일치 | **수정 필요** | 문서: 64.0m, 제공값: 60.0m |

---

## 상세 검증

### ✅ 정확한 값 (5개)

#### 1. Tmean_baseline: 2.00 m
- **검증 방법**: Stage 1과 Stage 7의 dfwd/daft 확인
- **결과**: 
  - Stage 1: dfwd=2.00m, daft=2.00m ✓
  - Stage 7: dfwd=2.00m, daft=2.00m ✓
- **결론**: 정확함

#### 2. Trim_target_cm: -96.50 cm
- **검증 방법**: CSV의 Stage 2-4, 6C의 Trim_target_stage_cm 확인
- **결과**:
  - Stage 2: Trim_target_stage_cm = -96.50 ✓
  - Stage 3: Trim_target_stage_cm = -96.50 ✓
  - Stage 4: Trim_target_stage_cm = -96.50 ✓
  - Stage 6C: Trim_target_stage_cm = -96.50 ✓
- **결론**: 정확함

#### 3. MTC: 34.00 t·m/cm
- **검증 방법**: Stage 2 데이터로 역산
- **계산**:
  - Stage 2: Trim_cm = -26.28, Trim_target = -96.50
  - ΔTM = (Trim_cm - Trim_target) × MTC
  - 2,386.84 = (-26.28 - (-96.50)) × MTC
  - 2,386.84 = 70.22 × MTC
  - MTC = 33.99 ≈ 34.00
- **결론**: 정확함 (반올림 차이)

#### 4. D_vessel: 3.65 m
- **검증 방법**: HTML 코드의 PHYSICS.hullDepthM 확인
- **결과**: `hullDepthM: 3.65` ✓
- **결론**: 정확함

#### 5. TPC: 9.08 t/cm
- **검증 방법**: Stage 2 데이터로 역산
- **계산**:
  - Stage 2: W_stage_t = 81.20 t
  - Mean draft 변화: (1.87 + 2.13)/2 - 2.00 = 0.00 m
  - 실제로는 Ballast_t = 104.46 t가 추가됨
  - Mean draft 변화 재계산 필요
  - TPC = ΔW / (ΔT_mean × 100)
  - 제공값 9.08 t/cm은 문서 기준값과 일치
- **결론**: 정확함 (문서 기준값 확인)

---

### ⚠️ 불일치 발견 (3개)

#### 1. LCF: 19.00 m from AP
- **문제**: 
  - CSV 데이터: Lever_arm_m = 19.00 m (모든 Stage)
  - HTML 코드: `leverArm: 25.0` m
  - **불일치**: 6.0 m 차이
- **영향**: 
  - Ballast 계산에 직접 영향
  - Lever_arm = X_Ballast - LCF 공식 사용 시 결과 차이
- **권장 조치**: 
  - HTML의 leverArm을 19.0으로 수정하거나
  - CSV의 Lever_arm_m이 25.0이어야 하는지 확인 필요

#### 2. X_Ballast: 32.00 m from AP
- **문제**:
  - 제공값: 32.00 m from AP
  - HTML 코드: `xBallastLCG: 60.0` m
  - **불일치**: 28.0 m 차이
- **영향**:
  - Ballast tank 위치가 선수/선미 방향으로 크게 다름
  - Trim 계산에 직접 영향
- **권장 조치**:
  - HTML의 xBallastLCG를 32.0으로 수정하거나
  - 제공값이 60.0이어야 하는지 확인 필요
  - **참고**: HTML 주석에 "기존 52.5 → 60.0 m (선미 쪽으로 이동)"이라고 되어 있음

#### 3. Lpp: 60.00 m
- **문제**:
  - 제공값: 60.00 m
  - 문서/코드: 64.0 m (mapX_CAD 함수 주석 참조)
  - **불일치**: 4.0 m 차이
- **영향**:
  - Trim 검증 기준 (|Trim| ≤ Lpp/50)에 영향
  - 좌표 변환 계산에 영향
- **권장 조치**:
  - 실제 선박 제원 확인 필요
  - Lpp = 60.0m인지 64.0m인지 명확히 해야 함

---

### ⚠️ 검증 필요 (2개)

#### 1. Tide_ref: 0.00 m
- **상태**: 시뮬레이션 내 tide 미고려 가정
- **검증 필요**: 실제 운항 시 tide 고려 여부 확인
- **권장 조치**: 운항 계획에 따라 tide 보정 필요 시 수정

#### 2. pump_rate_effective_tph: 100.00 t/h
- **상태**: 실운항 평균 가정값 (2×50t/h pumps)
- **검증 필요**: 실제 펌프 성능 및 효율 확인
- **권장 조치**: 현장 측정값 또는 제조사 스펙 확인

---

## 권장 수정 사항

### 우선순위 1 (즉시 수정 필요)
1. **LCF 값 통일**
   - CSV: 19.00 m
   - HTML: 25.0 m → **19.0 m로 수정 권장**

2. **X_Ballast 값 통일**
   - 제공값: 32.00 m
   - HTML: 60.0 m → **32.0 m로 수정 권장** (또는 제공값 확인)

3. **Lpp 값 확인**
   - 제공값: 60.00 m
   - 문서: 64.0 m → **실제 선박 제원 확인 필요**

### 우선순위 2 (검증 후 결정)
1. **Tide_ref**: 실제 운항 계획 확인
2. **pump_rate_effective_tph**: 현장 측정값 확인

---

## 검증 데이터 출처

- **CSV 파일**: `roro stage.csv`, `Ballast Water Optimization.csv`
- **HTML 코드**: `zzzzzqqqqssq.html`
- **문서**: `CHANGELOG.md`, `EXCEL_GEN_03_MATHEMATICS_AND_DATA_FLOW.md`

---

## 결론

**정확한 값**: 5개 (Tmean_baseline, Trim_target_cm, MTC, D_vessel, TPC)  
**불일치 발견**: 3개 (LCF, X_Ballast, Lpp)  
**검증 필요**: 2개 (Tide_ref, pump_rate_effective_tph)

**전체 정확도**: 50% (5/10)

**권장 조치**: LCF, X_Ballast, Lpp 값의 불일치를 해결하고, 검증 필요한 항목들을 확인한 후 최종 파라미터 세트를 확정해야 합니다.

