# BUSHRA Stability 수치 정리

**생성일**: 2025-01-XX
**소스**: 기존 코드/문서에서 추출 및 계산

---

## A. GM Curve용 Hydro 데이터 (Hydro_Table 시트)

**소스**: `docs/EXCEL_GEN_02_FUNCTIONS_AND_IMPLEMENTATION.md`, `agi tr.py`, `p.py`

### 형식: Disp_t / Tmean_m / Trim_m / GM_m / Draft_FWD / Draft_AFT

| Entry | Disp_t (t) | Tmean_m (m) | Trim_m (m) | GM_m (m) | Draft_FWD (m) | Draft_AFT (m) |
|-------|-----------|-------------|------------|----------|---------------|---------------|
| 1 | 2991.25 | 2.20 | 0.20 | 2.85 | 2.10 | 2.30 |
| 2 | 3208.25 | 3.18 | -0.53 | 1.68 | 2.92 | 3.45 |
| 3 | 3265.25 | 3.00 | 0.60 | 1.88 | 2.68 | 3.28 |
| 4 | 3425.25 | 3.00 | 0.70 | 1.85 | 2.65 | 3.35 |

**참고**:
- Trim_m: 양수 = AFT 깊음, 음수 = FWD 깊음
- 총 4개 entry (3~5점 요청에 대해 현재 4점 제공)
- 실제 Bushra 공식 Stability/Hydro 데이터 기반

---

## B. Ballast 탱크 데이터 (Ballast_Tanks 시트)

**소스**: `master_tanks.json`, `docs/EXCEL_GEN_02_FUNCTIONS_AND_IMPLEMENTATION.md`, `agi tr.py`

### 좌표계 변환 정보
- **AP_to_midship**: 30.151 m (Lpp/2, Lpp = 60.302 m)
- **변환 공식**: `x_mid = AP_to_midship - LCG_AP` (이론적)
- **실제 사용값**: 문서에 명시된 실측값 사용 (LCG_AP 값과 거의 일치)

### 탱크별 상세 데이터

#### FWB1 (Port & Starboard)
- **x_from_midship_m**: 57.52 m (aft of midship, 양수 = 선미 방향)
- **max_tonnage_t**: 50.57 t (실측 Weight@100%, SG=1.025 기준)
- **Air vent 직경**: 80 mm
- **use_flag**: "Y" (기본 활성)
- **참고**: Capacity_m3 = 50.6 m³, LCG_AP = 57.519 m

#### FWB2 (Port & Starboard)
- **x_from_midship_m**: 50.04 m (aft of midship, 양수 = 선미 방향)
- **max_tonnage_t**: 109.98 t (실측 Weight@100%, SG=1.025 기준)
- **Air vent 직경**: 80 mm
- **use_flag**: "Y" (기본 활성)
- **참고**: Capacity_m3 = 110.0 m³, LCG_AP = 50.038 m

#### FWCARGO1 (Port & Starboard)
- **x_from_midship_m**: 42.75 m (aft of midship, 양수 = 선미 방향)
- **max_tonnage_t**: 148.35 t (실측 Weight@100%, SG=1.000 기준, Ballast 사용 시 SG=1.025 적용)
- **Air vent 직경**: 125 mm
- **use_flag**: "N" (선택 사용, 기본 비활성)
- **참고**: Capacity_m3 = 148.4 m³, LCG_AP = 42.75 m
- **Ballast 사용 시**: SG=1.025 적용 시 max_t = 152.11 t

### 요약표

| 탱크 | x_from_midship (m) | max_t (t) | Air Vent (mm) | use_flag | 비고 |
|------|-------------------|-----------|---------------|----------|------|
| FWB1.P/S | 57.52 | 50.57 | 80 | Y | 기본 활성 |
| FWB2.P/S | 50.04 | 109.98 | 80 | Y | 기본 활성 |
| FWCARGO1.P/S | 42.75 | 148.35 (152.11*) | 125 | N | 선택 사용, *SG=1.025 기준 |

**참고**:
- x_from_midship: 양수 = 선미 방향 (aft of midship)
- max_t: 실측 Weight@100% 값 (이론적 용량이 아님)
- FWCARGO 탱크는 기본적으로 비활성("N"), 필요 시 선택 사용
- Ballast water 사용 시 SG=1.025 적용

---

## C. 캡틴 운용 한계값 (Calc 시트 - OPERATIONS 섹션)

**소스**: `Untitled-2.py`, `p.py`, `docs/EXCEL_GEN_03_MATHEMATICS_AND_DATA_FLOW.md`

