

## A. 엑셀 설계 – `CAPTAIN_REPORT` 시트 구조

**목적:**

* RORO_Stage_Scenarios 시트에서 **Stage별 Draft/Freeboard가 2.70 m / 0.28 m 조건을 만족하는지**를
  캡틴/Harbour Master에게 바로 보여주는 요약 시트.

### 1) 상단 Limit 입력 영역 (Row 3–7)

| Row | Col | 값 / 수식                                                      | 설명                      |
| --- | --- | ----------------------------------------------------------- | ----------------------- |
| 1   | A1  | `"LCT BUSHRA – Captain Summary (Draft / Trim / Freeboard)"` | 제목, A1:I1 병합 + Title 폰트 |
| 3   | A3  | `"Parameter"`                                               | 헤더                      |
| 3   | B3  | `"Value"`                                                   |                         |
| 3   | C3  | `"Unit"`                                                    |                         |
| 3   | D3  | `"Remark"`                                                  |                         |

**입력값(캡틴 요구 조건 고정):**

| Row | A열 (Parameter)                     | B열 (Value)                   | C     | D(비고)                                       |
| --- | ---------------------------------- | ---------------------------- | ----- | ------------------------------------------- |
| 4   | `"Summer draft limit (max draft)"` | `2.70`                       | `"m"` | `"As per summer draft, any mark ≤ 2.70 m"`  |
| 5   | `"Linkspan freeboard limit"`       | `0.28`                       | `"m"` | `"Minimum freeboard at ramp connector"`     |
| 6   | `"Tmean_baseline (ref)"`           | `=RORO_Stage_Scenarios!$D$5` | `"m"` | `"Baseline mean draft used in RORO stages"` |
| 7   | `"Tide_ref (ref)"`                 | `=RORO_Stage_Scenarios!$G$5` | `"m"` | `"Reference tide for RORO stages"`          |

* B4, B5는 **입력 셀** (노란색 `input_fill`)로 포맷.

### 2) Stage 요약 테이블 (Row 9 이후)

헤더 (예: Row 9):

| Col | 헤더             | 의미                         |
| --- | -------------- | -------------------------- |
| A   | `Stage`        | "Stage 1", "Stage 5A-2" 등  |
| B   | `Dfwd_m`       | Forward draft (RORO O열)    |
| C   | `Daft_m`       | Aft draft (RORO P열)        |
| D   | `Trim_m`       | Trim (RORO F열)             |
| E   | `Max_draft_m`  | `=MAX(Brow,Crow)`          |
| F   | `Draft_OK`     | `E ≤ $B$4 ? OK : ">2.70m"` |
| G   | `FWD_Height_m` | RORO Q열 (Fwd Height)       |
| H   | `Freeboard_OK` | `G ≥ $B$5 ? OK : "<0.28m"` |
| I   | `Notes`        | RORO S열 Stage 설명           |

**Stage별 참조 (기본 생성되는 RORO row 기준):**

* RORO_Stage_Scenarios 시트에서 Stage row는 **15~24행**:

| Stage                   | RORO 행 |
| ----------------------- | ------ |
| Stage 1                 | 15     |
| Stage 2                 | 16     |
| Stage 3                 | 17     |
| Stage 4                 | 18     |
| Stage 5                 | 19     |
| Stage 5A-1 (At-Limit)   | 20     |
| Stage 5A-2 (Optimized)  | 21     |
| Stage 5A-3 (Max-Safety) | 22     |
| Stage 6                 | 23     |
| Stage 7                 | 24     |

예: **CAPTAIN_REPORT Row 10 (Stage 1)**

* A10: `=RORO_Stage_Scenarios!A15`
* B10: `=RORO_Stage_Scenarios!O15`
* C10: `=RORO_Stage_Scenarios!P15`
* D10: `=RORO_Stage_Scenarios!F15`
* E10: `=MAX(B10,C10)`
* F10: `=IF($B$4="","",IF(E10<=$B$4,"OK",">2.70m"))`
* G10: `=RORO_Stage_Scenarios!Q15`
* H10: `=IF($B$5="","",IF(G10>=$B$5,"OK","<0.28m"))`
* I10: `=RORO_Stage_Scenarios!S15`

Row 11~19는 위 수식에서 **행/참조만 16~24로 변경**.

이렇게 하면:

* 캡틴이 말한 **“draft cannot be more than 2.7 m at all stages”** → F열로 한눈에 체크
* **“linkspan freeboard 0.28 m 충분 여부”** → H열로 바로 확인
  (FWD_Height_m vs 0.28 m)

---

## B. 파이썬 패치 – `build_bushra_agi_tr_from_scratch_patched.py`

이제 실제 코드 패치입니다.
**1) CAPTAIN_REPORT 시트 생성 함수 추가**,
**2) `create_workbook_from_scratch()`에서 호출** 두 군데만 손대면 됩니다.

