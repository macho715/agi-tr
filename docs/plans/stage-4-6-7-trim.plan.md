<!-- a82758d7-7b62-44ad-aa37-fe8b812c0c53 a644ab3a-546c-4931-80e4-1d7ed2d08078 -->
# VESSEL PARTICULARS 값 업데이트 계획 (Stability Booklet 기준)

## 공식 기준값 (Vessel_Stability_Booklet 기준)

### Principal Particulars

| 항목 | 공식 정의 | 값 | 현재 Excel | 변경 |
|------|----------|-----|-----------|------|
| LOA | Length Overall | **64.00 m** | 64.00 | ✅ 유지 |
| Lpp | Length Between Perpendiculars | **60.302 m** | 60.302 | ✅ 유지 |
| Beam (Moulded) | 선체 몰드 폭 | **14.00 m** | (없음) | ➕ 추가 (선택) |
| Depth (Moulded) | D_vessel_m | **3.65 m** | 4.85 | ❌ **3.65로 수정** |
| Lightship | 경선 중량 | **770.16 t** | (없음) | ➕ 추가 (선택) |
| MTC @ Δ=1183.85t | Moment to Change Trim 1cm | **33.99 t·m/cm** | 41.47 | ❌ **33.99로 수정** |
| TPC @ Δ=1183.85t | Tonnes per cm | **7.95 t/cm** | 7.50 | ❌ **7.95로 수정** |
| LCF from AP @ Δ=1183.85t | Center of Flotation from AP | **29.91 m** | (없음) | ➕ 참고용 |
| LCF from Midship @ Δ=1183.85t | Midship 기준 (Lpp/2 = 30.151m) | **-0.24 m** | 30.91 | ❌ **-0.20로 수정** |

### Ballast 탱크 중심

| 항목 | 값 | 현재 Excel | 변경 |
|------|-----|-----------|------|
| X_Ballast (FWB1/2) | **52.53 m (from AP)** | 50.0 | ❌ **52.5로 수정** |

## 작업 항목

### Calc 시트 수정

1. **D_vessel_m**: 4.85 → **3.65 m** (INPUT CONSTANTS 섹션, Row 8)
2. **MTC_t_m_per_cm**: 41.47 → **33.99 t·m/cm** (STABILITY 섹션, Row 14)
3. **LCF_m_from_midship**: 30.91 → **-0.20 m** (STABILITY 섹션, Row 15, **중요: midship 기준 음수**)
4. **TPC_t_per_cm**: 7.50 → **7.95 t/cm** (STABILITY 섹션, Row 16)
5. **Lpp_m**: 60.302 (유지, 이미 정확함) - 현재 64.00으로 잘못 설정됨, **60.302로 수정**

### RORO_Stage_Scenarios 시트 수정

6. **X_Ballast**: 50.0 → **52.5 m** (C12 셀)

## 중요 주의사항

### LCF 좌표계 정의

- **LCF_m_from_midship**는 **Midship(= Lpp/2 = 30.151m) 기준**으로 정의
- **Aft 방향이 음수(-)**, Forward 방향이 양수(+)
- Δ=1183.85t 기준: LCF from AP = 29.91m → LCF from Midship = 29.91 - 30.151 = **-0.24 m**
- 실무 권장: **-0.20 m**로 고정 (Stage_5A 조건 기준)

### 수식 영향

- Trim 계산: `Trim_cm = (W_stage_t * (x_stage_m - LCF_from_AP_m)) / MTC`
- LCF_from_AP = LCF_from_Midship + Lpp/2 = -0.20 + 30.151 = **29.951 m**
- Lever_arm 계산: `Lever_arm_m = X_Ballast - LCF_from_AP = 52.5 - 29.951 = 22.549 m`

### 현재 파일 상태 확인

- Lpp_m이 현재 64.00으로 설정되어 있음 (잘못됨) → **60.302로 수정 필요**
- D_vessel_m이 4.85로 설정되어 있음 → **3.65로 수정 필요**
- MTC가 33.95로 설정되어 있음 → **33.99로 수정 필요**
- LCF가 0.41로 설정되어 있음 → **-0.20로 수정 필요** (좌표계 변경)

## 검증 항목

1. 모든 값이 Stability Booklet과 일치하는지 확인
2. LCF 좌표계 변환이 올바른지 확인 (Midship 기준 음수)
3. X_Ballast 값이 Tank Plan과 일치하는지 확인
4. Excel 파일 재생성 후 수식이 올바르게 작동하는지 확인
5. Lpp_m 값이 60.302로 올바르게 설정되었는지 확인

