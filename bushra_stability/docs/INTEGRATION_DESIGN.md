# Stability Engine 통합 설계 문서

## 시스템 비교 분석

### 기존 src 시스템 (displacement.py)

**데이터 모델:**
- `WeightItem`: name, weight, lcg, vcg, tcg, fsm, group
- `DisplacementResult`: total_weight, lcg, vcg, tcg, total_fsm

**기능:**
- Excel 워크북 직접 읽기
- 기본 displacement 계산 (무게중심 집계)
- 단순하고 명확한 API

**제한사항:**
- Hydrostatic 데이터 없음
- GZ/Trim 계산 없음
- IMO 검증 없음

### 이전 버전 (참고용 - 통합 완료)

**참고**: `stability_engine_v21_noscipy.py`는 통합 작업 전의 독립 실행 파일이었으며, 모든 기능이 현재 `src/` 폴더의 모듈로 분산되었습니다. 패치 노트는 `docs/PATCH_NOTES.md`에 보관되어 있습니다.

**이전 데이터 모델:**
- `Lightship`: weight_t, lcg_m, vcg_m, tcg_m
- `HydroEngine`: 1D/2D 보간 (numpy 기반)
- `Vessel`: tanks_df, extra_df

**이전 기능:**
- CSV 기반 입력
- Hydrostatic 보간 (1D)
- KN 곡선 계산 (2D bilinear)
- GZ 계산
- Trim 계산 (단일 반복)
- IMO A.749 검증
- Excel/PDF 리포트

**제한사항 (해결됨):**
- SciPy 없이 구현 (정확도 제한) → 현재는 SciPy 기반으로 개선
- Trim 반복 없음 → 현재는 반복 계산 지원
- Excel 직접 읽기 없음 → 현재는 Excel/CSV 모두 지원

### PATCH_NOTES.md (SciPy 버전 패치)

**개선사항:**
- `RegularGridInterpolator` 사용 (2D/3D 보간)
- Trim 반복 계산 (iterative)
- Simpson 적분 (IMO 검증)
- 더 정확한 보간

**핵심 수정 (현재 구현에 반영됨):**
- RGI 입력 형식: `[[disp, trim]]` (2D)
- 3D RGI: `[[disp, trim, heel]]` (KN 계산)
- 피벗 그리드 정렬 및 재인덱스
- Trim 공식 단위 일관화

자세한 내용은 `docs/PATCH_NOTES.md` 참조.

## 통합 아키텍처 설계

### 모듈 구조

```
src/
├── displacement.py      # [기존] 기본 displacement 계산
├── excel_reader.py      # [기존] Excel 워크북 읽기
├── csv_reader.py        # [신규] CSV 파일 읽기 (master, condition)
├── hydrostatic.py       # [신규] HydroEngine (SciPy 기반)
├── stability.py         # [신규] GZ/Trim 계산
├── imo_check.py         # [신규] IMO A.749 검증
├── reporting.py         # [신규] Excel/PDF 리포트 생성
├── cli.py               # [확장] 고급 옵션 추가
└── streamlit_app.py     # [확장] 고급 기능 UI
```

### 데이터 모델 통합

**공통 데이터 모델:**
```python
# 기존 WeightItem 유지 (호환성)
@dataclass
class WeightItem:
    name: str
    weight: float
    lcg: Optional[float]
    vcg: Optional[float]
    tcg: Optional[float]
    fsm: float = 0.0
    group: Optional[str] = None

# Lightship을 WeightItem으로 변환 가능
def lightships_to_weight_items(ls: Lightship) -> WeightItem:
    return WeightItem(
        name="Light Ship",
        weight=ls.weight_t,
        lcg=ls.lcg_m,
        vcg=ls.vcg_m,
        tcg=ls.tcg_m,
        fsm=0.0
    )

# DisplacementResult 확장
@dataclass
class StabilityResult(DisplacementResult):
    """Extended result with stability calculations."""
    kg_corrected: float
    kmt: float
    gm: float
    trim: float
    draft_mean: float
    draft_fwd: float
    draft_aft: float
    kn_curve: Dict[int, float]  # heel_deg -> KN
    gz_curve: Dict[int, float]  # heel_deg -> GZ
    imo_check: Dict[str, Any]
```

### API 설계

**계층화된 API:**

```python
# Level 1: 기본 displacement (기존)
from src.displacement import calculate_displacement, WeightItem

# Level 2: Stability 계산 (신규)
from src.stability import calculate_stability, StabilityResult
from src.hydrostatic import HydroEngine

# Level 3: 전체 워크플로우
from src.vessel import Vessel  # 통합 클래스
```

**Vessel 클래스 (통합 인터페이스):**