### 1) CAPTAIN_REPORT 시트 생성 함수 추가

파일 안에 다른 시트 생성 함수들(`create_roro_sheet`, `create_hourly_sheet` 등) 아래에 **그대로 추가**하세요.

```python
def create_captain_report_sheet(wb):
    """CAPTAIN_REPORT 시트 생성 - 캡틴/Harbour Master용 요약"""
    ws = wb.create_sheet("CAPTAIN_REPORT")
    styles = get_styles()

    # 1. 제목
    ws["A1"] = "LCT BUSHRA – Captain Summary (Draft / Trim / Freeboard)"
    ws.merge_cells("A1:I1")
    ws["A1"].font = styles["title_font"]
    ws["A1"].alignment = styles["center_align"]

    # 2. LIMIT / REF 영역 헤더 (Row 3)
    header_row = 3
    param_headers = ["Parameter", "Value", "Unit", "Remark"]
    for col_idx, header in enumerate(param_headers, start=1):
        cell = ws.cell(row=header_row, column=col_idx)
        cell.value = header
        cell.font = styles["header_font"]
        cell.fill = styles["header_fill"]
        cell.alignment = styles["center_align"]
        cell.border = Border(
            left=styles["thin_border"],
            right=styles["thin_border"],
            top=styles["thin_border"],
            bottom=styles["thin_border"],
        )

    # 3. LIMIT / REF 값 (Row 4~7)
    # Row 4: Summer draft limit
    ws["A4"] = "Summer draft limit (max draft)"
    ws["B4"] = 2.70  # 캡틴 요구: 모든 stage에서 2.70m 초과 금지
    ws["C4"] = "m"
    ws["D4"] = "As per summer draft, any mark ≤ 2.70 m"
    ws["B4"].fill = styles["input_fill"]

    # Row 5: Linkspan freeboard limit
    ws["A5"] = "Linkspan freeboard limit"
    ws["B5"] = 0.28  # 캡틴 요구: linkspan freeboard 0.28m 이상
    ws["C5"] = "m"
    ws["D5"] = "Minimum freeboard at ramp connector"
    ws["B5"].fill = styles["input_fill"]

    # Row 6: Tmean_baseline ref (from RORO_Stage_Scenarios!D5)
    ws["A6"] = "Tmean_baseline (ref)"
    ws["B6"] = '=RORO_Stage_Scenarios!$D$5'
    ws["C6"] = "m"
    ws["D6"] = "Baseline mean draft used in RORO stages"

    # Row 7: Tide_ref ref (from RORO_Stage_Scenarios!G5)
    ws["A7"] = "Tide_ref (ref)"
    ws["B7"] = '=RORO_Stage_Scenarios!$G$5'
    ws["C7"] = "m"
    ws["D7"] = "Reference tide for RORO stages"

    # LIMIT / REF 영역 기본 폰트 적용
    for row in range(4, 8):
        for col in range(1, 5):
            cell = ws.cell(row=row, column=col)
            if cell.value is not None:
                cell.font = styles["normal_font"]
                if col == 2 and row in (4, 5):
                    # 이미 input_fill 적용됨
                    cell.number_format = "0.00"

    # 4. Stage 요약 테이블 헤더 (Row 9)
    summary_header_row = 9
    summary_headers = [
        "Stage",
        "Dfwd_m",
        "Daft_m",
        "Trim_m",
        "Max_draft_m",
        "Draft_OK",
        "FWD_Height_m",
        "Freeboard_OK",
        "Notes",
    ]
    for col_idx, header in enumerate(summary_headers, start=1):
        cell = ws.cell(row=summary_header_row, column=col_idx)
        cell.value = header
        cell.font = styles["header_font"]
        cell.fill = styles["header_fill"]
        cell.alignment = styles["center_align"]
        cell.border = Border(
            left=styles["thin_border"],
            right=styles["thin_border"],
            top=styles["thin_border"],
            bottom=styles["thin_border"],
        )

    # 5. RORO_Stage_Scenarios의 Stage별 row 매핑
    #   Stage 1  → 15
    #   Stage 2  → 16
    #   Stage 3  → 17
    #   Stage 4  → 18
    #   Stage 5  → 19
    #   Stage 5A-1 → 20
    #   Stage 5A-2 → 21
    #   Stage 5A-3 → 22
    #   Stage 6  → 23
    #   Stage 7  → 24
    roro_rows = [15, 16, 17, 18, 19, 20, 21, 22, 23, 24]
    data_start_row = summary_header_row + 1  # 10행부터

    for idx, roro_row in enumerate(roro_rows):
        row = data_start_row + idx
        row_str = str(row)
        roro_row_str = str(roro_row)

        # A: Stage 이름
        ws.cell(row=row, column=1).value = f'=RORO_Stage_Scenarios!A{roro_row_str}'
        # B: Dfwd_m (O열)
        ws.cell(row=row, column=2).value = f'=RORO_Stage_Scenarios!O{roro_row_str}'
        # C: Daft_m (P열)
        ws.cell(row=row, column=3).value = f'=RORO_Stage_Scenarios!P{roro_row_str}'
        # D: Trim_m (F열)
        ws.cell(row=row, column=4).value = f'=RORO_Stage_Scenarios!F{roro_row_str}'
        # E: Max_draft_m = MAX(B,C)
        ws.cell(row=row, column=5).value = f'=IF(OR(B{row_str}="",C{row_str}=""),"",MAX(B{row_str},C{row_str}))'
        # F: Draft_OK = E ≤ Summer draft limit?
        ws.cell(row=row, column=6).value = (
            f'=IF($B$4="","",IF(E{row_str}<=$B$4,"OK",">2.70m"))'
        )
        # G: FWD_Height_m = RORO Q열
        ws.cell(row=row, column=7).value = f'=RORO_Stage_Scenarios!Q{roro_row_str}'
        # H: Freeboard_OK = G ≥ 0.28?
        ws.cell(row=row, column=8).value = (
            f'=IF($B$5="","",IF(G{row_str}>=$B$5,"OK","<0.28m"))'
        )
        # I: Notes = RORO S열
        ws.cell(row=row, column=9).value = f'=RORO_Stage_Scenarios!S{roro_row_str}'

        # 숫자 포맷/스타일
        for col in range(2, 8):  # B~G
            cell = ws.cell(row=row, column=col)
            cell.font = styles["normal_font"]
            cell.number_format = "0.00"

        # Draft_OK / Freeboard_OK / Notes 스타일
        for col in (1, 6, 8, 9):
            cell = ws.cell(row=row, column=col)
            cell.font = styles["normal_font"]
            cell.alignment = styles["left_align"]

    # 6. 컬럼 너비 조정
    ws.column_dimensions["A"].width = 22
    ws.column_dimensions["B"].width = 10
    ws.column_dimensions["C"].width = 10
    ws.column_dimensions["D"].width = 10
    ws.column_dimensions["E"].width = 12
    ws.column_dimensions["F"].width = 12
    ws.column_dimensions["G"].width = 14
    ws.column_dimensions["H"].width = 14
    ws.column_dimensions["I"].width = 45

    # 7. 보기 좋게 그리드 보더 (요약 테이블 구간만)
    last_row = data_start_row + len(roro_rows) - 1
    for row in range(summary_header_row, last_row + 1):
        for col in range(1, 10):
            cell = ws.cell(row=row, column=col)
            cell.border = Border(
                left=styles["thin_border"],
                right=styles["thin_border"],
                top=styles["thin_border"],
                bottom=styles["thin_border"],
            )

    # 8. Panes 고정 (Stage 헤더 기준)
    ws.freeze_panes = "A10"
```

