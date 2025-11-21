# extract_ramp_x_from_pdf.py 패치 노트 v2.0

## 개요

이 문서는 `extract_ramp_x_from_pdf.py` 스크립트에 적용된 **Full-Geometry 강화 패치**의 상세 내용을 기록합니다.

**패치 일자**: 2025-01-XX  
**패치 버전**: v2.0  
**목적**: 축 추정 및 램프 라인 검출 알고리즘 강화로 인한 스케일/좌표 오류 해결

---

## 배경 및 문제점

### 기존 문제

1. **스케일 추정 오류**: 짧은 폴리라인을 선체 종축으로 오인하여 `meters_per_unit` 비정상 확대
   - 결과: `contact_x = -192.97 m` (비정상적으로 큰 값)
   - 원인: 축 후보 선택 시 길이 검증 부족

2. **램프 라인 오인**: 표 그리드/프레임 라인을 램프로 오인
   - 원인: 각도창 과다 확장(-45°~15°) 및 길이 임계값 과소(1.0 m)

3. **x 좌표 범위 검증 부재**: 산출된 x 값의 sanity 체크 없음

### 해결 목표

- 축 추정 강화: 직선성/수평성 점수 기반 후보 선택
- 스케일 sanity 체크: `m_per_unit ∈ [0.03, 0.20]` 범위 강제
- 램프 후보 사전필터: x 좌표 범위 검증 (`x ∈ [-0.6*Lpp, 0.1*Lpp]`)
- 단계적 각도 확장: 기본 `-15° ~ -2°`에서 실패 시 ±2°씩 확장
- 실패 시 Semi-Anchor 자동 폴백

---

## 주요 변경사항

### 1. `infer_vessel_axis()` 함수 추가 (148-195줄)

**기능**: PDF 벡터 데이터에서 선체 종축을 자동 추론

**알고리즘**:
1. 모든 폴리라인 추출 (`min_seg_len=5.0`)
2. 후보 평가 (상위 20개):
   - **bbox 폭**: `width = |x1 - x0|`
   - **직선성 점수**: `straight_score = Lunits / (Lunits + height)`
   - **수평성 점수**: `horizontal_score = 1.0 / (1.0 + |angle|)`
   - **종합 점수**: `score = width * (0.7*horizontal_score + 0.3*straight_score)`
3. 스케일 sanity 검증:
   - `m_per_unit = LPP_M / units` 계산
   - `0.03 ≤ m_per_unit ≤ 0.20` 범위 내 후보만 선택
4. 폴백: 페이지 폭 기반 축 추정

**반환값**:
```python
(stern, bow), m_per_unit, mid
```

**예시**:
```python
(stern, bow), m_per_unit, mid = infer_vessel_axis(page, LPP_M=64.0)
# m_per_unit ≈ 0.05-0.08 (정상 범위)
```

---

### 2. `select_ramp_line()` 함수 개선 (197-249줄)

**기존 시그니처**:
```python
def select_ramp_line(page, vessel_axis, meters_per_unit,
                     angle_window=(-25.0,-5.0), min_len_m=3.0, ...)
```

**새 시그니처**:
```python
def select_ramp_line(page, vessel_axis, meters_per_unit, LPP_M=64.0,
                     base_angle=(-15.0, -2.0), min_len_ratio=0.08, 
                     max_angle_expansions=3)
```

**주요 개선사항**:

#### a) x 사전필터
```python
x = signed_longitudinal_x(pm, mid, bow, stern, meters_per_unit)
if not (-0.6 * LPP_M <= x <= 0.1 * LPP_M):
    continue  # 램프는 선미 쪽(-)이며 과도한 원거리 제외
```

#### b) 동적 최소 길이
```python
min_len_units = (LPP_M * min_len_ratio) / meters_per_unit
# LPP=64m, ratio=0.08 → min_len ≈ 5.12m
```

#### c) 단계적 각도 확장
```python
for k in range(max_angle_expansions + 1):
    ang_win = (angle_lo - 2*k, angle_hi + 2*k)
    # k=0: (-15, -2)
    # k=1: (-17, 0)
    # k=2: (-19, 2)
    # k=3: (-21, 4)
    poly = pick(ang_win)
    if poly:
        return poly
```

#### d) 후보 정렬
```python
cands.sort(key=lambda t: (-t[1], -t[0]))  # 길이 우선, 다음 aftness
```

---

### 3. Full-Geometry 모드 경로 교체 (315-336줄)

**기존 로직**:
- 단순히 가장 긴 폴리라인을 축으로 선택
- 스케일 검증 없음

**새 로직**:
```python
try:
    (stern, bow), m_per_unit, mid = infer_vessel_axis(page, LPP_M=64.0)
    print(f"[INFO] Vessel axis inferred: m_per_unit={m_per_unit:.4f}")
    ramp_poly = select_ramp_line(page, (stern, bow), m_per_unit, LPP_M=64.0,
                                base_angle=tuple(args.angle) if len(args.angle) == 2 else (-15.0, -2.0))
    ramp_mid = poly_midpoint(ramp_poly)
    x_contact_m = signed_longitudinal_x(ramp_mid, mid, bow, stern, m_per_unit)
except Exception as e:
    print(f"[WARN] Full-Geometry failed: {e}. Falling back to Semi-Anchor heuristic.")
    # 폴백: 페이지 가로중선 축 + 합리 스케일
    rect = page.rect
    stern = (rect.x0, rect.y0 + rect.height / 2)
    bow = (rect.x1, rect.y0 + rect.height / 2)
    units = dist(stern, bow)
    m_per_unit = 64.0 / units if units else 0.1
    mid = ((stern[0] + bow[0]) / 2, (stern[1] + bow[1]) / 2)
    ramp_poly = select_ramp_line(page, (stern, bow), m_per_unit, LPP_M=64.0, ...)
    ...
```