```python
class Vessel:
    def __init__(self, name: str, lightships: List[WeightItem], hydro: HydroEngine):
        """Initialize vessel with lightships and hydrostatic data."""
        
    def add_weight_items(self, items: List[WeightItem]):
        """Add weight items (from Excel or CSV)."""
        
    def calculate_displacement(self) -> DisplacementResult:
        """Basic displacement calculation (uses existing logic)."""
        
    def calculate_stability(self, heel_angles: Optional[List[int]] = None) -> StabilityResult:
        """Full stability calculation with GZ/Trim/IMO."""
        
    def export_report(self, format: str = "json") -> str:
        """Export stability report."""
```

### 데이터 흐름

```
[입력 소스]
    ├─ Excel 워크북 → excel_reader → List[WeightItem]
    └─ CSV 파일들 → csv_reader → List[WeightItem]

[계산 엔진]
    List[WeightItem]
        ↓
    calculate_displacement() → DisplacementResult
        ↓
    [HydroEngine 보간]
        ↓
    calculate_stability() → StabilityResult
        ↓
    [IMO 검증]
        ↓
    StabilityResult (완전한 결과)

[출력]
    StabilityResult
        ├─ JSON/CSV (CLI)
        ├─ Excel 리포트 (reporting.py)
        ├─ PDF 리포트 (reporting.py)
        └─ Streamlit UI
```

## 통합 전략

### 1. 하위 호환성 유지

- 기존 `displacement.py` API 유지
- 기존 테스트 통과 보장
- 기존 CLI/Streamlit 동작 유지

### 2. 점진적 확장

- 기본 displacement 계산은 기존 로직 사용
- Stability 계산은 선택적 기능
- HydroEngine이 없으면 기본 계산만 수행

### 3. 데이터 소스 통합

- Excel 워크북 → `excel_reader.py` (기존)
- CSV 파일들 → `csv_reader.py` (신규)
- 두 형식 모두 `List[WeightItem]`으로 변환

### 4. 모듈 독립성

- 각 모듈은 독립적으로 테스트 가능
- 의존성 최소화
- 선택적 기능은 optional import

## 구현 우선순위

1. **Phase 1: 핵심 모듈**
   - hydrostatic.py (SciPy 기반)
   - stability.py (GZ/Trim 계산)

2. **Phase 2: 검증 및 리포트**
   - imo_check.py
   - reporting.py

3. **Phase 3: 데이터 통합**
   - csv_reader.py
   - excel_reader.py 확장

4. **Phase 4: 인터페이스 통합**
   - cli.py 확장
   - streamlit_app.py 확장

5. **Phase 5: 통합 클래스**
   - Vessel 클래스 (통합 인터페이스)

## API 호환성

### 기존 코드 호환성

```python
# 기존 코드는 그대로 동작
from src.displacement import calculate_displacement, WeightItem

items = [...]  # 기존 방식
result = calculate_displacement(items)  # 동일하게 동작
```

### 새로운 기능 사용

```python
# 새로운 기능은 선택적 사용
from src.hydrostatic import HydroEngine
from src.stability import calculate_stability

hydro = HydroEngine("hydrostatics.csv", "kn_table.csv")
stability_result = calculate_stability(items, hydro)
```

### 통합 사용

```python
# 통합 인터페이스
from src.vessel import Vessel

vessel = Vessel("BUSHRA", lightships, hydro)
vessel.add_weight_items(items)
result = vessel.calculate_stability()
```

## 의존성 관리

### 필수 의존성
- pandas >= 2.0.0
- numpy >= 1.20.0
- xlrd >= 2.0.0
- openpyxl == 3.1.2

### 선택적 의존성
- scipy >= 1.7.0 (고급 stability 계산용)
- matplotlib >= 3.5.0 (리포트 생성용)
- xlsxwriter >= 3.0.0 (Excel 리포트용)
- streamlit >= 1.28.0 (웹 UI용)

### 의존성 그룹

```toml
[project.optional-dependencies]
stability = ["scipy>=1.7.0"]
reporting = ["matplotlib>=3.5.0", "xlsxwriter>=3.0.0"]
web = ["streamlit>=1.28.0"]
all = ["scipy>=1.7.0", "matplotlib>=3.5.0", "xlsxwriter>=3.0.0", "streamlit>=1.28.0"]
```

## 테스트 전략

### 단위 테스트
- 각 모듈 독립 테스트
- 기존 테스트 유지
- 새로운 기능 테스트 추가

### 통합 테스트
- Excel → WeightItem → DisplacementResult
- CSV → WeightItem → StabilityResult
- 전체 워크플로우 테스트

### 검증 테스트
- Excel 워크북과의 일치성
- 기존 결과와의 일치성
- IMO 검증 정확성

