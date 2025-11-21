# agi tr.py Maintenance Patch Report

**Date**: 2025-11-18
**Version**: 3.3 → 3.3.1 (Maintenance)
**Source**: `11111111111.py` 패치 제안

---

## Executive Summary

두 가지 유지보수 패치를 적용하여 코드의 유지보수성을 향상시켰습니다:

1. **Row 범위 자동 연동**: 하드코딩된 row 번호를 `stages` 리스트 길이에 자동 연동
2. **Frame 매핑 디버그 헬퍼**: Frame-to-x 변환 검증을 위한 디버그 함수 추가

---

## Changes Applied

### 1. Row 범위 자동 연동 패치

#### 1.1 `create_roro_sheet()` 함수 수정
- **변경**: 함수가 `stages` 리스트와 `first_data_row`를 반환하도록 수정
- **위치**: Line 909
- **코드**:
  ```python
  return stages, first_data_row
  ```

#### 1.2 `extend_roro_captain_req()` 함수 수정
- **변경**: 함수 시그니처에 `first_data_row`, `num_stages` 파라미터 추가
- **위치**: Lines 1076, 1110
- **변경 전**:
  ```python
  def extend_roro_captain_req(ws):
      ...
      for row in range(15, 27):  # 12 stages (rows 15-26)
  ```
- **변경 후**:
  ```python
  def extend_roro_captain_req(ws, first_data_row, num_stages):
      ...
      for row in range(first_data_row, first_data_row + num_stages):
  ```

#### 1.3 `extend_roro_structural_opt1()` 함수 수정
- **변경**: 함수 시그니처에 `first_data_row`, `num_stages` 파라미터 추가
- **위치**: Lines 1188, 1244
- **변경 전**:
  ```python
  def extend_roro_structural_opt1(ws):
      ...
      for row in range(15, 27):  # 12 stages (rows 15-26)
  ```
- **변경 후**:
  ```python
  def extend_roro_structural_opt1(ws, first_data_row, num_stages):
      ...
      for row in range(first_data_row, first_data_row + num_stages):
  ```

#### 1.4 `create_captain_report_sheet()` 함수 수정
- **변경**: 함수 시그니처에 `stages`, `first_data_row` 파라미터 추가, `roro_rows` 자동 계산
- **위치**: Lines 917, 1007
- **변경 전**:
  ```python
  def create_captain_report_sheet(wb):
      ...
      roro_rows = [15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26]
  ```
- **변경 후**:
  ```python
  def create_captain_report_sheet(wb, stages, first_data_row):
      ...
      roro_rows = [first_data_row + i for i in range(len(stages))]
  ```

#### 1.5 `create_workbook_from_scratch()` 함수 수정
- **변경**: 함수 호출 시 새로운 시그니처 사용
- **위치**: Lines 1588, 1595, 1596, 1599
- **변경 전**:
  ```python
  create_roro_sheet(wb)
  ...
  extend_roro_captain_req(roro_ws)
  extend_roro_structural_opt1(roro_ws)
  create_captain_report_sheet(wb)
  ```
- **변경 후**:
  ```python
  stages, first_data_row = create_roro_sheet(wb)
  ...
  extend_roro_captain_req(roro_ws, first_data_row, len(stages))
  extend_roro_structural_opt1(roro_ws, first_data_row, len(stages))
  create_captain_report_sheet(wb, stages, first_data_row)
  ```

### 2. Frame 매핑 디버그 헬퍼 추가

#### 2.1 `debug_frame_mapping()` 함수 추가
- **위치**: Lines 112-131 (after `x_to_fr()` function)
- **기능**:
  - 현재 `_FRAME_SLOPE`와 `_FRAME_OFFSET` 값 출력
  - 주요 Stage의 Frame 번호와 변환된 x 좌표 출력
- **코드**:
  ```python
  def debug_frame_mapping():
      """
      Frame_x_from_mid_m.json 기반으로 현재 SLOPE/OFFSET과
      주요 기준 Frame들의 x_from_mid_m를 출력하는 디버그 함수.
      """
      print("[Frame Mapping Debug]")
      print(f"  _FRAME_SLOPE  = {_FRAME_SLOPE:.6f}")
      print(f"  _FRAME_OFFSET = {_FRAME_OFFSET:.3f}")

      key_frames = {
          "Stage 5 LCG (FWB1+2)": 52.5,
          "Stage 6A (TR1 final)": 42.0,
          "Stage 6B (TR2 mid ramp)": 38.0,
          "Stage 6C (Combined CG)": 40.0,
          "Stage 7 midship": 30.15,
      }

      for label, fr in key_frames.items():
          x = fr_to_x(fr)
          print(f"  {label:25s}: Fr={fr:6.2f} → x={x:7.3f} m")
  ```

#### 2.2 `if __name__ == "__main__":` 블록 수정
- **위치**: Lines 1624-1629
- **변경 전**:
  ```python
  if __name__ == "__main__":
      create_workbook_from_scratch()
  ```
- **변경 후**:
  ```python
  if __name__ == "__main__":
      import sys
      if len(sys.argv) > 1 and sys.argv[1] == "debug":
          debug_frame_mapping()
      else:
          create_workbook_from_scratch()
  ```

---