---

### 4. 산출 검증 추가 (338-340줄)

```python
# 산출 검증: x sanity
if abs(x_contact_m) > 0.6 * 64.0:
    raise ValueError(f"x_contact out of range ({x_contact_m:.2f} m). Check axis/scale.")
```

**검증 범위**: `|x_contact| ≤ 38.4 m` (0.6 * LPP)

---

### 5. 인자 기본값 조정 (297-298줄)

| 인자 | 기존 기본값 | 새 기본값 | 설명 |
|------|------------|----------|------|
| `--angle` | `[-25.0, -5.0]` | `[-15.0, -2.0]` | 램프 경사 보수 범위 |
| `--min-len-m` | `3.0` | `5.0` | 0.08*Lpp (≈5.12m) |

---

## 실행 방법

### 기본 실행 (Full-Geometry 모드)

```bash
cd scripts/stage_w_x
python extract_ramp_x_from_pdf.py \
    --pdf "../../RoRo Simulation_stowage plan_20251103 (2).pdf" \
    --page 0 \
    --mode full \
    --out stage_x_w.csv
```

### 각도 범위 조정

```bash
python extract_ramp_x_from_pdf.py \
    --pdf "../../RoRo Simulation_stowage plan_20251103 (2).pdf" \
    --page 0 \
    --mode full \
    --angle -20.0 5.0 \
    --out stage_x_w.csv
```

### Semi-Anchor 모드 (기준점 파일 사용)

```bash
python extract_ramp_x_from_pdf.py \
    --pdf "../../RoRo Simulation_stowage plan_20251103 (2).pdf" \
    --page 0 \
    --mode semi \
    --anchors anchors.yaml \
    --out stage_x_w.csv
```

**anchors.yaml 예시**:
```yaml
stern: [100.0, 400.0]
bow: [700.0, 400.0]
mid: [400.0, 400.0]  # optional
lpp_m: 64.0
```

---

## 검증 체크리스트

실행 후 다음 항목을 확인하세요:

- [ ] `m_per_unit`가 0.03-0.20 범위 내인지 확인
  ```bash
  # 로그에서 확인: [INFO] Vessel axis inferred: m_per_unit=0.XXXX
  ```

- [ ] 산출된 `x_stage_m`가 `[-38.40, +6.40]` 범위 내인지 확인
  ```bash
  # CSV 파일에서 확인: x_stage_m 컬럼 값
  ```

- [ ] 램프 라인 검출 성공 여부 확인
  ```bash
  # [WARN] 메시지 없이 [OK] 메시지 출력 확인
  ```

- [ ] CSV 파일 생성 확인
  ```bash
  # stage_x_w.csv 파일 존재 및 내용 확인
  ```

---

## 문제 해결 가이드

### 문제 1: "Ramp line not found after expansions"

**원인**: 각도 범위가 너무 좁거나 최소 길이 임계값이 너무 큼

**해결책**:
1. 각도 범위 확장:
   ```bash
   --angle -25.0 10.0
   ```
2. 최소 길이 감소 (주의: 너무 작으면 노이즈 유입):
   ```bash
   --min-len-m 3.0
   ```
3. Semi-Anchor 모드 사용 (더 정확)

---

### 문제 2: "x_contact out of range"

**원인**: 축 추정 또는 스케일 계산 오류

**해결책**:
1. `m_per_unit` 값 확인 (로그 출력)
   - 비정상 범위(>0.20 또는 <0.03)면 축 추정 실패
2. Semi-Anchor 모드로 전환하여 수동 기준점 제공
3. PDF 페이지 확인 (올바른 페이지 번호 사용)

---

### 문제 3: "Full-Geometry failed"

**원인**: 벡터 데이터 부족 또는 품질 문제

**해결책**:
1. 자동 폴백 확인 (Semi-Anchor 휴리스틱 사용)
2. PDF 품질 확인 (벡터 데이터 포함 여부)
3. Semi-Anchor 모드로 전환

---

## 기술적 세부사항

### 좌표계 및 단위

- **PDF/MuPDF 좌표**: 포인트 단위 (1 pt = 1/72 인치)
- **MuPDF 원점**: top-left (PDF는 bottom-left)
- **변환**: `Page.transformation_matrix`로 처리
- **스케일**: `m_per_unit = LPP_M / axis_length(pts)`

### 스케일 Sanity 범위 근거

- **A4/A3 도면**: 일반적으로 `m_per_unit ≈ 0.05-0.08`
- **범위 [0.03, 0.20]**: 
  - 하한: 작은 도면 (A4, 축 길이 짧음)
  - 상한: 큰 도면 (A0, 축 길이 김)

### x 좌표 범위 근거

- **램프 위치**: 선미 쪽 (음수 x)
- **범위 [-0.6*Lpp, 0.1*Lpp]**:
  - 하한: 선미 끝에서 0.6*Lpp 이내
  - 상한: 중앙선에서 0.1*Lpp 이내 (보수)

---

## 참고 자료

- [PyMuPDF Documentation - Appendix 3](https://pymupdf.readthedocs.io/en/latest/app3.html)
- [PyMuPDF Documentation - Page](https://pymupdf.readthedocs.io/en/latest/page.html)
- [PyMuPDF Documentation - Rect](https://pymupdf.readthedocs.io/en/latest/rect.html)

---

## 변경 이력

| 버전 | 일자 | 변경 내용 |
|------|------|----------|
| v2.0 | 2025-01-XX | Full-Geometry 강화 패치 적용 |
| v1.0 | - | 초기 버전 |

---

## 작성자

MACHO-GPT v3.4-mini (HVDC Project - Samsung C&T Logistics)