### 2) `create_workbook_from_scratch()`에 함수 호출 추가

이미 이 부분은 이렇게 돼 있을 겁니다:

```python
    # 새 워크북 생성
    print(f"\n[1/4] Creating new workbook")
    wb = Workbook()
    wb.remove(wb.active)  # 기본 시트 제거
    
    # 각 시트 생성
    print(f"\n[2/4] Creating sheets:")
    create_calc_sheet(wb)
    create_tide_sheet(wb)
    create_hourly_sheet(wb)
    create_roro_sheet(wb)
```

여기에 **한 줄만 추가**:

```python
    # 각 시트 생성
    print(f"\n[2/4] Creating sheets:")
    create_calc_sheet(wb)
    create_tide_sheet(wb)
    create_hourly_sheet(wb)
    create_roro_sheet(wb)
    create_captain_report_sheet(wb)  # ★ 신규 캡틴 요약 시트
```

이렇게 패치하면:

* 기존 `Calc / Tide / Hourly / RORO_Stage_Scenarios` 구조는 그대로 유지.
* 새로 생성되는 `CAPTAIN_REPORT` 시트에서

  * 각 Stage별 **Dfwd/Daft/Trim**
  * **Max draft vs 2.70m**
  * **FWD Height vs 0.28m freeboard**
    를 한 눈에 확인할 수 있어서,

캡틴이 메일에서 요구한:

> “draft cannot be more than 2.7 m at all stages as per summer daft”
> “linkspan freeboard 0.28 m is enough…?”

에 바로 대응 가능한 자료가 자동으로 생성됩니다.

---

원하는 게 **“실제 붙여넣을 수 있는 수준의 코드”**였으니까,
위 B-1, B-2 그대로 적용하시면 됩니다.

적용하시고 나서 생성된 `LCT_BUSHRA_AGI_TR_from_scratch.xlsx` 열어보면,
`CAPTAIN_REPORT` 시트 캡쳐만으로도 ADNOC / Harbour Master / 캡틴 설득 자료로 바로 쓸 수 있을 거예요.