## Testing Results

### 1. Debug Mode Test
```bash
python "agi tr.py" debug
```

**Output**:
```
[Frame Mapping Debug]
  _FRAME_SLOPE  = 1.000000
  _FRAME_OFFSET = -30.150
  Stage 5 LCG (FWB1+2)     : Fr= 52.50 → x= 22.350 m
  Stage 6A (TR1 final)     : Fr= 42.00 → x= 11.850 m
  Stage 6B (TR2 mid ramp)  : Fr= 38.00 → x=  7.850 m
  Stage 6C (Combined CG)   : Fr= 40.00 → x=  9.850 m
  Stage 7 midship          : Fr= 30.15 → x=  0.000 m
```

**결과**: 정상 작동 확인

### 2. Normal Mode Test
```bash
python "agi tr.py"
```

**Output**:
```
================================================================================
LCT_BUSHRA_AGI_TR.xlsx Creation from Scratch
================================================================================

[1/8] Creating new workbook

[2/8] Creating sheets:
  [OK] Calc sheet created with VENT&PUMP 실측 0.86
  [OK] December_Tide_2025 sheet created with 744 rows
  [OK] Hourly_FWD_AFT_Heights sheet created
  [OK] RORO_Stage_Scenarios sheet created
  [OK] Ballast_Tanks updated with tank_coordinates.json + tank_data.json (2025-11-18)
  [OK] Hydro_Table sheet created
  [OK] Frame_to_x_Table sheet created with 121 rows
  [OK] Captain Req columns added to RORO_Stage_Scenarios sheet (Patched)
  [OK] Structural Strength & Option 1 Ballast Fix Check columns added to RORO_Stage_Scenarios sheet
  [OK] Hinge Rx 자동 계산 적용
  [OK] CAPTAIN_REPORT sheet created

[7/8] Saving workbook: C:\Users\minky\Downloads\src\LCT_BUSHRA_AGI_TR_Integrated.xlsx
  [OK] File saved successfully

[8/8] Verification:
  [OK] File created: C:\Users\minky\Downloads\src\LCT_BUSHRA_AGI_TR_Integrated.xlsx
  [OK] File size: 111.74 KB
  [OK] Sheets: 8

================================================================================
[SUCCESS] Workbook creation from scratch complete!
================================================================================
```

**결과**: 정상 작동 확인, Excel 파일 생성 성공

### 3. Hardcoded Row Numbers 검증
```bash
grep -n "range(15, 27)" "agi tr.py"
```

**결과**: 하드코딩된 `range(15, 27)` 패턴이 모두 제거되었음을 확인

---

## Benefits

### 1. 유지보수성 향상
- **이전**: Stage 개수 변경 시 여러 곳의 하드코딩된 row 번호를 수동으로 수정해야 함
- **이후**: `stages` 리스트만 수정하면 모든 row 범위가 자동으로 연동됨

### 2. 버그 위험 감소
- **이전**: Stage 추가/제거 시 일부 함수의 row 범위를 놓칠 위험
- **이후**: 모든 함수가 동일한 `stages` 리스트를 기반으로 작동하여 불일치 위험 제거

### 3. 디버깅 편의성 향상
- **이전**: Frame-to-x 변환 검증을 위해 코드를 직접 수정해야 함
- **이후**: `python "agi tr.py" debug` 명령으로 즉시 확인 가능

### 4. 코드 가독성 향상
- **이전**: 매직 넘버(15, 27)의 의미를 코드에서 추론해야 함
- **이후**: `first_data_row`, `num_stages` 같은 명확한 변수명 사용

---

## Backward Compatibility

- **기능 변경 없음**: 기존 기능은 모두 동일하게 작동
- **API 변경**: 내부 함수 시그니처 변경 (외부 사용자에게는 영향 없음)
- **Excel 출력**: 동일한 구조와 내용의 Excel 파일 생성

---

## Future Improvements (Not Implemented)

다음 개선 사항은 이번 패치에 포함되지 않았으며, 향후 버전에서 고려할 수 있습니다:

1. **Hydro_Table 외부화**: 현재 하드코딩된 4개 row를 JSON/CSV 파일에서 읽도록 변경
2. **Vent_Time_h 상수 정식화**: 마법 숫자 45 t/h를 Calc 시트의 `Vent_rate_tph` 셀에서 참조하도록 변경

---

## Files Modified

- `agi tr.py`: 모든 패치 적용 완료

## Files Not Modified

- `docs/EXCEL_GEN_01_OVERVIEW_AND_ARCHITECTURE.md`: 기능 변경 없음
- `docs/EXCEL_GEN_02_FUNCTIONS_AND_IMPLEMENTATION.md`: 기능 변경 없음
- `docs/EXCEL_GEN_03_MATHEMATICS_AND_DATA_FLOW.md`: 기능 변경 없음
- `docs/CHANGELOG.md`: 향후 버전 업데이트 시 반영 예정

---

## Conclusion

모든 패치가 성공적으로 적용되었으며, 테스트를 통과했습니다. 코드의 유지보수성이 향상되었고, 향후 Stage 개수 변경 시에도 안전하게 작동할 것입니다.

---

**Report Generated**: 2025-11-18
**Status**: ✅ Complete

