# CHANGELOG - agi tr.py

**Script:** `agi tr.py`
**Output:** `LCT_BUSHRA_AGI_TR_Integrated_v2.xlsx`
**Last Updated:** 2025-11-19 (Version 3.9)

---

## Version 3.9.1 (2025-11-19) - Project File Organization

### Changed (Project Structure - Root Directory Cleanup)

#### Root Directory Cleanup
- **Verification Scripts**: Moved to `archive/verification/`
  - `comprehensive_formula_verification.py` → `archive/verification/`
  - `verify_excel_formulas.py` → `archive/verification/`
  - Reason: `verify_excel_generation.py` is the integrated verification script
- **Conversion Scripts**: Moved to `scripts/tools/`
  - `convert_tank_*.py` (5 files) → `scripts/tools/`
  - Updated `scripts/tools/README.md` with new scripts
  - Reason: Tank data conversion tools belong in tools directory
- **ZIP Files**: Moved to `archive/`
  - `bushra_excel_bridge_v1.zip` → `archive/`
  - `LCT_BUSHRA_Package_TANK_LEVER_ARM.zip` → `archive/`
  - Reason: Source code already exists, ZIP files are archives
- **Excel Files**: Moved to `archive/excel_backups/`
  - `LCT_BUSHRA_GateAB_v4_HYBRID.xlsx` → `archive/excel_backups/`
  - Reason: Final version exists in `output/` directory
- **Plan File**: Moved to `archive/docs/`
  - `.plan.md` → `archive/docs/.plan.md`
  - Reason: Plan file is historical documentation

#### Result
- **Root Directory**: Reduced from 17 files to 6 essential files
  - `agi tr.py` (main script)
  - `README.md` (project README)
  - `requirements.txt` (Python dependencies)
  - `verify_excel_generation.py` (integrated verification script)
  - `analyze_excel_structure.py` (analysis tool)
  - `bushra_excel_bridge_v1.py` (bridge system)

### Changed (Project Structure)

#### File Organization
- **Patch Guides**: Moved to `docs/patches/`
  - `sdsdds.md`, `zzzzz.md`, `aaaa.md`, `patcaah.md`, `wewewewe.md`
  - See [`docs/patches/README.md`](patches/README.md) for index
- **Captain Documents**: Moved to `docs/captain/`
  - `CAPTAIN_QUICK_REFERENCE.md` → `QUICK_REFERENCE.md`
  - `CAPTAIN_PATCH_EXECUTION_GUIDE.md` → `PATCH_EXECUTION_GUIDE.md`
  - `captain.md` → `GUIDE.md`
  - `README_CAPTAIN_PATCH.txt` → `README.txt`
  - See [`docs/captain/README.md`](captain/README.md) for index
- **Verification Reports**: Moved to `docs/verification/`
  - All verification reports consolidated
  - See [`docs/verification/README.md`](verification/README.md) for index
- **Archive Structure**: Organized archive directories
  - `archive/backups/` - Backup files
  - `archive/temp/` - Temporary files
  - `archive/data/unused/` - Unused data files
  - `archive/configs/` - Configuration backups
  - See [`archive/README.md`](../../archive/README.md) for structure

#### Excel Files
- **Root Directory**: Only latest version maintained
  - `LCT_BUSHRA_AGI_TR_Integrated_v2.xlsx` (latest)
- **Archived**: All timestamped and older versions moved to `archive/excel_backups/`

#### Data Files
- **Root JSON**: Moved to `data/` directory
  - `LCT BUSHRA GM 2D Grid.json` → `data/LCT_BUSHRA_GM_2D_Grid.json`
- **Unused Files**: Moved to `archive/data/unused/`

### Technical Details
- **Backward Compatibility**: All file references in code remain functional
- **Documentation**: Index files created for all new directories
- **Code References**: Patch guide references in `agi tr.py` comments remain valid (documentation only)

---

---

## Table of Contents

