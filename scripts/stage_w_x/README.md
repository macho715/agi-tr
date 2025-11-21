# Stage W/X Calculator

Stage Weight (W) 및 Position (x) 산출 관련 스크립트 모음

## 파일 목록

### 1. `extract_stage_data_from_pdf.py`
PDF stowage plan에서 Stage W(weight)와 x(position) 값을 추출하는 스크립트

**기능:**
- PDF 파일에서 Stage 3, 4, 5의 W, x 값 추출
- 정규표현식을 사용한 패턴 매칭
- 테이블 및 텍스트에서 데이터 추출

**사용법:**
```bash
python extract_stage_data_from_pdf.py
```

**출력:**
- Stage별 W_stage_t, x_stage_m 값
- Excel 입력 형식으로 출력

### 2. `update_stage_values.py`
Excel 파일의 `RORO_Stage_Scenarios` 시트에 Stage W, x 값을 업데이트하는 스크립트

**기능:**
- Stage 1~5의 W, x 값을 Excel에 자동 입력
- 노란색 셀(입력 셀)에 값 채우기
- 기본값 제공 (사용자 확인 후 업데이트)

**사용법:**
```bash
python update_stage_values.py
```

**기본값:**
- Stage 1: W=0, x=None (Empty condition)
- Stage 2: W=65, x=-10 (SPMT 1st entry on ramp)
- Stage 3: W=110, x=-5 (~50% on ramp)
- Stage 4: W=217, x=-2 (Full on ramp)
- Stage 5: W=434, x=32.5 (Deck full load)

### 3. `extract_ramp_x_from_pdf.py`
PDF 벡터에서 Ramp X 좌표를 추출하는 고급 스크립트 (PyMuPDF 사용)

**기능:**
- PDF 벡터 경로만 사용 (텍스트/OCR 없음)
- Semi-Anchor 모드: 고정 기준점 사용
- Full-Geometry 모드: 자동으로 vessel axis 추론
- Ramp line 자동 감지 및 x 좌표 계산
- Stage별 W, x 값을 CSV로 출력

**사용법:**
```bash
# Semi-Anchor 모드 (기준점 파일 필요)
python extract_ramp_x_from_pdf.py --pdf "../../RoRo Simulation_stowage plan_20251103.pdf" \
    --page 0 --mode semi --anchors anchors.yaml --out stage_x_w.csv

# Full-Geometry 모드 (자동 감지)
python extract_ramp_x_from_pdf.py --pdf "../../RoRo Simulation_stowage plan_20251103.pdf" \
    --page 0 --mode full --out stage_x_w.csv
```

**요구사항:**
- `pymupdf` (fitz) 패키지 필요
- `pyyaml` (semi 모드 사용 시)

### 4. `STAGE_W_X_ALGORITHM.md`
W, x 산출 알고리즘 상세 문서

**내용:**
- 좌표계 정의 (midship = 0)
- W 산출 방법 (반력 비율, SPMT 구성, 트림 변화 역산)
- x 산출 방법 (ramp 위치, deck 위치, 복합 중심 계산)
- 검증 방법 및 예제

## 좌표계

- **Origin**: Midship = 0 m
- **Forward direction**: Negative x (예: -5.0 m)
- **Aft direction**: Positive x (예: +15.27 m)
- **LCF**: +29.29 m (aft direction, verified from Stability Book)

## 워크플로우

1. **PDF에서 데이터 추출**
   ```bash
   python extract_stage_data_from_pdf.py
   ```

2. **Excel에 값 업데이트**
   ```bash
   python update_stage_values.py
   ```

3. **Excel 파일에서 확인**
   - `RORO_Stage_Scenarios` 시트 열기
   - Stage별 W, x 값 확인
   - 계산된 TM, Trim, Dfwd, Daft 값 검증

## 참고

- 모든 좌표는 midship 기준입니다
- LCF와 x_stage는 동일한 좌표 기준을 사용해야 합니다
- 상세 알고리즘은 `STAGE_W_X_ALGORITHM.md` 참조