### 운용 한계값

| 항목 | 파라미터명 | 값 | 단위 | 비고 |
|------|-----------|-----|------|------|
| **Max forward draft (harbour, 1st TR load 직후)** | max_fwd_draft_ops_m | **2.70** | m | 캡틴 운용 한계 |
| **Min GM (harbour ops)** | gm_target_m | **1.50** | m | 최소 GM 요구값 |
| **Linkspan 최소 Freeboard** | linkspan_freeboard_target_m | **0.28** | m | 이전 0.46m → 계획 0.28m |
| **Ramp door offset** | ramp_door_offset_m | 0.15 | m | 참고값 |

### Propeller/Shaft 조건

**현재 문서에 명시된 조건**:
- **Propeller immersion 조건**: 문서에 명시된 수치 없음
- **참고**: "TRIM이 -1.18m(FWD)로 가면 Prop 효율 NG" (캡틴 메일 기준)
- **제안**: "Aft draft ≥ 2.30m" 또는 "Immersion ≥ 70%" 등으로 수치화 필요

**추가 확인 필요**: 캡틴이 실제로 사용하는 Propeller/shaft 최소 잠김 Depth(m) 또는 "% Immersion" 조건

---

## D. Stage 6 Strength Check용 수치 (Calc 시트 - STRUCTURAL LIMITS 섹션)

**소스**: `Untitled-2.py`, `docs/EXCEL_GEN_03_MATHEMATICS_AND_DATA_FLOW.md`

### 구조 한계값

| 항목 | 파라미터명 | 값 | 단위 | 출처/비고 |
|------|-----------|-----|------|----------|
| **Max Hinge Reaction** | limit_reaction_t | **201.60** | t | Aries 허용치 |
| **Max Share Load on LCT** | limit_share_load_t | **118.80** | t | Mammoet 허용치 |
| **Max Deck Pressure** | limit_deck_press_tpm2 | **10.00** | t/m² | 사양 기준 |
| **Linkspan Contact Area** | linkspan_area_m2 | **12.00** | m² | 가정값 (Aries) |

### Stage 6 실제 계산값 (입력 필요)

**현재 Calc 시트에는 한계값만 정의되어 있으며, 실제 Stage 6 계산값은 RORO 시트에서 입력 필요:**

1. **Mammoet – Share Load (t)**
   - Stage 6 (또는 6A/6B)에서 "LCT deck에 전달되는 Share Load" 값
   - **입력 위치**: RORO 시트 Column AE (Share_Load_t)
   - **검증**: Column AF에서 limit_share_load_t (118.80t)와 비교

2. **Aries – Hinge Reaction (t)**
   - 같은 Stage에서 Linkspan Hinge Reaction 최대값
   - **입력 위치**: RORO 시트 Column AG (Hinge_Rx_t)
   - **검증**: Column AH에서 limit_reaction_t (201.60t)와 비교

3. **Deck Pressure 계산**
   - **계산식**: `Deck_Press = Share_Load / linkspan_area`
   - **자동 계산**: RORO 시트 Column AI (Deck_Press_t/m²)
   - **검증**: Column AJ에서 limit_deck_press_tpm2 (10.00 t/m²)와 비교

### 요약

- **한계값**: Calc 시트에 정의됨 (위 표 참조)
- **실제 계산값**: Stage별로 Mammoet/Aries 계산 결과를 RORO 시트에 입력 필요
- **자동 검증**: RORO 시트의 Strength Block (AE~AJ 열)에서 자동으로 OK/CHECK 표시

---

## 추가 정보

### 좌표계 참고
- **Midship 기준**: x = 0 m
- **양수 x**: 선미 방향 (aft of midship)
- **음수 x**: 선수 방향 (forward of midship)
- **LCF**: +29.29 m (midship 기준, 선미 방향)

### 용량 계산 참고
- **Ballast water SG**: 1.025 (표준)
- **Fresh water SG**: 1.000
- **실측 Weight@100%**: 이론적 용량이 아닌 실제 측정값 사용

### 데이터 출처
- **Hydro 데이터**: Excel 생성 코드 (`agi tr.py`, `p.py`)
- **Ballast 탱크**: `master_tanks.json` + 실측 데이터 (`tank_data.json` 2025-11-18)
- **운용 한계값**: Calc 시트 하드코딩 값
- **Strength 한계값**: Calc 시트 하드코딩 값 (Aries/Mammoet 사양 기반)

---

**END OF DOCUMENT**