1. [Version 3.9 (2025-11-19)](#version-39-2025-11-19)
2. [Version 3.8 (2025-11-19)](#version-38-2025-11-19)
3. [Version 3.7 (2025-11-19)](#version-37-2025-11-19)
4. [Version 3.6 (2025-11-18)](#version-36-2025-11-18)
5. [Version 3.3.1 (2025-11-18)](#version-331-2025-11-18)
6. [Version 3.3 (2025-11-18)](#version-33-2025-11-18)
7. [Version 3.2 (2025-11-18)](#version-32-2025-11-18)
8. [Version 3.1 (2025-11-18)](#version-31-2025-11-18)
9. [Version 3.0+ (2025-11-18)](#version-30-2025-11-18)
10. [Version 3.0 (2025-01-18)](#version-30-2025-01-18)
11. [Version 2.x (Initial Integrated)](#version-2x-initial-integrated)

---

## Version 3.9 (2025-11-19)

### Changed (sdsdds.md 가이드 - Stage별 Trim_target 컬럼 추가)

#### Q열 (17) - Trim_target_stage_cm 컬럼 추가

- **위치**: Daft_m(P열) 다음, FWD_Height_m(R열) 이전
- **헤더**: `"Trim_target_stage_cm"`
- **데이터**:
  - **Stage 1, 5, 7**: `0.0` (Baseline은 Trim=0이 타깃)
  - **나머지 Stage (2, 3, 4, 5A-1, 5A-2, 5A-3, 6A, 6B, 6C)**: 빈 값 `""` (전역 타깃 B6 사용)
- **Purpose**: Stage별로 다른 Trim 타깃을 설정할 수 있도록 확장
- **Implementation**: Lines 969, 1131-1138 in `create_roro_sheet()`

#### H열 (8) - ΔTM_cm_tm 수식 업데이트 (Stage별 타깃 지원)

- **Previous**: `=IF($A{row}="","",(E{row} - $B$6) * $B$8)` (전역 타깃만 사용)
- **Current**: `=IF($A{row}="","",(E{row} - IF($Q{row}="",$B$6,$Q{row})) * $B$8)`
- **의미**:
  - Q열이 비어있으면 → 전역 타깃 `$B$6`(-96.5 cm) 사용
  - Q열에 값이 있으면 → 그 Stage만의 타깃(예: 0 cm) 사용
- **특징**:
  - Stage 1/5/7: Q=0 → H=0, J/AM/AN/AO/AP=0 → "Baseline은 Fix 대상 아님"
  - 5A/6 시리즈: Q=빈 값 → B6(-96.5) 사용 → "실제 Trim vs 목표 Trim(-96.5) 차이" 계산
- **Implementation**: Lines 1091-1097 in `create_roro_sheet()`

#### 컬럼 구조 변경 (Q열 추가로 인한 한 칸씩 밀림)

- **FWD_Height_m**: Q(17) → R(18)
- **AFT_Height_m**: R(18) → S(19)
- **Notes**: S(19) → T(20)
- **Captain Req 컬럼**: T(20) → U(21) ~ AE(31)
  - GM: T(20) → U(21)
  - Fwd Draft: U(21) → V(22)
  - vs 2.70m: V(22) → W(23)
  - De-ballast Qty: W(23) → X(24)
  - Timing: X(24) → Y(25)
  - Phys_Freeboard_m: Y(25) → Z(26)
  - Clearance_Check: Z(26) → AA(27)
  - GM_calc: AA(27) → AB(28)
  - GM_Check: AB(28) → AC(29)
  - Prop Imm: AC(29) → AD(30)
  - Vent_Time_h: AD(30) → AE(31)
- **Structural/Option 1 컬럼**: AE(31) → AF(32) ~ AW(49)
  - Structural Strength: AE(31) → AF(32) ~ AK(37)
  - Dynamic Load Case: AK(37) → AL(38) ~ AM(39)
  - Option 1 Ballast Fix: AM(39) → AN(40) ~ AQ(43)
  - Heel/FSE: AQ(43) → AR(44) ~ AS(45)
  - Ramp/Stress: AS(45) → AT(46) ~ AW(49)
- **Implementation**:
  - `extend_roro_captain_req()`: start_col 20 → 21 (Lines 1457, 1476-1536)
  - `extend_roro_structural_opt1()`: start_col 31 → 32 (Lines 1604, 1639-1776)
  - `create_captain_report_sheet()`: 컬럼 참조 업데이트 (Lines 1377, 1379, 1382, 1386, 1391)

#### Excel Table 범위 업데이트

- **Previous**: `A14:AV26` (48 columns)
- **Current**: `A14:AW26` (49 columns)
- **마지막 컬럼**: AV(48) → AW(49)
- **Implementation**: Line 2111 in `create_workbook_from_scratch()`

### Technical Details

- **Source**: Integrated from `sdsdds.md` patch guide
- **Backward Compatibility**: Excel 출력 구조 변경 (Q열 추가, 컬럼 수 48→49)
- **Testing**:
  - Python 문법 검증 완료
  - Excel 파일 생성 검증 완료
  - Q열 데이터 입력 검증 완료 (Stage 1/5/7 = 0, 나머지 = 빈 값)
  - H열 수식 검증 완료 (Q열 참조 포함)
  - 컬럼 구조 검증 완료 (모든 컬럼 한 칸씩 밀림 확인)

### Benefits

- **유연성**: Stage별로 다른 Trim 타깃 설정 가능 (Baseline vs Fix 대상 Stage 분리)
- **명확성**: Stage 1/5/7은 Trim=0이 타깃임을 명시적으로 표현
- **일관성**: 나머지 Stage는 전역 타깃(B6)을 사용하여 일관된 계산
- **운영 효율**: Baseline Stage는 Fix 계산에서 자동으로 제외되어 불필요한 계산 방지

---

## Version 3.8 (2025-11-19)

### Changed (zzzzz.md 가이드 - Trim_target 기반 Ballast Fix 수식 패치)

#### RORO_Stage_Scenarios 시트 상단 파라미터 추가

- **A6, B6 - Trim_target_cm**: 목표 Trim 값 입력
  - **A6**: 헤더 `"Trim_target_cm"`
  - **B6**: 값 `-96.5` (목표 Trim_cm)
  - Purpose: 모든 Stage의 Trim을 목표값으로 맞추기 위한 기준값
  - Implementation: Lines 520-521 in `create_roro_sheet()`

- **B8 - MTC (t·m/cm)**: Calc 시트 직접 참조로 변경
  - **Previous**: 고정값 또는 수동 입력
  - **Current**: `=INDEX(Calc!$E:$E, MATCH("MTC_t_m_per_cm", Calc!$C:$C, 0))`
  - Purpose: Calc 시트의 MTC 값을 자동으로 참조
  - Implementation: Line 523 in `create_roro_sheet()`

- **B11 - pump_rate_effective_tph**: Calc 시트 직접 참조로 변경
  - **Previous**: 고정값 또는 수동 입력
  - **Current**: `=Calc!$E$31`
  - Purpose: Calc 시트의 pump_rate_effective_tph 값을 자동으로 참조
  - Implementation: Line 526 in `create_roro_sheet()`

#### H 컬럼 (8) - ΔTM_cm_tm 수식 업데이트

- **Previous**: `=IF($A{row}="", "", 0)` (무효화 상태)
- **Current**: `=IF($A{row}="","",(E{row} - $B$6) * $B$8)`
- **의미**: (현재 Trim_cm - 목표 Trim_target_cm) × MTC = 필요한 Trim 모멘트
- **특징**:
  - E = B6인 Stage (Trim이 목표값인 Stage)는 H=0
  - 양수: 선수침 증가 필요 (Ballast 추가)
  - 음수: 선수침 감소 필요 (De-ballast)
- Implementation: Line 1057 in `create_roro_sheet()`

#### J 컬럼 (10) - Ballast_t_calc 수식 업데이트

- **Previous**: `=IF(OR($A{row}="",$I{row}="", $I{row}=0),"",ROUND(H{row} / $I{row}, 2))`
- **Current**: 동일 (H 컬럼이 활성화되어 정상 작동)
- **의미**: ΔTM(H) / Lever_arm(I) = 이론적으로 필요한 Ballast 톤수
- Implementation: Line 1062 in `create_roro_sheet()`

#### K 컬럼 (11) - Ballast_time_h_calc 수식 업데이트

- **Previous**: `=IF(OR(J{row}="", $C$11="", $C$11=0, ISERROR($C$11)), "", ROUND(J{row} / $C$11, 2))`
- **Current**: `=IF(OR(J{row}="", $B$11="", $B$11=0, ISERROR($B$11)), "", ROUND(J{row} / $B$11, 2))`
- **변경사항**: `$C$11` → `$B$11` (pump_rate_effective_tph 참조 변경)
- **의미**: Ballast_t_calc(J) / pump_rate_effective_tph(B11) = 필요한 시간
- Implementation: Line 1067 in `create_roro_sheet()`

#### AM 컬럼 (39) - ΔTM_needed_cm·tm 수식 업데이트

- **Previous**: `=IF($A{row}="", "", 0)` (무효화 상태)
- **Current**: `=IF($A{row}="","",ABS(H{row}))`
- **의미**: H 컬럼의 절대값 (Trim 모멘트 크기만)
- **용도**: Option 1 Ballast Fix 블록에서 필요한 Trim 모멘트 크기 확인
- Implementation: Line 1652 in `extend_roro_structural_opt1()`

#### AN 컬럼 (40) - Ballast_req_t 수식 업데이트

- **Previous**: `=IF($A{row}="","",IF(OR($I{row}="",$I{row}=0),0,ROUND(H{row}/$I{row},2)))`
- **Current**: 동일 (H 컬럼이 활성화되어 정상 작동)
- **의미**: H / I = 필요한 Ballast 톤수 (J 컬럼과 동일 개념)
- **용도**: Option 1 Ballast Fix 블록에서 필요한 Ballast 톤수 계산
- Implementation: Line 1657 in `extend_roro_structural_opt1()`

#### AO 컬럼 (41) - Ballast_gap_t 수식 업데이트

- **Previous**: `=IF($A{row}="","",AN{row} - $L{row})`
- **Current**: 동일 (AN 컬럼이 활성화되어 정상 작동)
- **의미**: 필요한 Ballast(AN) - 실제 Ballast(L) = Gap 톤수
- **특징**:
  - 양수: 추가 Ballast 필요
  - 음수: De-ballast 필요
- Implementation: Line 1662 in `extend_roro_structural_opt1()`

#### AP 컬럼 (42) - Time_Add_h 수식 업데이트

- **Previous**: `=IF($A{row}="","",IF($C$11=0,0,AO{row}/$C$11))`
- **Current**: `=IF($A{row}="","",IF($B$11=0,0,AO{row}/$B$11))`
- **변경사항**: `$C$11` → `$B$11` (pump_rate_effective_tph 참조 변경)
- **의미**: Gap 톤수(AO) / pump_rate_effective_tph(B11) = 추가/감소 시간
- **특징**:
  - 양수: 추가 Ballast 시간
  - 음수: De-ballast 시간 (절대값 사용 권장)
- Implementation: Line 1667 in `extend_roro_structural_opt1()`

### Technical Details

- **Source**: Integrated from `zzzzz.md` patch guide
- **Backward Compatibility**: Excel 출력 구조 변경 없음 (수식만 업데이트)
- **Testing**:
  - Python 문법 검증 완료
  - Excel 파일 생성 검증 완료
  - 수식 구조 검증 완료 (zzzzz_patch_verification_report.md)
- **Sanity Check**:
  - Trim = Target Stage 체크: E열에 -96.5 입력 시 H≈0 확인 가능
  - Stage 5A-2 감도 체크: 부호·크기 직관성 확인 가능
  - Pump rate 변경 테스트: B11 변경 시 K/AP가 비례 변경 확인 가능

### Benefits

- **일관성**: 모든 Trim 관련 계산이 Trim_target_cm(B6) 기준으로 통일
- **자동화**: MTC(B8), pump_rate(B11)가 Calc 시트에서 자동 참조
- **명확성**: H/J/AM~AP 블록이 Trim_target 기준으로 명확하게 계산
- **운영 효율**: Option 1 Ballast Fix 블록이 실제 필요한 Ballast와 시간을 정확히 계산

---

## Version 3.7 (2025-11-19)

### Changed (LCF 기반 정밀 Draft 보정 모듈 패치)

#### Python 함수 수정 (`aaaa.md` 가이드 준수)

- **`calc_gm_effective()`**: Error handling 변경
  - **Previous**: `if disp_t <= 0: raise ValueError("disp_t must be > 0")`
  - **Current**: `if disp_t <= 0: return gm_m`
  - Reason: 가이드에 맞춰 예외 대신 기본값 반환
  - Implementation: Lines 211-218

- **`apply_dynamic_loads()`**: 파라미터 및 반환값 수정
  - **brake_factor 기본값**: 1.30 → 1.00
  - **horiz_factor 파라미터**: 제거됨
  - **반환값**: `horiz_load_t` 제거, `share_load_t`, `pin_stress_mpa`만 반환
  - Reason: `aaaa.md` 가이드에 맞춰 간소화
  - Implementation: Lines 258-280

- **Docstring 간소화**
  - `calc_heel_from_offset()`: 상세한 Parameters/Returns 섹션 제거, 핵심 설명만 유지
  - `calc_draft_with_lcf()`: 상세한 Parameters/Returns/공식 섹션 제거, 핵심 설명만 유지
  - Reason: 가이드 형식에 맞춰 간소화
  - Implementation: Lines 109-124, 196-208

#### Excel 수식 수정

- **H 컬럼 (8) - ΔTM_cm_tm**: 빈 값 → 0으로 변경
  - **Previous**: 빈 문자열 `""`
  - **Current**: `=IF($A{row}="", "", 0)`
  - Reason: J 컬럼이 H를 참조하므로 빈 값으로 인한 수식 오류 방지
  - Implementation: Lines 1057-1059

- **AM 컬럼 (39) - ΔTM_needed_cm·tm**: 수식 무효화
  - **Previous**: `Calc!$E$14 * (ABS(E{row}) - ABS(G{row}))`
  - **Current**: `=IF($A{row}="", "", 0)`
  - Reason: G 컬럼이 AFT_precise_m로 변경되어 Trim_target_cm 기반 계산 불가
  - Note: 향후 Trim_target 입력 컬럼 추가 시 수정 가능
  - Implementation: Lines 1652-1654

- **AS 컬럼 (45) - Reserved**: 완전 제거
  - **Previous**: Reserved 컬럼으로 "Reserved" 헤더 및 빈 데이터 행 처리
  - **Current**: AS 컬럼 완전 제거, Ramp/Stress 컬럼 재조정
  - **변경사항**:
    - AS 컬럼(45) Reserved 제거
    - Ramp/Stress 컬럼 재조정: AS(45), AT(46), AU(47), AV(48)
    - Excel 테이블 범위: A14:AS26 → A14:AV26
    - RORO 컬럼 수: 49 → 48
  - Reason: 불필요한 Reserved 컬럼 제거로 컬럼 구조 정리
  - Implementation: Lines 1533-1547 (헤더), 1694-1719 (데이터 행)

#### Calc 시트 PRECISION PARAMETERS 섹션 업데이트

- **Row 40 (E40) - LBP_m**: 값 및 Comment 추가
  - **Previous**: `60.30` (Comment 없음)
  - **Current**: `60.302` + Comment `"LBP (m) - Calc!$E$40"`
  - Reason: 정밀도 향상 및 참조 명확화
  - Implementation: Lines 648-649

- **Row 41 (E41) - LCF_from_mid_m**: 값 및 Comment 추가
  - **Previous**: `15.71` (Comment 없음)
  - **Current**: `30.910` + Comment `"LCF from mid (m) - Calc!$E$41"`
  - Reason: Fr30.15 기준 정확한 LCF 값 반영 및 참조 명확화
  - Implementation: Lines 657-660

- **Import 추가**: `from openpyxl.comments import Comment` 추가
  - Reason: Excel Comment 기능 사용을 위한 import
  - Implementation: Line 10

### Technical Details

- **Source**: Integrated from `aaaa.md` patch guide
- **Backward Compatibility**: Excel 출력 구조 변경 (AS 컬럼 제거, 컬럼 수 49→48)
- **Testing**: Python 문법 검증 완료, Excel 파일 생성 검증 완료

---

## Version 3.6 (2025-11-18)

### Enhanced (Data Externalization & Maintenance)

#### Hydro_Table JSON Externalization
- **`create_hydro_table_sheet()`**: Enhanced to load data from JSON file
  - Loads from `data/hydro_table.json` using `_load_json()` function
  - Supports 12 hydrostatic data points (up from 4 hardcoded points)
  - Supports both dict list format and array format
  - Falls back to 4 hardcoded points if JSON not found or invalid
  - Prints success message: `"  [OK] Hydro_Table loaded from JSON ({len(data)} points)"`
  - Prints fallback message: `"  [FALLBACK] Using built-in 4 points"`
  - Implementation: Lines 1461-1494

#### Vent_rate Fixed Value
- **`create_calc_sheet()`**: Changed `pump_rate_effective_tph` (E31) from formula to fixed value
  - **Previous**: Formula calculating effective pump rate based on air vent bottlenecks
  - **Current**: Fixed value `45.00 t/h`
  - Note: "FWD tank air vent 제한 (80 mm) → 실효 45 t/h"
  - Cell fill changed to `input_fill` (yellow background)
  - Implementation: Line 387

#### Debug CLI Improvements
- **`debug_frame_mapping()`**: Enhanced output formatting
  - Improved separator lines (60-char width for better readability)
  - Added `sys.exit(0)` to terminate script after debug output
  - Prevents accidental Excel file generation when running in debug mode
  - Implementation: Lines 128-142

#### Frame Mapping Initialization Enhancement
- **`_init_frame_mapping()`**: Improved initialization and messaging
  - Now called in `if __name__ == "__main__":` block instead of module level
  - Added INFO messages for default and calculated slope/offset values
  - Better error handling with informative messages
  - Implementation: Lines 78-110, 1668

#### `_load_json()` Warning Message
- **`_load_json()`**: Added warning message when file not found
  - Prints `[WARNING] {filename} not found → using fallback` when file not found
  - Helps users identify missing JSON files during execution
  - Implementation: Line 69

### Benefits
- **Data Management**: Hydro_Table data can now be easily updated via JSON file without code changes
- **Maintainability**: Externalized data reduces hardcoded values in code
- **User Experience**: Clear warning messages help identify missing data files
- **Debugging**: Improved debug output makes Frame mapping verification easier
- **Flexibility**: Supports 12 data points for more accurate GM lookup interpolation

### Technical Details
- **Source**: Integrated from `ssssss.py` patch proposal
- **Backward Compatibility**: All changes maintain backward compatibility with fallback mechanisms
- **Data Format**: JSON supports both `[{"Disp_t": ..., ...}, ...]` and `[[...], ...]` formats
- **Testing**: All tests passed, Excel file generation verified with both JSON and fallback scenarios

---

## Version 3.3.1 (2025-11-18)

### Enhanced (Maintenance Patch)

#### Row Range Auto-Binding
- **`create_roro_sheet()`**: Now returns `(stages, first_data_row)` tuple
  - Enables automatic row range calculation in dependent functions
  - Implementation: Line 909

- **`extend_roro_captain_req()`**: Updated function signature
  - **Previous**: `extend_roro_captain_req(ws)`
  - **Current**: `extend_roro_captain_req(ws, first_data_row, num_stages)`
  - Row range changed from hardcoded `range(15, 27)` to `range(first_data_row, first_data_row + num_stages)`
  - Implementation: Lines 1076, 1110

- **`extend_roro_structural_opt1()`**: Updated function signature
  - **Previous**: `extend_roro_structural_opt1(ws)`
  - **Current**: `extend_roro_structural_opt1(ws, first_data_row, num_stages)`
  - Row range changed from hardcoded `range(15, 27)` to `range(first_data_row, first_data_row + num_stages)`
  - Implementation: Lines 1188, 1244

- **`create_captain_report_sheet()`**: Updated function signature
  - **Previous**: `create_captain_report_sheet(wb)`
  - **Current**: `create_captain_report_sheet(wb, stages, first_data_row)`
  - `roro_rows` changed from hardcoded `[15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26]` to `[first_data_row + i for i in range(len(stages))]`
  - Implementation: Lines 917, 1007

- **`create_workbook_from_scratch()`**: Updated function calls
  - Captures return value from `create_roro_sheet()`: `stages, first_data_row = create_roro_sheet(wb)`
  - Passes parameters to extension functions
  - Implementation: Lines 1588, 1595, 1596, 1599

#### Debug Helper Function
- **`debug_frame_mapping()`**: New debug function added
  - Prints current `_FRAME_SLOPE` and `_FRAME_OFFSET` values
  - Prints key Stage Frame numbers and converted x-coordinates
  - Implementation: Lines 112-131

- **Command-line debug mode**: Added debug mode support
  - **Usage**: `python "agi tr.py" debug`
  - Prints Frame mapping debug information without generating Excel file
  - Implementation: Lines 1624-1629

### Benefits
- **Maintainability**: Stage count changes automatically propagate to all row ranges
- **Bug Prevention**: No risk of forgetting to update hardcoded row numbers when stages are added/removed
- **Debugging**: Easy verification of Frame-to-x conversion parameters
- **Code Quality**: Eliminated magic numbers (15, 27) in favor of calculated values

### Technical Details
- **Source**: Integrated from `11111111111.py` patch proposal
- **Backward Compatibility**: Excel output structure unchanged, only internal implementation improved
- **Testing**: All tests passed, Excel file generation verified

---

## Version 3.3 (2025-11-18)

### Changed

#### Stage 5/7 Trim Target Updates
- **Stage 5**: Trim target changed from -163.68 cm to **-89.58 cm**
  - Reason: New design criteria, lever arm ratio (8.56/15.64) applied based on new x_CG (22.35 m)
  - Previous value was based on old x_CG position
  - New value reflects updated FWB1+FWB2 LCG position
  - Implementation: Line 700 in `create_roro_sheet()`

- **Stage 7**: Trim target changed from -96.5 cm to **0.0 cm** (Even keel)
  - Reason: Cargo off + symmetric midship ballast should target even keel condition
  - Ensures vessel returns to neutral trim after cargo removal
  - Implementation: Line 707 in `create_roro_sheet()`

### Technical Details

- **Source**: Integrated from `ppppp12.py` guide
- **Impact**: All trim moment calculations (ΔTM) that reference Stage 5 trim or Stage 7 trim target are affected
- **Backward Compatibility**: Old trim target values are no longer used; calculations automatically use new values

---

## Version 3.2 (2025-11-18)

### Enhanced

#### Frame Conversion Utilities
- **`_load_json(filename)`**: Enhanced with multiple path support
  - Tries script directory first
  - Falls back to current working directory
  - Finally tries `/mnt/data` (Notebook environment)
  - Returns `None` if file not found in any location
  - Implementation: Lines 52-69

- **`_init_frame_mapping()`**: Automatic slope/offset estimation from JSON
  - Loads `data/Frame_x_from_mid_m.json` automatically
  - Calculates `_FRAME_SLOPE` and `_FRAME_OFFSET` from first two entries
  - Falls back to default values (slope=1.0, offset=-30.15) if JSON not found
  - Called at module level during script initialization
  - Implementation: Lines 77-99

- **`fr_to_x(fr)`**: Enhanced to use slope parameter
  - Formula: `x = _FRAME_OFFSET + _FRAME_SLOPE * Fr`
  - Supports non-linear Frame-to-x mappings if slope is adjusted
  - Implementation: Lines 102-104

- **`x_to_fr(x)`**: Enhanced to use slope parameter
  - Formula: `Fr = (x - _FRAME_OFFSET) / _FRAME_SLOPE`
  - Inverse of `fr_to_x()` with slope support
  - Implementation: Lines 107-109

- **`build_tank_lookup()`**: Enhanced with auto SG/air_vent assignment
  - Auto SG assignment based on tank name prefix:
    - `FWB*`: SG = 1.025
    - `FWCARGO*`: SG = 1.000
    - Others: SG = 1.000 (default)
  - Auto air_vent assignment based on tank name prefix:
    - `FWB*`: air_vent = 80 mm
    - `FWCARGO*`: air_vent = 125 mm
    - Others: air_vent = "" (empty)
  - Uses `fr_to_x()` for Mid_Fr to x_from_mid_m conversion
  - Implementation: Lines 115-161

#### Stage 5/7 Coordinate Updates
- **Stage 5**: Updated to Frame-based coordinate system
  - Weight: Changed from 434.0 t to **0.0 t** (Ballast only scenario)
  - x coordinate: Changed from 15.27 m to **fr_to_x(52.5) ≈ 22.35 m**
  - Description: "Ballast only at combined FWB1+FWB2 LCG (cargo off)"
  - Implementation: Line 733 in `stage_defaults`

- **Stage 7**: Updated to Frame-based coordinate system
  - Weight: Changed from 434.0 t to **0.0 t** (Cargo off scenario)
  - x coordinate: Changed from 0.63 m to **fr_to_x(30.15) ≈ 0.00 m**
  - Description: "Cargo off (TR removed), symmetric ballast around midship"
  - Implementation: Line 747 in `stage_defaults`

#### Stage Notes Updates
- **Stage 2**: Updated description to "SPMT 1st entry on ramp (light load, initial trim)."
- **Stage 3**: Updated description to "SPMT mid-ramp position (increasing trim)."
- **Stage 5**: Updated description to "Ballast only at combined FWB1+FWB2 LCG (cargo off)."
- **Stage 6A**: Updated description to "TR1 at final deck position (TR2 still on ramp)."
- **Stage 6B**: Updated description to "TR2 mid-ramp (6B ramp mid CG)."
- **Stage 6C**: Updated description to "TR1+TR2 combined CG (symmetric final)."
- **Stage 7**: Updated description to "Cargo off (TR removed), symmetric ballast around midship."
- Implementation: Lines 706-719 in `stage_notes`

#### create_ballast_tanks_sheet() Improvements
- **Simplified structure**: Changed from `tank_config` with tuples to `target_tanks` list
  - Old: `[("FWB1.P", "Y", 1.025, 80), ...]`
  - New: `[("FWB1.P", "Y"), ...]` (SG and air_vent handled by `build_tank_lookup()`)
- **Structured fallback dictionary**: Changed from separate `fallback_x` and `fallback_max_t` to unified `fallback` dictionary
  - Structure: `{"TankName": {"x": value, "max_t": value, "SG": value, "air_vent_mm": value}}`
- **Cleaner data row generation**: Simplified logic using dictionary lookups
- **Better JSON vs fallback indication**: Print message distinguishes between JSON-loaded and fallback data
  - JSON loaded: `"Ballast_Tanks updated with tank_coordinates.json + tank_data.json (2025-11-18)"`
  - Fallback used: `"Ballast_Tanks used fallback hard-coded data (JSON not found)"`
- Implementation: Lines 1332-1417

### Technical Details

- **Source**: Integrated from `p2222.py` guide
- **Frame Mapping**: Automatically initialized from `data/Frame_x_from_mid_m.json` at module load
- **Coordinate System**: All Stage 5/6/7 coordinates now use Frame-based system for consistency
- **Backward Compatibility**: All fallback values maintained for graceful degradation

---

## Version 3.1 (2025-11-18)

### Added

#### Frame_to_x_Table Sheet
- **New Sheet**: `Frame_to_x_Table` (8th sheet)
- **Purpose**: Frame number to x-coordinate conversion table
- **Data Source**: `data/Frame_x_from_mid_m.json`
- **Columns**:
  - `Fr`: Frame number (0.0 to 60.0, 0.5 increments)
  - `x_from_mid_m`: X-coordinate from midship (meters)
  - `비고`: Notes (special positions like "Ramp hinge", "6B ramp 중간", etc.)
- **Rows**: 121 data rows
- **Implementation**:
  - Function: `create_frame_table_sheet(wb)` (lines 1288-1353)
  - JSON file path: `C:\Users\minky\Downloads\src\data\Frame_x_from_mid_m.json`
  - Error handling: FileNotFoundError, JSONDecodeError, KeyError, ValueError
  - Styling: Consistent with other sheets (header font, fill, alignment, borders)
  - Number formatting: "0.00" for Fr and x_from_mid_m columns
  - Column widths: A=12, B=15, C=20

### Technical Details

- **File Size Impact**: +2.54 KB (109.26 KB → 111.80 KB)
- **Sheet Count**: 7 → 8 sheets
- **Integration**: Added to `create_workbook_from_scratch()` after `create_hydro_table_sheet()`

---

## Version 3.0+ (2025-11-18)

### Added

#### RAMP GEOMETRY Section (Calc Sheet)
- **Location**: Rows 32-35 in Calc sheet
- **Parameters**:
  - `ramp_hinge_x_mid_m`: -30.151 m (LBP 60.302 m 기준)
  - `ramp_length_m`: 8.30 m (TRE Cert 2020-08-04)
  - `linkspan_height_m`: 2.00 m
  - `ramp_end_clearance_min_m`: 0.40 m
- **Implementation**: Lines 246-268 in `create_calc_sheet()`

#### HINGE STRESS Section (Calc Sheet)
- **Location**: Rows 36-37 in Calc sheet
- **Parameters**:
  - `hinge_pin_area_m2`: 0.117 m² (Doubler 390x300 mm, Aries)
  - `hinge_limit_rx_t`: 201.60 t (Max Hinge Reaction, duplicate of E23 for clarity)
- **Implementation**: Lines 270-284 in `create_calc_sheet()`

#### Ramp Angle & Pin Stress Columns (RORO Sheet)
- **New Columns**: AP-AS (columns 42-45)
- **Columns**:
  - `Ramp_Angle_deg` (AP, column 42): Calculated ramp angle in degrees
    - Formula: `DEGREES(ASIN((Y{row}-Calc!$E$35)/Calc!$E$33))`
    - Based on Physical Freeboard (Y column) and ramp geometry
  - `Ramp_Angle_Check` (AQ, column 43): Validation against 10° limit
    - Formula: `IF(AP{row}<=10, "OK", "NG")`
  - `Pin_Stress_N/mm²` (AR, column 44): Pin stress calculation
    - Formula: `(AG{row}/4)/Calc!$E$36*9.81/1000`
    - Based on Hinge_Rx_t (AG column) divided by 4 pins
  - `Von_Mises_Check` (AS, column 45): Stress limit validation
    - Formula: `IF(AR{row}<=188, "OK", "NG")`
    - Limit: 188 N/mm²
- **Implementation**: Lines 1150-1188 in `extend_roro_structural_opt1()`
- **Styling**: Structure fill (orange) for header cells

### Changed

#### Hinge_Rx_t Auto-Calculation
- **Previous**: Manual input column
- **Current**: Auto-calculated formula (AG column, column 33)
- **Formula**: `IF(AE{row}="", 45, 45 + AE{row} * 0.545)`
  - Base: 45 t (ramp self-weight)
  - Additional: Share_Load_t (AE column) × 0.545 (share ratio)
- **Implementation**: Lines 1102-1107 in `extend_roro_structural_opt1()`

#### Rx_Check Formula Update
- **Previous**: Referenced `Calc!$E$23` (limit_reaction_t)
- **Current**: References `Calc!$E$37` (hinge_limit_rx_t)
- **Output Change**: "CHECK" → "NG" for failures
- **Formula**: `IF(AG{row}<=Calc!$E$37, "OK", "NG")`
- **Implementation**: Line 1110-1113 in `extend_roro_structural_opt1()`

#### Excel Table Range Extension
- **Previous**: `A14:AO{last_row}` (columns A-AO, 41 columns)
- **Current**: `A14:AS{last_row}` (columns A-AS, 45 columns)
- **Reason**: Added 4 new columns (AP-AS) for Ramp Angle & Pin Stress
- **Implementation**: Line 713 in `create_roro_sheet()`

#### Font Application Loop Update
- **Previous**: `range(5, 32)` (rows 5-31)
- **Current**: `range(5, 39)` (rows 5-38)
- **Reason**: Added RAMP GEOMETRY and HINGE STRESS sections
- **Implementation**: Line 287 in `create_calc_sheet()`

### Technical Details

- **Source Files**: Integrated from `Untitled-4.py`
- **Column Count**: RORO sheet now has 45 columns (was 41)
- **Calc Sheet Rows**: Extended to row 43 (PRECISION PARAMETERS section, was 31 in v3.0, 37 in v3.0+)

---

## Version 3.0 (2025-01-18)

### Added

#### VENT & PUMP Section (Calc Sheet)
- **Location**: Rows 29-31 in Calc sheet
- **Parameters**:
  - `vent_flow_coeff`: 0.86 t/h per mm
    - Note: "실측 보정 0.86 (2025-11-18, MAPE 0.30%)"
    - Updated from 0.85 to 0.86 based on field measurements
  - `pump_rate_tph`: 100.00 t/h (Hired pump rate)
  - `pump_rate_effective_tph`: Calculated effective pump rate
    - Formula: `MIN(E30, SUMPRODUCT((Ballast_Tanks!E$2:E$100="Y")*(Ballast_Tanks!F$2:F$100)*E29))`
    - Accounts for air vent bottleneck
    - Typical value: 68.80 t/h
- **Implementation**: Lines 224-244 in `create_calc_sheet()`

#### Ballast_Tanks Sheet Enhancement
- **New Column**: `air_vent_mm` (6th column, column F)
- **Values**:
  - FWB1.P/S: 80 mm
  - FWB2.P/S: 80 mm
  - FWCARGO1.P/S: 125 mm
  - FWCARGO2.P/S: 125 mm
- **Data Update**: Real measured data from `tank_data.json`
  - 8 tanks total (4 pairs: FWB1, FWB2, FWCARGO1, FWCARGO2)
  - Real measured weights: Weight@100% → max_t
  - Coordinates updated from `tank_coordinates.json`
- **Implementation**: Lines 1204-1248 in `create_ballast_tanks_sheet()`

#### RORO Sheet Pump Rate Reference Update
- **Previous**: Referenced `Calc!$E$12` (old pump_rate_tph)
- **Current**: References `Calc!$E$31` (pump_rate_effective_tph)
- **Location**: Cell C11 in RORO_Stage_Scenarios sheet
- **Label Update**: B11 changed to "pump_rate_effective_tph"
- **Implementation**: Lines 522-523 in `create_roro_sheet()`

#### Stage 6 Split
- **Previous**: Single "Stage 6"
- **Current**: Three stages:
  - `Stage 6A`: 1번 TR만 최종
    - W: 434.0 t, x: 15.27 m
  - `Stage 6B`: 2번 TR ramp 중간
    - W: 434.0 t, x: 10.00 m
  - `Stage 6C`: 완료 (대칭)
    - W: 868.0 t, x: 12.64 m
- **Impact**:
  - Total stages: 10 → 12
  - Row ranges: 15-24 → 15-26
  - Excel Table range: Updated to include new rows
- **Implementation**:
  - Lines 516-528: Stage definitions
  - Lines 539-541: Target trim values
  - Lines 554-556: Stage notes
  - Lines 572-574: Stage defaults

#### Structural Strength Columns (RORO Sheet)
- **New Columns**: AE-AJ (columns 31-36)
- **Columns**:
  - `Share_Load_t` (AE): Input column for share load
  - `Share_Check` (AF): Validation against limit_share_load_t (118.80 t)
  - `Hinge_Rx_t` (AG): Auto-calculated hinge reaction (see Version 3.0+)
  - `Rx_Check` (AH): Validation against hinge_limit_rx_t (201.60 t)
  - `Deck_Press_t/m²` (AI): Deck pressure calculation
  - `Press_Check` (AJ): Validation against limit_deck_press_tpm2 (10.00 t/m²)
- **Styling**: Structure fill (orange) for header cells
- **Implementation**: Lines 1032-1201 in `extend_roro_structural_opt1()`

#### Option 1 Ballast Fix Check Columns (RORO Sheet)
- **New Columns**: AK-AO (columns 37-41)
- **Columns**:
  - `ΔTM_needed_cm·tm` (AK): Required trim moment change
  - `Ballast_req_t` (AL): Required ballast quantity
  - `Ballast_gap_t` (AM): Gap between required and calculated ballast
  - `Time_Add_h` (AN): Additional time needed
  - `Fix_Status` (AO): Overall fix status
    - Checks: max_aft_ballast_cap_t (1200 t) and max_pump_time_h (6 h)
- **Styling**: Option 1 fill (purple) for header cells
- **Implementation**: Lines 1128-1161 in `extend_roro_structural_opt1()`

#### CAPTAIN_REPORT Sheet
- **New Sheet**: `CAPTAIN_REPORT` (7th sheet)
- **Purpose**: Captain/Harbour Master summary report
- **Sections**:
  - LIMIT / REF values (Summer draft limit, Linkspan freeboard limit, etc.)
  - Stage summary table with:
    - Draft values (Dfwd, Daft, Trim)
    - Max draft check (vs 2.70 m)
    - Freeboard check (vs 0.28 m)
    - GM check (vs 1.50 m)
    - Notes
- **Data Source**: References RORO_Stage_Scenarios sheet
- **Implementation**: Lines 761-912 in `create_captain_report_sheet()`

### Changed

#### STRUCTURAL LIMITS Section Notes Update
- **limit_reaction_t** (E23): Note updated to "Aries Ramp hinge limit 201.60 t (share ratio 0.545, 2025-11-18)"
- **linkspan_area_m2** (E26): Note updated to "Linkspan 실제 접지 12.00 m² (Ramp 1 TR only 규정)"
- **Implementation**: Lines 186, 206-207 in `create_calc_sheet()`

#### Row Range Updates
- **extend_roro_captain_req()**: `range(15, 25)` → `range(15, 27)` (12 stages)
- **extend_roro_structural_opt1()**: `range(15, 25)` → `range(15, 27)` (12 stages)
- **create_captain_report_sheet()**: `roro_rows` updated from `[15, ..., 24]` to `[15, ..., 26]`

#### Column Width Updates
- **Calc Sheet**: Column F width increased from 30 to 35
- **RORO Sheet**: New columns AP, AR widths set to 15

### Technical Details

- **Source Files**: Integrated from `Untitled-2.py` and `pss.py`
- **Sheet Count**: 6 → 7 sheets (added CAPTAIN_REPORT)
- **RORO Columns**: Extended from ~30 to 41 columns
- **File Size**: Increased due to new sheets and columns

---

## Version 2.x (Initial Integrated)

### Initial Features

#### Core Sheets
1. **Calc**: Calculator and limits reference sheet
2. **December_Tide_2025**: Tide data (744 rows from JSON)
3. **Hourly_FWD_AFT_Heights**: Hourly draft calculations
4. **RORO_Stage_Scenarios**: Main stage scenario calculations
5. **Ballast_Tanks**: Ballast tank data (8 tanks)
6. **Hydro_Table**: Hydrostatic data for GM lookup

#### Basic Functionality
- Programmatic Excel generation using `openpyxl`
- Formula-based calculations
- Styling and formatting
- JSON data integration
- Error handling

#### Key Parameters
- INPUT CONSTANTS: L_ramp_m, theta_max_deg, KminusZ_m, D_vessel_m
- LIMITS & OPS: min_fwd_draft_m, max_fwd_draft_m, pump_rate_tph
- STABILITY: MTC, LCF, TPC, Lpp
- OPERATIONS: max_fwd_draft_ops_m, ramp_door_offset_m, linkspan_freeboard_target_m, gm_target_m

---

## Migration Notes

### For Users Upgrading from Version 2.x to 3.0+

1. **New Required Data Files**:
   - `data/Frame_x_from_mid_m.json` (for Frame_to_x_Table sheet)
   - Updated `data/tank_data.json` (with air_vent_mm data)
   - Updated `data/tank_coordinates.json`

2. **Formula References**:
   - Update any external references to `Calc!$E$12` (old pump_rate_tph) to `Calc!$E$31` (pump_rate_effective_tph)
   - Update references to `Calc!$E$23` (limit_reaction_t) to `Calc!$E$37` (hinge_limit_rx_t) for Rx_Check

3. **Stage Definitions**:
   - Stage 6 is now split into Stage 6A, 6B, 6C
   - Update any external references to "Stage 6" accordingly
   - **v3.3**: Stage 5 trim target changed from -163.68 cm to -89.58 cm
   - **v3.3**: Stage 7 trim target changed from -96.5 cm to 0.0 cm (Even keel)

4. **New Columns**:
   - RORO sheet now has 45 columns (was 30-41 depending on version)
   - New columns: Structural Strength (AE-AJ), Option 1 (AK-AO), Ramp/Stress (AP-AS)

### For Developers

1. **Function Additions**:
   - `create_frame_table_sheet(wb)`: New sheet creation function
   - `extend_roro_structural_opt1(ws)`: Extended with ramp/stress columns

2. **Code Organization**:
   - Calc sheet sections now extend to row 43 (PRECISION PARAMETERS section)
   - Font application loops updated accordingly (range 5-44)
   - Excel Table ranges updated for new columns

3. **Data Dependencies**:
   - Ensure all JSON data files are in `data/` directory
   - Verify JSON file paths are absolute or relative correctly

---

## Version Summary

| Version | Date | Sheets | RORO Columns | Key Features |
|---------|------|--------|--------------|--------------|
| 3.9 | 2025-11-19 | 8 | 49 | sdsdds.md 가이드 - Stage별 Trim_target 컬럼 추가 (Q열), H열 수식 업데이트, 컬럼 구조 변경 |
| 3.8 | 2025-11-19 | 8 | 48 | zzzzz.md 가이드 - Trim_target 기반 Ballast Fix 수식 패치 (H/J/K/AM~AP 컬럼 업데이트) |
| 3.7 | 2025-11-19 | 8 | 48 | LCF 기반 정밀 Draft 보정 모듈 패치 (aaaa.md), 함수 수정, Excel 수식 수정, AS 컬럼 제거 |
| 3.6 | 2025-11-18 | 8 | 45 | Hydro_Table JSON externalization, fixed vent_rate, improved debug CLI |
| 3.3.1 | 2025-11-18 | 8 | 45 | Row range auto-binding, debug helper function |
| 3.3 | 2025-11-18 | 8 | 45 | Stage 5/7 trim target updates (-89.58 cm, 0.0 cm Even keel) |
| 3.2 | 2025-11-18 | 8 | 45 | Enhanced Frame-based coordinate system, auto Frame mapping, Stage 5/7 updates |
| 3.1 | 2025-11-18 | 8 | 45 | Frame_to_x_Table sheet |
| 3.0+ | 2025-11-18 | 7 | 45 | RAMP GEOMETRY, HINGE STRESS, Ramp/Stress columns |
| 3.0 | 2025-01-18 | 7 | 41 | VENT & PUMP, Structural/Option 1 columns, Stage 6 split |
| 2.x | - | 6 | ~30 | Initial integrated version |

---

## Notes

- All dates are in YYYY-MM-DD format
- Line numbers refer to `agi tr.py` file
- Formula references use Excel notation (e.g., `Calc!$E$31`)
- Column letters use Excel notation (A, B, C, ..., AA, AB, ..., AW)

---

**Document Maintained By**: MACHO-GPT
**Last Review**: 2025-11-19 (Version 3.9)

