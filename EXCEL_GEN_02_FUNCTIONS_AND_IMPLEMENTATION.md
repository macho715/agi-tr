# Excel Generation Script - Functions and Implementation

**Version:** 4.0.0 (DAS Method v4.3 Final Optimized & CAPTAIN_REPORT v4.3)
**Date:** 2025-11-19
**Related:** [EXCEL_GEN_01_OVERVIEW_AND_ARCHITECTURE.md](EXCEL_GEN_01_OVERVIEW_AND_ARCHITECTURE.md)

---

## Table of Contents

1. [Helper Functions](#1-helper-functions)
2. [Calc Sheet Creation](#2-calc-sheet-creation)
3. [Tide Sheet Creation](#3-tide-sheet-creation)
4. [Hourly Sheet Creation](#4-hourly-sheet-creation)
5. [RORO Sheet Creation](#5-roro-sheet-creation)
6. [RORO Sheet Extensions](#6-roro-sheet-extensions)
7. [Additional Sheet Creation Functions](#7-additional-sheet-creation-functions)
8. [Excel Formula Generation](#8-excel-formula-generation)

---

## 1. Helper Functions

### 1.1 get_styles() Function

**Purpose**: Returns a dictionary of pre-configured style objects for consistent formatting across all Excel sheets.

**Return Value**: Dictionary containing 10 style definitions:

| Key | Type | Description | Usage |
|-----|------|-------------|-------|
| `title_font` | `Font` | Large bold title text | Sheet titles, main headings |
| `header_font` | `Font` | Bold white text | Column headers |
| `normal_font` | `Font` | Standard text | Data cells, body text |
| `header_fill` | `PatternFill` | Dark blue background (#1F4E78) | Header row background |
| `input_fill` | `PatternFill` | Light yellow background (#FFF2CC) | User input cells |
| `ok_fill` | `PatternFill` | Light green background (#C6E0B4) | OK status cells |
| `ng_fill` | `PatternFill` | Light orange background (#F8CBAD) | NG/CHECK status cells |
| `structure_fill` | `PatternFill` | Orange background (#C65911) | Structural Strength column headers |
| `opt1_fill` | `PatternFill` | Purple background (#7030A0) | Option 1 Ballast Fix Check column headers |
| `thin_border` | `Side` | Thin gray border | Cell borders |
| `center_align` | `Alignment` | Center-aligned, wrapped | Headers, centered data |
| `left_align` | `Alignment` | Left-aligned, wrapped | Text content |

**Style Specifications**:
- Title Font: Calibri, 18pt, Bold
- Header Font: Calibri, 11pt, Bold, White (#FFFFFF)
- Normal Font: Calibri, 11pt
- Header Fill: Dark blue (#1F4E78)
- Input Fill: Light yellow (#FFF2CC)
- OK Fill: Light green (#C6E0B4)
- NG Fill: Light orange (#F8CBAD)
- Structure Fill: Orange (#C65911) - for Structural Strength columns
- Opt1 Fill: Purple (#7030A0) - for Option 1 Ballast Fix Check columns

### 1.2 Formula Helper Functions

**Note**: These functions are defined but not actively used in the script. The actual formulas are constructed inline using f-strings for better readability and control.

#### create_index_match_formula()
```python
def create_index_match_formula(lookup_value, lookup_range, return_range):
    """INDEX/MATCH 조합 수식 생성"""
    return f'=INDEX({return_range}, MATCH("{lookup_value}", {lookup_range}, 0))'
```

#### create_if_formula()
```python
def create_if_formula(condition, true_value, false_value=""):
    """IF 수식 생성"""
    # Handles string vs. numeric false values
```

#### create_if_or_formula()
```python
def create_if_or_formula(conditions, true_value, false_value=""):
    """IF/OR 조합 수식 생성"""
    # Generates IF/OR formula strings for multiple condition checks
```

### 1.3 Frame Conversion Utilities (v3.2/v3.6)

#### _load_json(filename)
**Purpose**: Enhanced JSON loader with multiple path support for flexible file location.

**Parameters**:
- `filename`: Relative or absolute path to JSON file

**Return Value**: Parsed JSON object (dict/list) or `None` if file not found

**Path Resolution Order**:
1. Script directory (where `agi tr.py` is located)
2. Current working directory
3. `/mnt/data` (Notebook environment)

**Warning Message** (v3.6): Prints `[WARNING] {filename} not found → using fallback` when file not found in any location

**Implementation**: Lines 52-69

**Example**:
```python
data = _load_json("data/Frame_x_from_mid_m.json")
if data:
    # Process data
```

#### _init_frame_mapping()
**Purpose**: Automatically initializes Frame-to-x conversion parameters from JSON file.

**Behavior**:
- Loads `data/Frame_x_from_mid_m.json` using `_load_json()`
- Calculates `_FRAME_SLOPE` and `_FRAME_OFFSET` from first two entries
- Falls back to default values (slope=1.0, offset=-30.15) if JSON not found
- **v3.6**: Now called in `if __name__ == "__main__":` block instead of module level
- **v3.6**: Added INFO messages for default and calculated slope/offset values

**Formula**: `x = _FRAME_OFFSET + _FRAME_SLOPE * Fr`

**Implementation**: Lines 78-110, 1668

#### fr_to_x(fr)
**Purpose**: Converts Frame number to x-coordinate from midship (meters).

**Parameters**:
- `fr`: Frame number (float)

**Return Value**: x-coordinate from midship (float, meters)

**Formula**: `x = _FRAME_OFFSET + _FRAME_SLOPE * Fr`

**Implementation**: Lines 102-104

**Example**:
```python
x = fr_to_x(52.5)  # Returns x-coordinate for Frame 52.5
```

#### x_to_fr(x)
**Purpose**: Converts x-coordinate to Frame number (inverse of `fr_to_x()`).

**Parameters**:
- `x`: x-coordinate from midship (float, meters)

**Return Value**: Frame number (float)

**Formula**: `Fr = (x - _FRAME_OFFSET) / _FRAME_SLOPE`

**Implementation**: Lines 107-109

**Example**:
```python
fr = x_to_fr(22.35)  # Returns Frame number for x=22.35 m
```

#### debug_frame_mapping() (v3.3.1/v3.6)
**Purpose**: Debug helper function to print current Frame mapping parameters and key Stage coordinates.

**Return Value**: None (prints to console, then exits)

**Output Format** (v3.6: improved formatting):
```
============================================================
LCT BUSHRA Frame ↔ x Debug (v3.6)
============================================================
_FRAME_SLOPE  = 1.000000
_FRAME_OFFSET = -30.150
Ramp hinge Fr0            : Fr   0.00 → x  -30.150 m
FWB1+2 LCG                : Fr  52.50 → x   22.350 m
Midship Fr30.15           : Fr  30.15 → x    0.000 m
TR final                  : Fr  42.00 → x   11.850 m
============================================================
```

**Usage**: Run `python "agi tr.py" debug` to verify Frame-to-x conversion parameters.

**v3.6 Enhancements**:
- Improved separator lines (60-char width for better readability)
- Added `sys.exit(0)` to terminate script after debug output
- Prevents accidental Excel file generation when running in debug mode

**Implementation**: Lines 123-142

#### build_tank_lookup()
**Purpose**: Builds tank data lookup dictionary from JSON files with automatic SG/air_vent assignment.

**Data Sources**:
- `data/tank_coordinates.json`: Tank coordinates (Mid_Fr, Weight_MT, Volume_m3)
- `data/tank_data.json`: Tank capacities (Weight_MT, real measured 100% values)

**Return Value**: Dictionary mapping tank names to properties:
```python
{
    "TankName": {
        "x_from_mid_m": float,  # Calculated from Mid_Fr using fr_to_x()
        "max_t": float,         # Weight_MT from tank_data.json or tank_coordinates.json
        "SG": float,            # Auto-assigned: FWB=1.025, FWCARGO=1.000
        "air_vent_mm": int      # Auto-assigned: FWB=80, FWCARGO=125
    }
}
```

**Auto-Assignment Rules**:
- **SG (Specific Gravity)**:
  - `FWB*` tanks: 1.025
  - `FWCARGO*` tanks: 1.000
  - Others: 1.000 (default)
- **air_vent_mm (Air Vent Diameter)**:
  - `FWB*` tanks: 80 mm
  - `FWCARGO*` tanks: 125 mm
  - Others: "" (empty)

**Implementation**: Lines 115-161

**Example**:
```python
lookup = build_tank_lookup()
fwb1_info = lookup.get("FWB1.P", {})
# Returns: {"x_from_mid_m": 57.52, "max_t": 50.57, "SG": 1.025, "air_vent_mm": 80}
```

---

## 2. Calc Sheet Creation

### 2.1 Function: create_calc_sheet()

**Purpose**: Creates the **Calc** sheet, which serves as the central parameter reference for all calculations in the workbook.

**Key Features**:
- Multiple parameters organized into sections (INPUT CONSTANTS, LIMITS & OPS, STABILITY, OPERATIONS, STRUCTURAL LIMITS, BALLAST FIX CHECK, VENT & PUMP, RAMP GEOMETRY, HINGE STRESS, PRECISION PARAMETERS)
- Input cells highlighted with yellow fill
- Clear parameter names, units, and notes
- Referenced by formulas in other sheets
- Includes Comments for key parameters (E40, E41)

### 2.2 Sheet Structure

**Layout**:
- Row 2: Title: "LCT BUSHRA — RORO Calculator & Limits"
- Row 3: Headers: [SECTION | PARAMETER | UNIT | VALUE | NOTES]
- Rows 5-8: INPUT CONSTANTS section
- Rows 10-12: LIMITS & OPS section
- Rows 14-17: STABILITY section
- Rows 18-21: OPERATIONS section
- Rows 23-26: STRUCTURAL LIMITS section
- Rows 27-28: BALLAST FIX CHECK section
- Rows 29-31: VENT & PUMP section
- Rows 32-35: RAMP GEOMETRY section
- Rows 36-37: HINGE STRESS section
- Rows 39-43: PRECISION PARAMETERS section

### 2.3 Parameter Definitions

#### INPUT CONSTANTS Section (Rows 5-8)
- **L_ramp_m** (E5): 12.0 m - Linkspan length
- **theta_max_deg** (E6): 6.0 deg - Maximum ramp angle
- **KminusZ_m** (E7): 3.0 m - K - Z (vertical distance)
- **D_vessel_m** (E8): 3.65 m - Molded depth

#### LIMITS & OPS Section (Rows 10-12)
- **min_fwd_draft_m** (E10): 1.5 m - Minimum forward draft
- **max_fwd_draft_m** (E11): 3.5 m - Maximum forward draft
- **pump_rate_tph** (E12): 10.0 t/h - Pump rate

#### STABILITY Section (Rows 14-17)
- **MTC_t_m_per_cm** (E14): 33.99 t·m/cm - Moment to Change Trim
- **LCF_m_from_midship** (E15): 30.91 m - Longitudinal Center of Flotation
- **TPC_t_per_cm** (E16): 7.95 t/cm - Tons Per Centimeter
- **Lpp_m** (E17): 60.302 m - Length Between Perpendiculars

#### OPERATIONS Section (Rows 18-21)
- **max_fwd_draft_ops_m** (E18): 2.70 m - Max forward draft for operations
- **ramp_door_offset_m** (E19): 0.15 m - Ramp door offset
- **linkspan_freeboard_target_m** (E20): 0.28 m - Linkspan freeboard target
- **gm_target_m** (E21): 1.50 m - GM target

#### STRUCTURAL LIMITS Section (Rows 23-26)
- **limit_reaction_t** (E23): 201.60 t - Max Hinge Reaction (Aries)
- **limit_share_load_t** (E24): 118.80 t - Max Share Load on LCT (Mammoet)
- **limit_deck_press_tpm2** (E25): 10.00 t/m² - Max Deck Pressure (Spec)
- **linkspan_area_m2** (E26): 12.00 m² - Assumed Linkspan Contact Area

#### BALLAST FIX CHECK Section (Rows 27-28)
- **max_aft_ballast_cap_t** (E27): 1200.00 t - Max AFT Ballast Capacity
- **max_pump_time_h** (E28): 6.00 h - Max Allowed Pump Time for Fix

#### VENT & PUMP Section (Rows 29-31)
- **vent_flow_coeff** (E29): 0.86 t/h per mm - 실측 보정 0.86 (2025-11-18, MAPE 0.30%)
- **pump_rate_tph** (E30): 100.00 t/h - Hired pump rate
- **pump_rate_effective_tph** (E31): **Fixed value** - 45.00 t/h (v3.6: changed from formula to fixed value)
  - **Previous** (v3.5 and earlier): Formula calculating effective pump rate based on air vent bottlenecks
  - **Current** (v3.6): Fixed value `45.00 t/h`
  - Note: "FWD tank air vent 제한 (80 mm) → 실효 45 t/h"
  - Cell fill: `input_fill` (yellow background)

#### RAMP GEOMETRY Section (Rows 32-35)
- **ramp_hinge_x_mid_m** (E32): -30.151 m - Ramp hinge x-coordinate from midship
- **ramp_length_m** (E33): 8.30 m - Ramp length (TRE Cert 2020-08-04)
- **linkspan_height_m** (E34): 2.00 m - Linkspan height
- **ramp_end_clearance_min_m** (E35): 0.40 m - Minimum ramp end clearance

#### HINGE STRESS Section (Rows 36-37)
- **hinge_pin_area_m2** (E36): 0.117 m² - Hinge pin area (Doubler 390x300 mm, Aries)
- **hinge_limit_rx_t** (E37): 201.60 t - Max Hinge Reaction (duplicate of E23 for clarity)

#### PRECISION PARAMETERS Section (Rows 39-43)
- **LBP_m** (E40): 60.302 m - Length Between Perpendiculars (for precise draft calculation)
  - Comment: `"LBP (m) - Calc!$E$40"`
  - Used in: LCF 기반 정밀 Draft 보정 모듈
- **LCF_from_mid_m** (E41): 30.910 m - LCF from midship (Fr30.15 기준, for precise draft calculation)
  - Comment: `"LCF from mid (m) - Calc!$E$41"`
  - Used in: LCF 기반 정밀 Draft 보정 모듈
- **dynamic_factor** (E42): 1.15 - Dynamic load amplification factor (for Load Case B)
- **heel_y_offset_m** (E43): 1.50 m - Heel y-offset (for heel angle calculation)

### 2.4 Parameter Lookup Pattern

Other sheets reference Calc sheet parameters using INDEX/MATCH:
```excel
=INDEX(Calc!$E:$E, MATCH("PARAMETER_NAME", Calc!$C:$C, 0))
```

---

## 3. Tide Sheet Creation

### 3.1 Function: create_tide_sheet()

**Purpose**: Creates the **December_Tide_2025** sheet, which contains hourly tide data for the entire month of December 2025.

**Key Features**:
- Automatic JSON data loading
- Graceful degradation if JSON file missing
- Proper date/time formatting
- Numeric formatting for tide values
- Error handling with user-friendly messages

### 3.2 Sheet Structure

**Layout**:
- Row 1: Headers: `["datetime_gst", "tide_m               (Chart Datum)"]`
- Rows 2-745: Data rows (744 entries)

**Data Range**: December 1, 2025 00:00:00 to December 31, 2025 23:00:00 (744 hours)

### 3.3 JSON Data Loading

**File Path**: `C:\Users\minky\Downloads\src\data\gateab_v3_tide_data.json` (absolute path)

**JSON Structure**:
```json
[
  {
    "datetime": "2025-12-01 00:00:00",
    "tide_m": 2.06
  },
  ...
]
```

**Loading Process**:
1. Use fixed absolute path to JSON file
2. Open file with UTF-8 encoding
3. Parse JSON array
4. Loop through each entry
5. Insert data into Excel cells (rows 2-745)

**Note**: Absolute path ensures data is always loaded. The path is fixed to `C:\Users\minky\Downloads\src\data\gateab_v3_tide_data.json` to guarantee data insertion.

### 3.4 Error Handling

**FileNotFoundError**: Creates empty sheet with proper formatting, allows manual data entry

**JSONDecodeError / KeyError / ValueError**: Same graceful degradation as FileNotFoundError

---

## 4. Hourly Sheet Creation

### 4.1 Function: create_hourly_sheet()

**Purpose**: Creates the **Hourly_FWD_AFT_Heights** sheet, which performs hourly calculations for 744 hours (December 1-31, 2025).

**Key Features**:
- 744 rows of calculations (one per hour)
- 10 calculated columns per row = 7,440 formulas
- References multiple sheets (Calc, December_Tide_2025)
- Conditional calculations (IF statements)
- Status validation (OK/CHECK)

### 4.2 Sheet Structure

**Layout**:
- Row 1: Headers (14 columns)
- Rows 2-745: Calculation rows (744 rows)

### 4.3 Column Definitions

| Col | Header | Type | Description |
|-----|--------|------|-------------|
| A | DateTime (GST) | Formula | Date/time from tide sheet |
| B | Tide_m | Formula | Tide value from tide sheet |
| C | Dfwd_req_m (even) | Formula | Required forward draft (even keel) |
| D | Trim_m (optional) | Input | User-entered trim (optional) |
| E | Dfwd_adj_m | Formula | Adjusted forward draft |
| F | Daft_adj_m | Formula | Adjusted aft draft |
| G | Ramp_Angle_deg | Formula | Calculated ramp angle |
| H | Status | Formula | OK or CHECK |
| I | FWD_Height_m | Formula | Forward height above water |
| J | AFT_Height_m | Formula | Aft height above water |
| K | Notes | Formula | "Even Keel" if trim=0 |
| L | (empty) | - | Empty column |
| M | Trim_m (optional) | Input | Duplicate of column D |
| N | (description) | Text | Instructions (row 2 only) |

### 4.4 Key Formulas

#### Column C: Dfwd_req_m (even)
```excel
=IF($A2="","",
 INDEX(Calc!$E:$E, MATCH("KminusZ_m", Calc!$C:$C, 0)) + $B2 -
 INDEX(Calc!$E:$E, MATCH("L_ramp_m", Calc!$C:$C, 0)) *
 TAN(RADIANS(INDEX(Calc!$E:$E, MATCH("theta_max_deg", Calc!$C:$C, 0)))))
```

**Mathematical Formula**: `Dfwd_req = KminusZ + Tide - L_ramp × tan(θ_max)`

#### Column E: Dfwd_adj_m
```excel
=IF($C2="","", IF($D2="", $C2, $C2 - $D2/2))
```

**Mathematical Formula**: `Dfwd_adj = Dfwd_req - Trim/2` (if trim specified)

#### Column G: Ramp_Angle_deg
```excel
=IF($E2="","",
 DEGREES(ATAN((INDEX(Calc!$E:$E, MATCH("KminusZ_m", Calc!$C:$C, 0)) - $E2 + $B2) /
 INDEX(Calc!$E:$E, MATCH("L_ramp_m", Calc!$C:$C, 0)))))
```

**Mathematical Formula**: `θ = arctan((KminusZ - Dfwd + Tide) / L_ramp)`

#### Column H: Status
```excel
=IF($E2="","",
 IF(AND($E2>=INDEX(Calc!$E:$E, MATCH("min_fwd_draft_m", Calc!$C:$C, 0)),
        $E2<=INDEX(Calc!$E:$E, MATCH("max_fwd_draft_m", Calc!$C:$C, 0)),
        $G2<=INDEX(Calc!$E:$E, MATCH("theta_max_deg", Calc!$C:$C, 0))),
    "OK", "CHECK"))
```

**Logic**: Validates that conditions are within safe limits

### 4.5 Formula Count

- **Total Rows**: 744
- **Formulas per Row**: 10 (columns A, B, C, E, F, G, H, I, J, K)
- **Total Formulas**: 7,440
- **Input Cells**: 2 per row (columns D, M) = 1,488 input cells

---

## 5. RORO Sheet Creation

### 5.1 Function: create_roro_sheet()

**Purpose**: Creates the **RORO_Stage_Scenarios** sheet, which performs trim and ballast calculations for 12 different loading stages.

**Return Value** (v3.3.1): Returns tuple `(stages, first_data_row)` where:
- `stages`: List of stage names (9 stages)
- `first_data_row`: First data row number (20, updated from 18 in v3.9.2, was 15)

**Key Features**:
- 9 loading stages (Stage 1-7, Stage 5_PreBallast, Stage 6A_Critical (Opt C))
- Lever-arm ballast calculation model
- Named ranges for formula simplification
- Excel Table structure for easy reference
- Default values for all stages
- Returns stages list and first_data_row for automatic row range binding (v3.3.1)

### 5.2 Sheet Structure

**Layout** (v3.9.2):
- Row 1: Title: "RORO Stage Scenarios – LCT BUSHRA / AGI TR (Stability, Strength & Fix Check)"
- Row 3: Headers (Parameter, Value, Unit, REMARK, Stage, EXPLANATION)
- Rows 4-13: Parameters (A4-A13: Parameter names, B4-B13: Values, C4-C13: Units, D4-D13: REMARK)
  - Parameters: Tmean_baseline, Tide_ref, Trim_target_cm, MTC, LCF, D_vessel, TPC, pump_rate_effective_tph, X_Ballast, Lpp
- Rows 4-15: Stage names and explanations (F4-F15: Stage names, G4-G15: Stage Notes/EXPLANATION)
- Row 19: Table headers (51 columns: A-S original, T(20) removed, U-AD Captain Req, AE-AJ Structural, AK-AO Option 1, AS-AW Ramp/Stress, AX-AY Opt C Tide)
- Rows 20-29: Stage data rows (9 stages)
- Freeze panes: B20

### 5.3 Stage Definitions

1. **Stage 1**: Empty condition (Baseline) – Lightship + constant consumables only
2. **Stage 2**: SPMT 1st entry on ramp (light load, initial trim)
3. **Stage 3**: SPMT mid-ramp position (increasing trim)
4. **Stage 4**: Full on ramp / Break-even (1 unit full weight)
5. **Stage 5**: Ballast only at combined FWB1+FWB2 LCG (cargo off) - **v3.2**: W=0.0, x=fr_to_x(52.5) ≈ 22.35 m - **v3.3**: Trim target updated to **-89.58 cm** (from -163.68 cm, based on new x_CG and lever arm ratio)
6. **Stage 5A-1 (At-Limit)**: TR1 & TR2 at final deck positions. Ballast adjusted to max allowable limit
7. **Stage 5A-2 (Optimized)**: Recommended trim optimization case. Aft ballast ≈ 146t
8. **Stage 5A-3 (Max-Safety)**: Conservative variation of 5A-2
9. **Stage 6A**: TR1 at final deck position (TR2 still on ramp) - **v3.2**: Frame-based x coordinate
10. **Stage 6B**: TR2 mid-ramp (6B ramp mid CG) - **v3.2**: Frame-based x coordinate
11. **Stage 6C**: TR1+TR2 combined CG (symmetric final) - **v3.2**: Frame-based x coordinate
12. **Stage 7**: Cargo off (TR removed), symmetric ballast around midship - **v3.2**: W=0.0, x=fr_to_x(30.15) ≈ 0.00 m - **v3.3**: Trim target updated to **0.0 cm** (Even keel, from -96.5 cm)

### 5.4 Key Column Formulas

#### Column D: TM (t·m) - Trimming Moment
```excel
=IF(OR(B15="", C15="", $C$9=""), "", B15 * (C15 - $C$9))
```

**Mathematical Formula**: `TM = W_stage × (x_stage - LCF)`

#### Column E: Trim_cm
```excel
=IF(OR(D15="", OR($C$8="", $C$8=0)), "", D15 / $C$8)
```

**Mathematical Formula**: `Trim_cm = TM / MTC`

#### Column G: Trim_target_cm
- **Type**: Input (with default values)
- **Description**: Target trim value for each stage (cm)
- **Default Values** (v3.3):
  - Stage 5: **-89.58 cm** (updated from -163.68 cm in v3.3)
  - Stage 7: **0.0 cm** (Even keel, updated from -96.5 cm in v3.3)
  - Other stages: See `target_trim_by_stage` dictionary in code
- **Usage**: Used in Column H (ΔTM) calculation to determine required trimming moment change

#### Column H: ΔTM_cm_tm - Required trimming moment change
```excel
=IF(OR(ISERROR(MTC), ISERROR(TRIM5_CM), G15=""), "",
 ROUND(MTC * (ABS(TRIM5_CM) - ABS(G15)), 2))
```

**Mathematical Formula**: `ΔTM = MTC × (|TRIM5_CM| - |Trim_target_cm|)`

#### Column I: Lever_arm_m
```excel
=IF(OR(ISBLANK($C$12), ISBLANK($C$9), ISERROR($C$9)), "",
 ROUND($C$12 - $C$9, 2))
```

**Mathematical Formula**: `Lever_arm = X_Ballast - LCF`

#### Column J: Ballast_t_calc - Required ballast weight (lever-arm method)
```excel
=IF(OR(H15="", I15=""), "", ROUND(H15 / I15, 2))
```

**Mathematical Formula**: `Ballast_t = ΔTM / Lever_arm`

#### Column L: Ballast_t - Required ballast weight (rule-of-thumb method)
```excel
=IF(OR(F15="", OR($C$10="", $C$10=0)), "",
 ROUND(ABS(F15) * 50 * $C$10, 2))
```

**Mathematical Formula**: `Ballast_t = |Trim_m| × 50 × TPC`

### 5.5 Named Ranges

The function creates the following Excel named ranges (v3.9.2):
- `MTC`: `'RORO_Stage_Scenarios'!$B$7` - Moment to Change Trim (updated from $C$8)
- `LCF`: `'RORO_Stage_Scenarios'!$B$8` - Longitudinal Center of Flotation (updated from $C$9)
- `PumpRate`: `'RORO_Stage_Scenarios'!$B$11` - Ballast pump rate (updated from $C$11)
- `X_Ballast`: `'RORO_Stage_Scenarios'!$B$12` - Ballast position (updated from $C$12)
- `TRIM5_CM`: `'RORO_Stage_Scenarios'!$E${trim5_row}` - Stage 5 trim value (v3.3: -89.58 cm)

### 5.6 Excel Table

**Name**: "Stages"
**Range**: A17:AW29 (header row 17 + 12 data rows 18-29, 49 columns)
**Style**: TableStyleMedium9
**Features**: Row striping, structured references
**Columns**: A-S (original 19 columns), T(20) removed (empty), U-AD (Captain Req, 11 columns), AE-AJ (Structural, 6 columns), AK-AO (Option 1, 5 columns), AS-AW (Ramp/Stress, 4 columns)
**Note** (v3.9.2): T(20) column is empty (Notes moved to G4-G15). Total columns: 49 (was 48).

---

## 6. RORO Sheet Extensions

### 6.1 Function: extend_roro_captain_req(ws, first_data_row, num_stages)

**Purpose**: Extends the RORO_Stage_Scenarios sheet by adding 11 columns (T-AD) for Captain/Harbour Master operational requirements.

**Location**: Called after `create_roro_sheet()` in the main orchestration function.

**Parameters** (v3.3.1):
- `ws`: Worksheet object (RORO_Stage_Scenarios sheet)
- `first_data_row`: First data row number (20 in v4.0.0, was 18 in v3.9.2, was 15)
- `num_stages`: Number of stages (typically 9)

**Return Value**: None (modifies worksheet in place)

**Row Range** (v3.3.1): Automatically calculated as `range(first_data_row, first_data_row + num_stages)` (20-29 in v4.0.0, was 18-29 in v3.9.2, was 15-26). This ensures row ranges automatically adjust when stages are added or removed.

**Column Details**:

#### Column T (20): GM(m)
- **Type**: Formula
- **Formula**: `=IF(O{row}="", "", VLOOKUP(AVERAGE(O{row},P{row}), Hydro_Table!$B:$D, 3, 1))`
- **Description**: Looks up GM value from Hydro_Table based on mean draft (average of forward and aft draft)
- **Cross-sheet Reference**: Hydro_Table sheet (columns B-D)
- **Number Format**: 0.00

#### Column U (21): Fwd Draft(m)
- **Type**: Formula (reference)
- **Formula**: `=O{row}`
- **Description**: Copies forward draft from column O
- **Number Format**: 0.00

#### Column V (22): vs 2.70m
- **Type**: Formula (validation)
- **Formula**: `=IF(U{row}="", "", IF(U{row}<=Calc!$E$18, "OK", "NG"))`
- **Description**: Validates forward draft against summer draft limit (2.70 m from Calc!E18)
- **Output Values**: "OK" if ≤ 2.70m, "NG" if > 2.70m
- **Cross-sheet Reference**: Calc sheet (E18: max_fwd_draft_ops_m)

#### Column W (23): De-ballast Qty(t)
- **Type**: Formula (reference)
- **Formula**: `=J{row}`
- **Description**: Copies calculated ballast quantity from column J
- **Number Format**: 0.00

#### Column X (24): Timing
- **Type**: Input (empty)
- **Description**: User input field for ballast timing information
- **Formatting**: Normal font, no fill

#### Column Y (25): Phys_Freeboard_m
- **Type**: Formula
- **Formula**: `=IF(O{row}="", "", $F$9 - O{row})`
- **Description**: Calculates physical freeboard (vessel depth minus forward draft, no tide)
- **Mathematical Formula**: `Phys_Freeboard = D_vessel - Dfwd`
- **Number Format**: 0.00
- **Cross-sheet Reference**: RORO sheet cell F9 (D_vessel)

#### Column Z (26): Clearance_Check
- **Type**: Formula (validation)
- **Formula**: `=IF(Y{row}="", "", IF(Y{row}>=Calc!$E$20, "OK", "<0.28m CHECK"))`
- **Description**: Validates physical freeboard against linkspan freeboard limit (0.28 m from Calc!E20)
- **Output Values**: "OK" if ≥ 0.28m, "<0.28m CHECK" if < 0.28m
- **Cross-sheet Reference**: Calc sheet (E20: linkspan_freeboard_target_m)

#### Column AA (27): GM_calc
- **Type**: Formula (reference)
- **Formula**: `=T{row}`
- **Description**: Copies GM value from column T
- **Number Format**: 0.00

#### Column AB (28): GM_Check
- **Type**: Formula (validation)
- **Formula**: `=IF(AA{row}="", "", IF(AA{row}>=Calc!$E$21, "OK", "NG"))`
- **Description**: Validates GM against target GM (1.50 m from Calc!E21)
- **Output Values**: "OK" if ≥ 1.50m, "NG" if < 1.50m
- **Cross-sheet Reference**: Calc sheet (E21: gm_target_m)

#### Column AC (29): Prop Imm(%)
- **Type**: Formula
- **Formula**: `=IF(P{row}="", "", (P{row}-2.10)/1.25*100)`
- **Description**: Calculates propeller immersion percentage
- **Mathematical Formula**: `Prop_Imm = ((Daft - 2.10) / 1.25) × 100`
- **Number Format**: 0.00
- **Assumptions**: Propeller reference depth = 2.10 m, immersion range = 1.25 m

#### Column AD (30): Vent_Time_h
- **Type**: Formula
- **Formula**: `=IF(W{row}>0, W{row}/45, "-")`
- **Description**: Calculates ventilation time based on ballast quantity
- **Mathematical Formula**: `Vent_Time = Ballast_Qty / 45` (if ballast > 0)
- **Number Format**: 0.00
- **Output**: Time in hours or "-" if no ballast

**Row Range** (v3.3.1): Automatically calculated as `range(first_data_row, first_data_row + num_stages)` (20-29 in v4.0.0, was 18-29 in v3.9.2, was 15-26 for 9 stages)

**Column Widths**:
- T: 12, U: 12, V: 12, W: 15, X: 12, Y: 18, Z: 15, AA: 12, AB: 12, AC: 12, AD: 12

### 6.2 Function: extend_roro_structural_opt1(ws, first_data_row, num_stages)

**Purpose**: Extends the RORO_Stage_Scenarios sheet further by adding Structural Strength validation columns (AE-AJ), Option 1 Ballast Fix Check columns (AK-AO), and Ramp/Stress columns (AS-AV).

**Location**: Called after `extend_roro_captain_req()` in the main orchestration function.

**Parameters** (v3.3.1):
- `ws`: Worksheet object (RORO_Stage_Scenarios sheet)
- `first_data_row`: First data row number (20 in v4.0.0, was 18 in v3.9.2, was 15)
- `num_stages`: Number of stages (typically 9)

**Return Value**: None (modifies worksheet in place)

**Row Range** (v3.3.1): Automatically calculated as `range(first_data_row, first_data_row + num_stages)` (20-29 in v4.0.0, was 18-29 in v3.9.2, was 15-26). This ensures row ranges automatically adjust when stages are added or removed.

**Structural Strength Columns (AE-AJ, columns 31-36)**:

#### Column AE (31): Share_Load_t
- **Type**: Input
- **Description**: User input for share load on LCT
- **Formatting**: Yellow fill (input_fill), normal font
- **Usage**: Enter actual share load value for each stage

#### Column AF (32): Share_Check
- **Type**: Formula (validation)
- **Formula**: `=IF(AE{row}="", "", IF(AE{row}<=Calc!$E$24, "OK", "CHECK"))`
- **Description**: Validates share load against limit (118.80 t from Calc!E24)
- **Output Values**: "OK" if ≤ 118.80t, "CHECK" if > 118.80t
- **Cross-sheet Reference**: Calc sheet (E24: limit_share_load_t)

#### Column AG (33): Hinge_Rx_t
- **Type**: Formula (auto-calculated)
- **Formula**: `=IF(AE{row}="", 45, 45 + AE{row} * 0.545)`
- **Description**: Auto-calculated hinge reaction force (Ramp self-weight 45t + share 54.5%)
- **Mathematical Formula**: `Hinge_Rx = 45 + Share_Load × 0.545`
- **Number Format**: 0.00
- **Formatting**: Normal font (no input fill, as it's calculated)
- **Usage**: Automatically calculates hinge reaction based on Share_Load input

#### Column AH (34): Rx_Check
- **Type**: Formula (validation)
- **Formula**: `=IF(AG{row}="", "", IF(AG{row}<=Calc!$E$23, "OK", "NG"))`
- **Description**: Validates hinge reaction against limit (201.60 t from Calc!E23)
- **Output Values**: "OK" if ≤ 201.60t, "NG" if > 201.60t
- **Cross-sheet Reference**: Calc sheet (E23: limit_reaction_t)

#### Column AI (35): Deck_Press_t/m²
- **Type**: Formula
- **Formula**: `=IF(AE{row}="", "", AE{row}/Calc!$E$26)`
- **Description**: Calculates deck pressure from share load and linkspan area
- **Mathematical Formula**: `Deck_Press = Share_Load / linkspan_area`
- **Number Format**: 0.00
- **Cross-sheet Reference**: Calc sheet (E26: linkspan_area_m2)

#### Column AJ (36): Press_Check
- **Type**: Formula (validation)
- **Formula**: `=IF(AI{row}="", "", IF(AI{row}<=Calc!$E$25, "OK", "CHECK"))`
- **Description**: Validates deck pressure against limit (10.00 t/m² from Calc!E25)
- **Output Values**: "OK" if ≤ 10.00 t/m², "CHECK" if > 10.00 t/m²
- **Cross-sheet Reference**: Calc sheet (E25: limit_deck_press_tpm2)

**Option 1 Ballast Fix Check Columns (AK-AO, columns 37-41)**:

#### Column AK (37): ΔTM_needed_cm·tm
- **Type**: Formula
- **Formula**: `=IF(OR(E{row}="", G{row}=""), "", Calc!$E$14 * (ABS(E{row}) - ABS(G{row})))`
- **Description**: Calculates required trimming moment change to achieve target trim
- **Mathematical Formula**: `ΔTM = MTC × (|Trim_cm| - |Trim_target_cm|)`
- **Number Format**: 0.00
- **Cross-sheet Reference**: Calc sheet (E14: MTC_t_m_per_cm)

#### Column AL (38): Ballast_req_t
- **Type**: Formula
- **Formula**: `=IF(AK{row}="", "", AK{row}/I{row})`
- **Description**: Calculates required ballast weight using lever-arm method
- **Mathematical Formula**: `Ballast_req = ΔTM / Lever_arm`
- **Number Format**: 0.00
- **Cross-sheet Reference**: Column I (Lever_arm_m)

#### Column AM (39): Ballast_gap_t
- **Type**: Formula
- **Formula**: `=IF(AL{row}="", "", AL{row} - IF(J{row}="", 0, J{row}))`
- **Description**: Calculates gap between required ballast and calculated ballast
- **Mathematical Formula**: `Ballast_gap = Ballast_req - Ballast_calc`
- **Number Format**: 0.00
- **Cross-sheet Reference**: Column J (Ballast_t_calc)

#### Column AN (40): Time_Add_h
- **Type**: Formula
- **Formula**: `=IF(AM{row}="", "", ABS(AM{row})/Calc!$E$12)`
- **Description**: Calculates additional pumping time needed to close the ballast gap
- **Mathematical Formula**: `Time_Add = |Ballast_gap| / PumpRate`
- **Number Format**: 0.00
- **Cross-sheet Reference**: Calc sheet (E12: pump_rate_tph)

#### Column AO (41): Fix_Status
- **Type**: Formula (validation)
- **Formula**: `=IF(AL{row}="", "", IF(AL{row}<=Calc!$E$27, IF(AN{row}<=Calc!$E$28, "OK", "NG (Time>6h)"), "NG (Cap>1200t)"))`
- **Description**: Validates ballast fix check against capacity and time limits
- **Output Values**:
  - "OK" if ballast ≤ 1200t AND time ≤ 6h
  - "NG (Cap>1200t)" if ballast > 1200t
  - "NG (Time>6h)" if time > 6h
- **Cross-sheet References**:
  - Calc sheet (E27: max_aft_ballast_cap_t = 1200.00 t)
  - Calc sheet (E28: max_pump_time_h = 6.00 h)

**Ramp Angle & Pin Stress Columns (AS-AV, columns 45-48)**:

#### Column AS (45): Ramp_Angle_deg
- **Type**: Formula
- **Formula**: `=IF(Y{row}="","",DEGREES(ASIN((Y{row}-Calc!$E$35)/Calc!$E$33)))`
- **Description**: Calculates ramp angle in degrees based on Physical Freeboard (Y column) and ramp geometry
- **Mathematical Formula**: `θ = arcsin((Phys_Freeboard - ramp_end_clearance_min) / ramp_length)`
- **Number Format**: 0.00
- **Cross-sheet References**:
  - Column Y (Phys_Freeboard_m)
  - Calc sheet (E33: ramp_length_m)
  - Calc sheet (E35: ramp_end_clearance_min_m)

#### Column AT (46): Ramp_Angle_Check
- **Type**: Formula (validation)
- **Formula**: `=IF(AS{row}="","",IF(AS{row}<=10,"OK","NG"))`
- **Description**: Validates ramp angle against 10° limit
- **Output Values**: "OK" if ≤ 10°, "NG" if > 10°
- **Limit**: 10° maximum ramp angle

#### Column AU (47): Pin_Stress_N/mm²
- **Type**: Formula
- **Formula**: `=IF(AG{row}="","",(AG{row}/4)/Calc!$E$36*9.81/1000)`
- **Description**: Calculates pin stress based on Hinge_Rx_t (AG column) divided by 4 pins
- **Mathematical Formula**: `Pin_Stress = (Hinge_Rx / 4) / hinge_pin_area × 9.81 / 1000`
- **Number Format**: 0.00
- **Cross-sheet References**:
  - Column AG (Hinge_Rx_t)
  - Calc sheet (E36: hinge_pin_area_m2)

#### Column AV (48): Von_Mises_Check
- **Type**: Formula (validation)
- **Formula**: `=IF(AU{row}="","",IF(AU{row}<=188,"OK","NG"))`
- **Description**: Validates pin stress against Von Mises stress limit
- **Output Values**: "OK" if ≤ 188 N/mm², "NG" if > 188 N/mm²
- **Limit**: 188 N/mm² maximum stress

**Color Coding**:
- Structural columns (AE-AJ): Orange header fill (structure_fill, #C65911)
- Option 1 columns (AK-AO): Purple header fill (opt1_fill, #7030A0)
- Ramp/Stress columns (AS-AV): Orange header fill (structure_fill, #C65911)

**Row Range** (v3.3.1): Automatically calculated as `range(first_data_row, first_data_row + num_stages)` (20-29 in v4.0.0, was 18-29 in v3.9.2, was 15-26 for 9 stages)

**Column Widths**: All columns 11, except AO (Status) = 18, AS (Ramp Angle) = 15, AU (Pin Stress) = 15

---

## 7. Additional Sheet Creation Functions

### 7.1 Function: create_captain_report_sheet(wb, stages, first_data_row)

**Purpose**: Creates the **CAPTAIN_REPORT** sheet, a summary sheet for Captain/Harbour Master with DAS Method operational limits and stage-by-stage safety checks. Updated for v4.3: DAS Method & Critical Checkpoints Highlight.

**Location**: Created after all RORO sheet extensions in the main orchestration function.

**Parameters** (v3.3.1):
- `wb`: Workbook object
- `stages`: List of stage names (from `create_roro_sheet()`)
- `first_data_row`: First data row number in RORO_Stage_Scenarios sheet (20 in v4.0.0, was 18 in v3.9.2, was 15)

**Return Value**: None (creates new sheet in workbook)

**Sheet Removal Logic** (v4.3): If CAPTAIN_REPORT sheet already exists, it is removed before creating a new one to ensure clean state.

**Row Mapping** (v3.3.1): `roro_rows` is automatically calculated as `[first_data_row + i for i in range(len(stages))]` (20-29 in v4.0.0, was 18-29 in v3.9.2, was 15-26). This ensures row mapping automatically adjusts when stages are added or removed.

**Sheet Structure** (v4.3):

#### Row 1: Title
- **Cell**: A1 (merged A1:J1)
- **Value**: "LCT BUSHRA – OPERATION SUMMARY (DAS METHOD)"
- **Formatting**: Title font, center-aligned, header fill (dark blue)

#### Row 3: OPERATIONAL LIMITS Section Header
- **Cell**: A3 (merged A3:D3)
- **Value**: "1. OPERATIONAL LIMITS"
- **Formatting**: Header font, structure fill (orange background)

#### Row 4: OPERATIONAL LIMITS Table Headers
- **Columns**: A-D
- **Headers**: ["PARAMETER", "LIMIT", "UNIT", "REMARK"]
- **Formatting**: Header font, header fill, center-aligned, borders

#### Rows 5-8: OPERATIONAL LIMITS Parameters

**Row 5: Summer Draft Max**
- **A5**: "Summer Draft Max"
- **B5**: 2.70 (hardcoded value)
- **C5**: "m"
- **D5**: "Operational Limit (Harbour: Check Depth)"
- **Formatting**: B5 has input fill (yellow), number format 0.00

**Row 6: Min Freeboard**
- **A6**: "Min Freeboard"
- **B6**: 0.28 (hardcoded value)
- **C6**: "m"
- **D6**: "Linkspan Connection Safety"
- **Formatting**: B6 has input fill (yellow), number format 0.00

**Row 7: Min GM**
- **A7**: "Min GM"
- **B7**: 1.50 (hardcoded value)
- **C7**: "m"
- **D7**: "Stability Requirement"
- **Formatting**: B7 has input fill (yellow), number format 0.00

**Row 8: Max Ramp Angle**
- **A8**: "Max Ramp Angle"
- **B8**: 6.0 (hardcoded value)
- **C8**: "deg"
- **D8**: "SPMT Climbing Limit"
- **Formatting**: B8 has input fill (yellow), number format 0.00

#### Row 9: STAGE-BY-STAGE SAFETY CHECK Section Header
- **Cell**: A9 (merged A9:J9)
- **Value**: "2. STAGE-BY-STAGE SAFETY CHECK"
- **Formatting**: Header font, structure fill (orange background)

#### Row 10: STAGE-BY-STAGE SAFETY CHECK Table Headers
- **Columns**: A-I (9 columns)
- **Headers**: ["Stage", "Condition", "Trim (m)", "Fwd Draft", "Aft Draft", "Draft Check", "Freeboard", "Deck Check", "Action / Note"]
- **Formatting**: Header font, header fill, center-aligned, borders

#### Rows 11-22: Stage Summary Data (9 stages, or number of stages)

**Column A: Stage name**
- **Formula**: `='RORO_Stage_Scenarios'!A{roro_row}`
- **Type**: Reference
- **Row Mapping**: RORO rows 18-29 → CAPTAIN_REPORT rows 11-22 (v3.9.2, was 15-26)

**Column B: Condition**
- **Formula**: `=IF(ISNUMBER(SEARCH("PreBallast",A{row})),"PRE-BALLAST",IF(ISNUMBER(SEARCH("Critical",A{row})),"CRITICAL","NORMAL"))`
- **Type**: Calculated (auto-classification)
- **Description**: Automatically classifies stage condition based on stage name
- **Output Values**: 
  - "PRE-BALLAST" if stage name contains "PreBallast"
  - "CRITICAL" if stage name contains "Critical"
  - "NORMAL" otherwise

**Column C: Trim (m)**
- **Formula**: `='RORO_Stage_Scenarios'!F{roro_row}`
- **Type**: Reference
- **Number Format**: 0.00

**Column D: Fwd Draft**
- **Formula**: `='RORO_Stage_Scenarios'!O{roro_row}`
- **Type**: Reference
- **Number Format**: 0.00

**Column E: Aft Draft**
- **Formula**: `='RORO_Stage_Scenarios'!P{roro_row}`
- **Type**: Reference
- **Number Format**: 0.00

**Column F: Draft Check**
- **Formula**: `=IF(B{row}="PRE-BALLAST", "CHECK DEPTH", IF(MAX(D{row},E{row})<=$B$5, "OK", "OVER DRAFT"))`
- **Type**: Validation (conditional logic)
- **Description**: 
  - For PRE-BALLAST stages: Returns "CHECK DEPTH" (intentional high trim warning)
  - For other stages: Validates max draft against 2.70 m limit (B5)
- **Output Values**: 
  - "CHECK DEPTH" for PRE-BALLAST stages
  - "OK" if max draft ≤ 2.70m
  - "OVER DRAFT" if max draft > 2.70m

**Column G: Freeboard**
- **Formula**: `='RORO_Stage_Scenarios'!Z{roro_row}`
- **Type**: Reference
- **Description**: Physical freeboard from RORO sheet column Z (Phys_Freeboard_m)
- **Number Format**: 0.00
- **Cross-sheet Reference**: RORO_Stage_Scenarios column Z (26) - Phys_Freeboard_m

**Column H: Deck Check**
- **Formula**: `=IF(G{row}>=$B$6, "OK", "SUBMERGED/LOW")`
- **Type**: Validation
- **Description**: Validates physical freeboard against 0.28 m limit (B6)
- **Output Values**: 
  - "OK" if freeboard ≥ 0.28m
  - "SUBMERGED/LOW" if freeboard < 0.28m

**Column I: Action / Note**
- **Formula**: `='RORO_Stage_Scenarios'!G{4 + idx}`
- **Type**: Reference
- **Description**: Stage explanation from RORO sheet column G (Explanation column)
- **Alignment**: Left-aligned, wrapped

**Formatting**:
- All numeric columns (C-E, G): Number format 0.00, normal font
- Text columns (A, B, F, H, I): Left-aligned, normal font
- All cells: Borders applied (bottom border)
- **Critical Stages Highlighting** (v4.3): Stages containing "PreBallast" or "Critical" in name have yellow background fill (input_fill) applied to all columns
- Freeze panes: Not explicitly set (can be added if needed)

**Column Widths**:
- A: 25, B: 15, C: 10, D: 10, E: 10, F: 15, G: 10, H: 15, I: 50

**Implementation Notes** (v4.3):
- Sheet removal logic ensures clean state on regeneration
- Condition column provides automatic stage classification for DAS Method workflow
- Draft Check uses conditional logic to handle PRE-BALLAST stages differently
- Critical stages (PreBallast, Critical) are visually highlighted with yellow background
- Freeboard reference updated from column Y to column Z (26) - Phys_Freeboard_m

### 7.2 Function: create_ballast_tanks_sheet(wb)

**Purpose**: Creates the **Ballast_Tanks** sheet, a reference sheet containing ballast tank specifications with real measured data from tank_data.json (2025-11-18).

**Location**: Created after RORO sheet, before extensions in the main orchestration function.

**Parameters**:
- `wb`: Workbook object

**Return Value**: None (creates new sheet in workbook)

**Data Source** (v3.2 Enhanced): JSON-based lookup with fallback values
- Primary: `data/tank_coordinates.json` + `data/tank_data.json` via `build_tank_lookup()`
- Fallback: Hardcoded values if JSON files not found
- Coordinates: Calculated from `Mid_Fr` using `fr_to_x()` function
- SG and air_vent: Auto-assigned based on tank name prefix

**Sheet Structure**:

#### Row 1: Headers
- **Columns**: A-F
- **Headers**: ["TankName", "x_from_mid_m", "max_t", "SG", "use_flag", "air_vent_mm"]

#### Rows 2-9: Tank Data (8 tanks)

**Tank Entries**:

1. **FWB1.P** (Row 2)
   - x_from_mid_m: 57.52 m (aft of midship)
   - max_t: 50.57 t (real Weight@100%)
   - SG: 1.025
   - use_flag: "Y"
   - air_vent_mm: 80 mm

2. **FWB1.S** (Row 3)
   - x_from_mid_m: 57.52 m (aft of midship)
   - max_t: 50.57 t (real Weight@100%)
   - SG: 1.025
   - use_flag: "Y"
   - air_vent_mm: 80 mm

3. **FWB2.P** (Row 4)
   - x_from_mid_m: 50.04 m (aft of midship)
   - max_t: 109.98 t (real Weight@100%)
   - SG: 1.025
   - use_flag: "Y"
   - air_vent_mm: 80 mm

4. **FWB2.S** (Row 5)
   - x_from_mid_m: 50.04 m (aft of midship)
   - max_t: 109.98 t (real Weight@100%)
   - SG: 1.025
   - use_flag: "Y"
   - air_vent_mm: 80 mm

5. **FWCARGO1.P** (Row 6)
   - x_from_mid_m: 42.75 m (aft of midship)
   - max_t: 148.35 t (real Weight@100%)
   - SG: 1.000
   - use_flag: "N" (selectable, not default active)
   - air_vent_mm: 125 mm

6. **FWCARGO1.S** (Row 7)
   - x_from_mid_m: 42.75 m (aft of midship)
   - max_t: 148.35 t (real Weight@100%)
   - SG: 1.000
   - use_flag: "N" (selectable, not default active)
   - air_vent_mm: 125 mm

7. **FWCARGO2.P** (Row 8)
   - x_from_mid_m: 35.25 m (aft of midship)
   - max_t: 148.36 t (real Weight@100%)
   - SG: 1.000
   - use_flag: "N" (selectable, not default active)
   - air_vent_mm: 125 mm

8. **FWCARGO2.S** (Row 9)
   - x_from_mid_m: 35.25 m (aft of midship)
   - max_t: 148.36 t (real Weight@100%)
   - SG: 1.000
   - use_flag: "N" (selectable, not default active)
   - air_vent_mm: 125 mm

**Implementation Details** (v3.2):

1. **JSON Lookup**: Calls `build_tank_lookup()` to merge data from `tank_coordinates.json` and `tank_data.json`
2. **Target Tanks List**: Simplified structure `[("TankName", "use_flag"), ...]`
3. **Fallback Dictionary**: Structured as `{"TankName": {"x": value, "max_t": value, "SG": value, "air_vent_mm": value}}`
4. **Data Row Generation**: Uses dictionary lookups with fallback values
5. **Auto-Assignment**: SG and air_vent automatically assigned by `build_tank_lookup()` based on tank name prefix

**Key Notes**:
- **x_from_mid_m**: Calculated from `Mid_Fr` using `fr_to_x()` function (Frame-based coordinate system)
- **max_t**: Real Weight@100% values from `tank_data.json` (preferred) or `tank_coordinates.json` (fallback)
- **use_flag**: FWB tanks default to "Y" (active), FWCARGO tanks default to "N" (selectable, not default active)
- **SG**: Auto-assigned: FWB=1.025, FWCARGO=1.000
- **air_vent_mm**: Auto-assigned: FWB=80mm, FWCARGO=125mm. Used in pump rate effective calculation (Calc sheet E31)

**Formatting**:
- Headers: Header font, header fill, center-aligned, borders
- Data rows: Normal font
- Columns C, D, and F (max_t, SG, air_vent_mm): Number format 0.00
- Column widths: A: 15, B: 15, C: 12, D: 10, E: 10, F: 14

**Print Messages** (v3.2):
- JSON loaded: `"  [OK] Ballast_Tanks updated with tank_coordinates.json + tank_data.json (2025-11-18)"`
- Fallback used: `"  [WARN] Ballast_Tanks used fallback hard-coded data (JSON not found)"`

**Implementation**: Lines 1332-1417

**Usage**: Reference data for ballast operations. The air_vent_mm column was previously used in the Calc sheet's `pump_rate_effective_tph` calculation (E31), but as of v3.6, E31 is a fixed value (45.00 t/h). Not directly used in other formulas, but provides operational reference for users.

### 7.3 Function: create_hydro_table_sheet(wb)

**Purpose**: Creates the **Hydro_Table** sheet, a hydrostatic data table used for GM lookup in the RORO sheet.

**Location**: Created after Ballast_Tanks sheet in the main orchestration function.

**Parameters**:
- `wb`: Workbook object

**Return Value**: None (creates new sheet in workbook)

**Data Source** (v3.6): JSON-based loading with fallback
- **Primary**: Loads from `data/hydro_table.json` using `_load_json()` function
- **Format Support**:
  - Dict list format: `[{"Disp_t": ..., "Tmean_m": ..., ...}, ...]`
  - Array format: `[[...], ...]`
- **Data Points**: 12 hydrostatic data points (up from 4 hardcoded points)
- **Fallback**: Falls back to 4 hardcoded points if JSON not found or invalid
- **Print Messages**:
  - Success: `"  [OK] Hydro_Table loaded from JSON ({len(data)} points)"`
  - Fallback: `"  [FALLBACK] Using built-in 4 points"`

**Sheet Structure**:

#### Row 1: Headers
- **Columns**: A-F
- **Headers**: ["Disp_t", "Tmean_m", "Trim_m", "GM_m", "Draft_FWD", "Draft_AFT"]

#### Rows 2-13: Hydrostatic Data (12 entries from JSON, or 4 if fallback)

**Data Loading Process** (v3.6):
1. Attempts to load `data/hydro_table.json` using `_load_json()`
2. If JSON is dict list format, converts to array format
3. If JSON is already array format, uses directly
4. If JSON not found or invalid, uses fallback 4-point data

**Fallback Hydrostatic Data Entries** (used if JSON not found):

1. **Entry 1** (Row 2)
   - Disp_t: 2991.25 t
   - Tmean_m: 2.20 m
   - Trim_m: 0.20 m
   - GM_m: 2.85 m
   - Draft_FWD: 2.10 m
   - Draft_AFT: 2.30 m

2. **Entry 2** (Row 3)
   - Disp_t: 3208.25 t
   - Tmean_m: 3.18 m
   - Trim_m: -0.53 m
   - GM_m: 1.68 m
   - Draft_FWD: 2.92 m
   - Draft_AFT: 3.45 m

3. **Entry 3** (Row 4)
   - Disp_t: 3265.25 t
   - Tmean_m: 3.00 m
   - Trim_m: 0.60 m
   - GM_m: 1.88 m
   - Draft_FWD: 2.68 m
   - Draft_AFT: 3.28 m

4. **Entry 4** (Row 5)
   - Disp_t: 3425.25 t
   - Tmean_m: 3.00 m
   - Trim_m: 0.70 m
   - GM_m: 1.85 m
   - Draft_FWD: 2.65 m
   - Draft_AFT: 3.35 m

**Note**: When JSON is loaded successfully, the sheet contains 12 data rows (rows 2-13) instead of 4.

**Formatting**:
- Headers: Header font, header fill, center-aligned, borders
- Data rows: Normal font, number format 0.00 for all numeric columns
- Column widths: All columns (A-F): 12

**VLOOKUP Usage in RORO Sheet**:

The Hydro_Table is used in the RORO sheet (column T, GM lookup) with the following formula:

```excel
=VLOOKUP(AVERAGE(O{row},P{row}), Hydro_Table!$B:$D, 3, 1)
```

**Formula Components**:
- **Lookup Key**: `AVERAGE(O{row},P{row})` - Mean draft (average of forward and aft draft)
- **Lookup Range**: `Hydro_Table!$B:$D` - Columns B (Tmean_m) to D (GM_m)
- **Return Column**: `3` - Column D (GM_m)
- **Match Type**: `1` - Approximate match (ascending order)

**Data Ordering Requirement**: The data must be sorted by Tmean_m (column B) in ascending order for VLOOKUP with match type 1 to work correctly.

**Usage**: Provides GM values for different mean draft conditions. Used by `extend_roro_captain_req()` function in column T (GM lookup).

**Implementation**: Lines 1454-1521

**v3.6 Enhancements**:
- JSON-based data loading with 12 data points support
- Automatic format detection (dict list vs array)
- Graceful fallback to 4 hardcoded points if JSON not found
- Informative print messages for debugging

### 7.4 Function: create_frame_table_sheet(wb)

**Purpose**: Creates the **Frame_to_x_Table** sheet, a reference table for Frame number to x-coordinate conversion.

**Location**: Created after Hydro_Table sheet in the main orchestration function.

**Parameters**:
- `wb`: Workbook object

**Return Value**: None (creates new sheet in workbook)

**Data Source**: `C:\Users\minky\Downloads\src\data\Frame_x_from_mid_m.json` (absolute path)

**Sheet Structure**:

#### Row 1: Headers
- **Columns**: A-C
- **Headers**: ["Fr", "x_from_mid_m", "비고"]

#### Rows 2-122: Frame Data (121 entries)

**Data Format**:
- `Fr`: Frame number (0.0 to 60.0, 0.5 increments)
- `x_from_mid_m`: X-coordinate from midship (meters)
- `비고`: Notes (special positions like "Ramp hinge", "6B ramp 중간", etc.)

**Loading Process**:
1. Use fixed absolute path to JSON file
2. Open file with UTF-8 encoding
3. Parse JSON array
4. Loop through each entry
5. Insert data into Excel cells (rows 2-122)

**Error Handling**:
- **FileNotFoundError**: Creates empty sheet with proper formatting (121 rows)
- **JSONDecodeError / KeyError / ValueError**: Same graceful degradation as FileNotFoundError

**Formatting**:
- Headers: Header font, header fill, center-aligned, borders
- Data rows: Normal font, number format "0.00" for Fr and x_from_mid_m columns
- Column widths: A: 12, B: 15, C: 20

**Print Messages**:
- Success: `"  [OK] Frame_to_x_Table sheet created with {len(frame_data)} rows"`
- Warning: `"  [WARNING] JSON file not found. Creating empty Frame_to_x_Table sheet."`

**Implementation**: Lines 1461-1527

**Usage**: Reference data for Frame-to-x coordinate conversion. Used by `_init_frame_mapping()` for automatic slope/offset estimation, and provides lookup table for users.

---

## 8. Excel Formula Generation

### 8.1 Formula Construction Patterns

#### Basic Pattern
**Template**: `f'=FORMULA({arguments})'`

**Example**:
```python
ws.cell(row=2, column=1).value = f'=IF($A2="","",$B2)'
```

#### Multi-Line Formulas
For complex formulas, Python uses parentheses for line continuation:
```python
ws.cell(row=row, column=3).value = (
    f'=IF($A{row_str}="","", '
    f'INDEX(Calc!$E:$E, MATCH("KminusZ_m", Calc!$C:$C, 0)) + $B{row_str} - '
    f'INDEX(Calc!$E:$E, MATCH("L_ramp_m", Calc!$C:$C, 0)) * '
    f'TAN(RADIANS(INDEX(Calc!$E:$E, MATCH("theta_max_deg", Calc!$C:$C, 0)))))'
)
```

#### Row Number Variable
**Pattern**: `row_str = str(row)` then `f'=IF($A{row_str}="","",...)'`

### 8.2 Cell Reference Patterns

#### Absolute References
**Pattern**: `$Column$Row`
**Usage**: Fixed cell references that don't change when copied
**Example**: `f'$C$8'` - Always refers to column C, row 8

#### Mixed References
**Pattern**: `$ColumnRow` or `Column$Row`
**Example**: `f'$A{row_str}'` - Column A is absolute, row is relative

#### Relative References
**Pattern**: `ColumnRow`
**Example**: `f'B{row_str}'` - Both column and row are relative

### 8.3 Cross-Sheet References

#### Basic Syntax
**Pattern**: `SheetName!CellReference`
**Example**: `f'December_Tide_2025!A{row_str}'`

#### INDEX/MATCH Pattern
**Common Pattern**: Lookup parameter from Calc sheet
```python
f'INDEX(Calc!$E:$E, MATCH("PARAMETER_NAME", Calc!$C:$C, 0))'
```

**Components**:
- `Calc!$E:$E`: Return range (column E, all rows)
- `Calc!$C:$C`: Lookup range (column C, all rows)
- `"PARAMETER_NAME"`: Value to search for
- `0`: Exact match

### 8.4 Named Ranges

#### Creating Named Ranges
```python
from openpyxl.workbook.defined_name import DefinedName

wb.defined_names['MTC'] = DefinedName('MTC', attr_text="'RORO_Stage_Scenarios'!$B$7")  # v3.9.2: updated from $C$8
```

**Syntax**: `'SheetName'!$CellReference` (sheet name must be in single quotes)

#### Using Named Ranges in Formulas
**Pattern**: Use name directly (no sheet reference needed)
```python
f'=IF(OR(ISERROR(MTC), ISERROR(TRIM5_CM), G{row_str}=""), "", ROUND(MTC * (ABS(TRIM5_CM) - ABS(G{row_str})), 2))'
```

### 8.5 Conditional Logic

#### IF Statement Pattern
```python
f'=IF(condition, true_value, false_value)'
```

**Example**:
```python
f'=IF($A{row_str}="","",$B{row_str})'
```

#### Nested IF Pattern
```python
f'=IF(condition1, IF(condition2, value1, value2), value3)'
```

#### AND/OR Logic
**AND Pattern**:
```python
f'=IF(AND(condition1, condition2, condition3), "OK", "CHECK")'
```

**OR Pattern**:
```python
f'=IF(OR(condition1, condition2), value1, value2)'
```

#### Error Handling
**ISERROR Pattern**:
```python
f'=IF(OR(ISERROR(MTC), ISERROR(TRIM5_CM), G{row_str}=""), "", formula)'
```

**ISBLANK Pattern**:
```python
f'=IF(OR(ISBLANK($C$12), ISBLANK($C$9), ISERROR($C$9)), "", formula)'
```

### 8.6 VLOOKUP Pattern

#### VLOOKUP for GM Lookup
**Pattern**: Lookup value from Hydro_Table based on mean draft
```python
f'=IF(O{row_str}="", "", VLOOKUP(AVERAGE(O{row_str},P{row_str}), Hydro_Table!$B:$D, 3, 1))'
```

**Components**:
- `AVERAGE(O{row_str},P{row_str})`: Lookup key (mean draft)
- `Hydro_Table!$B:$D`: Lookup range (Tmean_m to GM_m)
- `3`: Return column index (GM_m)
- `1`: Match type (approximate match, ascending order)

**Usage**: Used in RORO sheet column T (GM lookup) to find GM value based on mean draft.

### 8.7 Structural Strength Validation Formulas

#### Share Load Check
```python
f'=IF(AE{row_str}="", "", IF(AE{row_str}<=Calc!$E$24, "OK", "CHECK"))'
```

**Logic**: Validates share load against limit_share_load_t (Calc!E24 = 118.80 t)

#### Hinge Reaction Check
```python
f'=IF(AG{row_str}="", "", IF(AG{row_str}<=Calc!$E$23, "OK", "CHECK"))'
```

**Logic**: Validates hinge reaction against limit_reaction_t (Calc!E23 = 201.60 t)

#### Deck Pressure Calculation
```python
f'=IF(AE{row_str}="", "", AE{row_str}/Calc!$E$26)'
```

**Mathematical Formula**: `Deck_Press = Share_Load / linkspan_area`

#### Deck Pressure Check
```python
f'=IF(AI{row_str}="", "", IF(AI{row_str}<=Calc!$E$25, "OK", "CHECK"))'
```

**Logic**: Validates deck pressure against limit_deck_press_tpm2 (Calc!E25 = 10.00 t/m²)

### 8.8 Option 1 Ballast Fix Check Formulas

#### Required Trimming Moment Change
```python
f'=IF(OR(E{row_str}="", G{row_str}=""), "", Calc!$E$14 * (ABS(E{row_str}) - ABS(G{row_str})))'
```

**Mathematical Formula**: `ΔTM = MTC × (|Trim_cm| - |Trim_target_cm|)`

#### Required Ballast Weight
```python
f'=IF(AK{row_str}="", "", AK{row_str}/I{row_str})'
```

**Mathematical Formula**: `Ballast_req = ΔTM / Lever_arm`

#### Ballast Gap
```python
f'=IF(AL{row_str}="", "", AL{row_str} - IF(J{row_str}="", 0, J{row_str}))'
```

**Mathematical Formula**: `Ballast_gap = Ballast_req - Ballast_calc`

#### Additional Pumping Time
```python
f'=IF(AM{row_str}="", "", ABS(AM{row_str})/Calc!$E$12)'
```

**Mathematical Formula**: `Time_Add = |Ballast_gap| / PumpRate`

#### Fix Status Check
```python
f'=IF(AL{row_str}="", "", IF(AL{row_str}<=Calc!$E$27, IF(AN{row_str}<=Calc!$E$28, "OK", "NG (Time>6h)"), "NG (Cap>1200t)"))'
```

**Logic**:
- "OK" if ballast ≤ 1200t AND time ≤ 6h
- "NG (Cap>1200t)" if ballast > 1200t
- "NG (Time>6h)" if time > 6h

### 8.9 Formula Generation Examples

#### Simple Reference Formula
```python
ws.cell(row=row, column=1).value = f'=IF(December_Tide_2025!A{row_str}="","",December_Tide_2025!A{row_str})'
```

**Generated Excel Formula** (for row 2):
```excel
=IF(December_Tide_2025!A2="","",December_Tide_2025!A2)
```

#### Complex Calculation Formula
```python
ws.cell(row=row, column=3).value = (
    f'=IF($A{row_str}="","", '
    f'INDEX(Calc!$E:$E, MATCH("KminusZ_m", Calc!$C:$C, 0)) + $B{row_str} - '
    f'INDEX(Calc!$E:$E, MATCH("L_ramp_m", Calc!$C:$C, 0)) * '
    f'TAN(RADIANS(INDEX(Calc!$E:$E, MATCH("theta_max_deg", Calc!$C:$C, 0)))))'
)
```

#### Status Check Formula
```python
ws.cell(row=row, column=8).value = (
    f'=IF($E{row_str}="","", '
    f'IF(AND($E{row_str}>=INDEX(Calc!$E:$E, MATCH("min_fwd_draft_m", Calc!$C:$C, 0)), '
    f'$E{row_str}<=INDEX(Calc!$E:$E, MATCH("max_fwd_draft_m", Calc!$C:$C, 0)), '
    f'$G{row_str}<=INDEX(Calc!$E:$E, MATCH("theta_max_deg", Calc!$C:$C, 0))), "OK", "CHECK"))'
)
```

---

## Summary

This document covers:
1. **Helper Functions**: Style definitions and formula helper functions
2. **Calc Sheet**: Parameter reference sheet with multiple sections (includes Structural Limits, Ballast Fix Check, RAMP GEOMETRY, HINGE STRESS, PRECISION PARAMETERS)
3. **Tide Sheet**: JSON data loading and tide data storage (absolute path)
4. **Hourly Sheet**: 7,440+ formulas for hourly calculations
5. **RORO Sheet**: Stage scenarios with ballast calculations (49 columns, v3.9.2: updated from 48)
6. **RORO Sheet Extensions**: Captain Requirements (U-AD, v3.9.2: T(20) removed), Structural/Option 1 (AE-AO), and Ramp/Stress (AS-AW, v3.9.2: extended to AW) columns
7. **Additional Sheets**: Ballast_Tanks, Hydro_Table, Frame_to_x_Table, and CAPTAIN_REPORT sheets
8. **Excel Formula Generation**: Patterns and techniques for programmatic formula creation, including VLOOKUP and validation formulas

**Next:** [EXCEL_GEN_03_MATHEMATICS_AND_DATA_FLOW.md](EXCEL_GEN_03_MATHEMATICS_AND_DATA_FLOW.md) for mathematical formulas and data flow

---

**End of Functions and Implementation Document**

