# PDF에서 추출해야 할 데이터 체크리스트

## 개요

`Vessel_TankPlan_64m_LandingCraft.pdf`와 같은 탱크 플랜 PDF에서 stability 계산을 위해 필요한 정보를 확인하는 가이드입니다.

## 필수 데이터 (PDF에서 추출 가능)

### 1. Master Tanks 데이터

각 탱크에 대해 다음 정보가 필요합니다:

| 필드명 | 설명 | 단위 | 필수 여부 | PDF에서 찾을 위치 |
|--------|------|------|----------|------------------|
| **Tank_ID** | 탱크 식별자 | - | 필수 | 탱크 번호/이름 (예: "T001", "NO.1 FO TANK (P)") |
| **Content** | 탱크 내용물 | - | 선택 | 탱크 용도 (예: "Fuel Oil", "Fresh Water") |
| **Capacity_m3** | 탱크 용량 | m³ | 필수 | 탱크 용량 표 (Volume 또는 Capacity) |
| **SG_Master** | 비중 (기본값) | - | 필수 | 내용물별 비중 (예: Fuel Oil = 0.821, Fresh Water = 1.000) |
| **LCG_m** | 종방향 무게중심 | m | 필수 | 탱크 중심의 종방향 위치 (Fore/Aft 기준) |
| **VCG_m** | 수직 무게중심 | m | 필수 | 탱크 중심의 수직 위치 (Keel 기준) |
| **TCG_m** | 횡방향 무게중심 | m | 필수 | 탱크 중심의 횡방향 위치 (Centerline 기준, Port=-, Starboard=+) |
| **FSM_full_tm** | 자유수면 모멘트 (만재시) | t·m | 필수 | 탱크가 만재 상태일 때의 FSM 값 |

**PDF에서 확인 방법:**
- 탱크 플랜 도면에서 탱크 위치 및 치수 확인
- 탱크 데이터 테이블에서 수치 확인
- 탱크 용량표에서 용량 및 무게중심 좌표 확인

### 2. Lightship 데이터

선박 자체의 무게 및 무게중심:

| 필드명 | 설명 | 단위 | 필수 여부 |
|--------|------|------|----------|
| **Weight** | 경하 중량 | t | 필수 |
| **LCG** | 경하 종방향 무게중심 | m | 필수 |
| **VCG** | 경하 수직 무게중심 | m | 필수 |
| **TCG** | 경하 횡방향 무게중심 | m | 선택 (기본값: 0.0) |

**PDF에서 확인 방법:**
- 선박 제원표 (Principal Particulars)
- 경하 상태 데이터 테이블
- 선박 도면의 무게중심 표시

## 선택적 데이터 (PDF에 없을 수 있음)

### 3. Hydrostatic 데이터

**파일**: `hydrostatics.csv`

이 데이터는 일반적으로 탱크 플랜 PDF에는 포함되지 않으며, 별도의 Hydrostatic 테이블 문서가 필요합니다.

| 필드명 | 설명 | 단위 |
|--------|------|------|
| **Displacement** | 배수량 | t |
| **Trim** | 트림 | m (양수 = 후미) |
| **Draft** | 흘수 | m |
| **LCB** | 부심 종방향 위치 | m |
| **VCB** | 부심 수직 위치 | m |
| **KMT** | 횡방향 메타센터 높이 | m |
| **MTC** | 트림 변화 모멘트 | t·m/cm |

**필요한 경우:**
- Stability 계산 (GZ 곡선, Trim 계산)
- IMO 검증

**없는 경우:**
- 기본 Displacement 계산만 가능
- Stability 계산 불가

### 4. KN Table 데이터

**파일**: `kn_table.csv`

이 데이터도 일반적으로 탱크 플랜 PDF에는 포함되지 않으며, 별도의 KN 곡선 테이블이 필요합니다.

| 필드명 | 설명 | 단위 |
|--------|------|------|
| **Displacement** | 배수량 | t |
| **Trim** | 트림 | m |
| **Heel_0** | 0도 기울임에서의 KN | m |
| **Heel_10** | 10도 기울임에서의 KN | m |
| **Heel_20** | 20도 기울임에서의 KN | m |
| **Heel_30** | 30도 기울임에서의 KN | m |
| **Heel_40** | 40도 기울임에서의 KN | m |
| **Heel_50** | 50도 기울임에서의 KN | m |
| **Heel_60** | 60도 기울임에서의 KN | m |

**필요한 경우:**
- GZ 곡선 계산
- IMO A.749 검증

**없는 경우:**
- Stability 계산 불가
- 기본 Displacement 계산만 가능

## PDF 확인 체크리스트

### 탱크 플랜 PDF에서 확인할 항목

- [ ] **탱크 목록**: 모든 탱크의 ID/이름
- [ ] **탱크 용량**: 각 탱크의 용량 (m³)
- [ ] **탱크 위치**: 
  - [ ] LCG (종방향 위치, m)
  - [ ] VCG (수직 위치, m)
  - [ ] TCG (횡방향 위치, m)
- [ ] **탱크 내용물**: 각 탱크의 용도 (Fuel Oil, Fresh Water 등)
- [ ] **비중 정보**: 내용물별 비중 (SG)
- [ ] **FSM 값**: 각 탱크의 자유수면 모멘트 (t·m)
- [ ] **경하 데이터**: 
  - [ ] 경하 중량 (t)
  - [ ] 경하 LCG (m)
  - [ ] 경하 VCG (m)
  - [ ] 경하 TCG (m, 선택)

### 추가 문서 필요 여부 확인

- [ ] **Hydrostatic 테이블**: 별도 문서 필요 여부 확인
- [ ] **KN 곡선 테이블**: 별도 문서 필요 여부 확인
- [ ] **선박 제원표**: Principal Particulars 문서

## 데이터 추출 우선순위

### 우선순위 1: 기본 Displacement 계산

다음 데이터만 있으면 기본 displacement 계산 가능:

1. **Master Tanks 데이터** (모든 필수 필드)
2. **Lightship 데이터** (Weight, LCG, VCG, TCG)

### 우선순위 2: Stability 계산

기본 displacement + 다음 데이터 필요:

3. **Hydrostatic CSV** (Displacement × Trim 테이블)
4. **KN Table CSV** (Displacement × Trim × Heel 테이블)

### 우선순위 3: IMO 검증

Stability 계산 + 자동 검증 (추가 데이터 불필요)

## PDF에서 데이터 추출 시 주의사항

### 좌표계 확인

- **LCG 기준점**: Fore Perpendicular (FP) 또는 Midship 기준 확인
- **VCG 기준점**: Keel (기선) 기준 확인
- **TCG 기준점**: Centerline 기준, Port/Starboard 방향 확인

### 단위 확인

- **용량**: m³ (리터나 갤런이면 변환 필요)
- **무게**: t (톤, 킬로그램이면 변환 필요)
- **거리**: m (미터, 피트나 인치면 변환 필요)
- **FSM**: t·m (톤미터)

### 데이터 검증

- 모든 탱크의 필수 필드가 있는지 확인
- 좌표 값이 합리적인 범위인지 확인 (예: LCG는 선박 길이 내)
- 용량과 FSM 값이 일치하는지 확인

## 예상 PDF 구조

일반적인 탱크 플랜 PDF는 다음 섹션을 포함합니다:

1. **Cover Page**: 선박 정보, 문서 정보
2. **General Arrangement**: 선박 전체 배치도
3. **Tank Plan**: 탱크 배치도 (도면)
4. **Tank Capacity Table**: 탱크 용량 및 무게중심 표
5. **Tank Data Table**: 상세 탱크 데이터 (LCG, VCG, TCG, FSM)
6. **Principal Particulars**: 선박 제원 (경하 데이터 포함)
7. **Appendices**: 추가 정보

## 다음 단계

PDF에서 데이터를 확인한 후:

1. **데이터 추출**: PDF 파서 또는 수동 입력으로 CSV 생성
2. **데이터 검증**: 필수 필드 및 값 범위 확인
3. **CSV 파일 생성**: 
   - `master_tanks.csv` 생성
   - `tank_mapping.csv` 생성 (조건별 매핑)
   - `condition_*.csv` 생성 (조건별 충전률)
4. **계산 실행**: CLI 또는 Streamlit으로 stability 계산

## 관련 문서

- [사용자 가이드](USER_GUIDE.md): CSV 파일 형식 상세 설명
- [기술 문서](TECHNICAL_ARCHITECTURE.md): 계산 알고리즘 설명
- [통합 설계](INTEGRATION_DESIGN.md): 시스템 구조 설명

