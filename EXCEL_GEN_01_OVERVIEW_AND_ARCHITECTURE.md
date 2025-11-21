# Excel Generation Script - Overview and Architecture

**Version:** 4.0.0 (DAS Method v4.3 Final Optimized & CAPTAIN_REPORT v4.3)
**Date:** 2025-11-19
**Script:** `agi tr.py`
**Output:** `LCT_BUSHRA_AGI_TR_Final_v3.xlsx`

---

## Table of Contents

1. [Introduction](#1-introduction)
2. [Script Purpose](#2-script-purpose)
3. [System Architecture](#3-system-architecture)
4. [Dependencies and Requirements](#4-dependencies-and-requirements)
5. [File Structure](#5-file-structure)
6. [Output Specification](#6-output-specification)
7. [Main Orchestration Function](#7-main-orchestration-function)
8. [Documentation Index](#8-documentation-index)

---

## 1. Introduction

### 1.1 Overview

`agi tr.py` is a Python script that programmatically generates the `LCT_BUSHRA_AGI_TR_Final_v3.xlsx` Excel workbook from scratch. Unlike template-based approaches, this script creates all Excel formulas, styles, and data structures programmatically using the `openpyxl` library.

### 1.2 Key Features

- **Zero Template Dependency**: Creates Excel file entirely from code
- **Formula Generation**: Generates 7,440+ Excel formulas across multiple sheets
- **Data Integration**: Loads tide data from JSON files (absolute path)
- **Style Consistency**: Applies consistent formatting across all sheets
- **Error Handling**: Graceful degradation when data files are missing
- **Named Ranges**: Creates Excel named ranges for formula simplification
- **Structural Limits Validation**: Validates structural strength parameters (reaction, share load, deck pressure)
- **Option 1 Ballast Fix Check**: Validates ballast capacity and pumping time constraints
- **CAPTAIN_REPORT Sheet**: Summary sheet for Captain/Harbour Master with DAS Method operational limits and stage-by-stage safety checks (v4.3)
- **Reference Sheets**: Ballast_Tanks and Hydro_Table for operational reference

### 1.3 Use Case

This script is used to generate the LCT BUSHRA RORO Calculator Excel workbook, which performs:
- Hourly tide-based draft calculations
- Trim and stability analysis
- Ramp angle calculations
- Ballast requirement calculations
- Stage-by-stage loading scenario analysis
- Structural strength validation (hinge reaction, share load, deck pressure)
- Ballast fix check validation (capacity and time limits)
- Captain summary reporting (draft, trim, freeboard checks)

---

## 2. Script Purpose

### 2.1 Primary Objective

Generate a fully functional Excel workbook (`LCT_BUSHRA_AGI_TR.xlsx`) that:
1. Contains all necessary calculation sheets
2. Includes pre-loaded tide data for December 2025
3. Provides hourly draft and trim calculations
4. Supports RORO stage scenario analysis
5. Maintains formula integrity across all sheets

### 2.2 Design Philosophy

- **Reproducibility**: Same input always produces identical output
- **Maintainability**: Code-based generation allows version control
- **Flexibility**: Easy to modify formulas and structures
- **Accuracy**: Direct formula generation ensures correctness

---

## 3. System Architecture

### 3.1 High-Level Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    agi tr.py                             │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  ┌──────────────────────────────────────────────────┐  │
│  │  create_workbook_from_scratch()                  │  │
│  │  (Main Orchestration Function)                   │  │
│  └──────────────┬───────────────────────────────────┘  │
│                 │                                        │
│     ┌───────────┴───────────┐                           │
│     │                       │                           │
│  ┌──▼────────┐      ┌───────▼────────┐                 │
│  │ Helper    │      │ Sheet Creation │                 │
│  │ Functions │      │ Functions      │                 │
│  └───────────┘      └───────┬────────┘                 │
│                             │                           │
│        ┌────────────────────┼────────────────────┐     │
│        │                    │                    │     │
│  ┌─────▼─────┐    ┌─────────▼────────┐  ┌───────▼──┐ │
│  │ Calc      │    │ December_Tide    │  │ Hourly   │ │
│  │ Sheet     │    │ Sheet            │  │ Sheet    │ │
│  └───────────┘    └──────────────────┘  └──────────┘ │
│                                                         │
│  ┌──────────────────────────────────────────────────┐  │
│  │ RORO_Stage_Scenarios Sheet                      │  │
│  │  + extend_roro_captain_req()                    │  │
│  │  + extend_roro_structural_opt1()                │  │
│  └──────────────────────────────────────────────────┘  │
│                                                          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐ │
│  │ Ballast_Tanks│  │ Hydro_Table  │  │Frame_to_x_   │  │CAPTAIN_REPORT│ │
│  │ Sheet        │  │ Sheet        │  │Table Sheet   │  │ Sheet        │ │
│  └──────────────┘  └──────────────┘  └──────────────┘  └──────────────┘ │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

### 3.2 Component Breakdown

#### 3.2.1 Helper Functions
- `get_styles()`: Returns style definitions dictionary
- `create_index_match_formula()`: Generates INDEX/MATCH formulas
- `create_if_formula()`: Generates IF formulas
- `create_if_or_formula()`: Generates IF/OR formulas

#### 3.2.1a Frame Conversion Utilities (v3.2/v3.6)
- `_load_json(filename)`: Enhanced JSON loader with multiple path support (script dir, cwd, /mnt/data) (v3.6: added WARNING message when file not found)
- `_init_frame_mapping()`: Automatically initializes Frame-to-x conversion parameters from `Frame_x_from_mid_m.json` (v3.6: now called in `if __name__ == "__main__":` block, added INFO messages)
- `fr_to_x(fr)`: Converts Frame number to x-coordinate from midship (meters)
- `x_to_fr(x)`: Converts x-coordinate to Frame number (inverse of `fr_to_x()`)
- `debug_frame_mapping()`: Debug helper function to print current Frame mapping parameters and key Stage coordinates (v3.6: improved output formatting, added `sys.exit(0)`)
- `build_tank_lookup()`: Builds tank data lookup dictionary from `tank_coordinates.json` and `tank_data.json` with auto SG/air_vent assignment

#### 3.2.2 Sheet Creation Functions
- `create_calc_sheet()`: Creates parameter reference sheet (includes Structural Limits and Ballast Fix Check sections)
- `create_tide_sheet()`: Creates tide data sheet with JSON loading (absolute path)
- `create_hourly_sheet()`: Creates hourly calculation sheet (744 rows)
- `create_roro_sheet()`: Creates RORO stage scenarios sheet, returns `(stages, first_data_row)` tuple (v3.3.1)
- `create_ballast_tanks_sheet()`: Creates ballast tank reference sheet
- `create_hydro_table_sheet()`: Creates hydrostatic data table for GM lookup (v3.6: loads from `data/hydro_table.json` with 12 points, falls back to 4 hardcoded points)
- `create_frame_table_sheet()`: Creates Frame-to-x coordinate conversion table (from JSON)
- `create_captain_report_sheet(wb, stages, first_data_row)`: Creates Captain summary sheet (v3.3.1: accepts stages and first_data_row parameters)

#### 3.2.3 RORO Sheet Extension Functions
- `extend_roro_captain_req(ws, first_data_row, num_stages)`: Adds Captain Requirements columns (U-AD, 11 columns, start_col=21) (v3.9.2: T(20) removed, was T-AD) (v3.3.1: row range auto-bound to stages length)
- `extend_roro_structural_opt1(ws, first_data_row, num_stages)`: Adds Structural Strength (AE-AJ), Option 1 Ballast Fix Check (AK-AO), and Ramp/Stress (AS-AW) columns (v3.9.2: extended to AW, was AS-AV) (v3.3.1: row range auto-bound to stages length)

#### 3.2.4 Main Orchestration
- `create_workbook_from_scratch()`: Coordinates all sheet creation and extensions

### 3.3 Data Flow

```
JSON Files
    │
    ├─→ gateab_v3_tide_data.json
    │       ├─→ create_tide_sheet()
    │       │       └─→ December_Tide_2025 Sheet (744 rows)
    │       │
    │       └─→ create_hourly_sheet()
    │               └─→ References December_Tide_2025
    │               └─→ References Calc Sheet
    │               └─→ Hourly_FWD_AFT_Heights Sheet (744 rows)
    │                       │
    │                       └─→ 7,440+ formulas generated
    │
    ├─→ Frame_x_from_mid_m.json
    │       └─→ _init_frame_mapping() (v3.6: called in if __name__ == "__main__": block)
    │               └─→ Calculates _FRAME_SLOPE and _FRAME_OFFSET
    │               └─→ Used by fr_to_x() and x_to_fr() functions
    │
    ├─→ tank_coordinates.json + tank_data.json
    │       └─→ build_tank_lookup()
    │               └─→ create_ballast_tanks_sheet()
    │                       └─→ Ballast_Tanks Sheet (JSON-based with fallback)
    │
    └─→ data/hydro_table.json (v3.6)
            └─→ create_hydro_table_sheet()
                    └─→ Hydro_Table Sheet (12 points, falls back to 4 if JSON not found)

Calc Sheet (Parameters)
    │
    ├─→ create_hourly_sheet() (references)
    └─→ create_roro_sheet() (references)

RORO_Stage_Scenarios Sheet
    │
    ├─→ References Calc Sheet
    ├─→ References Hydro_Table (GM lookup)
    ├─→ Uses fr_to_x() for Stage 5/6/7 coordinates (Frame-based)
    ├─→ Creates Named Ranges
    ├─→ Excel Table structure (A19:AY29, 51 columns, 9 stages, header_row=19, freeze_panes=B20)
    ├─→ extend_roro_captain_req() adds columns U-AD (start_col=21, T(20) removed in v3.9.2)
    └─→ extend_roro_structural_opt1() adds columns AE-AY (extended to AY in v4.0.0, includes Opt C Tide columns)

Ballast_Tanks Sheet
    └─→ JSON-based lookup with fallback values (enhanced in v3.2)

Hydro_Table Sheet (v3.6: JSON-based with 12 points, fallback to 4)
    └─→ Used by RORO sheet for GM lookup via VLOOKUP

Frame_to_x_Table Sheet
    └─→ Reference data for Frame-to-x coordinate conversion (from JSON)

CAPTAIN_REPORT Sheet
    └─→ References RORO_Stage_Scenarios for stage summaries
```

---

## 4. Dependencies and Requirements

### 4.1 Python Dependencies

```python
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment, PatternFill, Border, Side, Protection
from openpyxl.utils import get_column_letter
from openpyxl.comments import Comment
import os
import sys
import json
from datetime import datetime
```

### 4.2 External Files

- **Input JSON Files**:
  - `C:\Users\minky\Downloads\src\data\gateab_v3_tide_data.json`
    - Format: JSON array with 744 entries
    - Structure: `[{"datetime": "2025-12-01 00:00:00", "tide_m": 2.06}, ...]`
    - Required: Always loaded (absolute path ensures data insertion)
    - Path: Fixed absolute path to ensure data is always available

  - `data/Frame_x_from_mid_m.json` (v3.2)
    - Format: JSON array with Frame-to-x coordinate mappings
    - Structure: `[{"Fr": 0.0, "x_from_mid_m": -30.15, "비고": "..."}, ...]`
    - Used by: `_init_frame_mapping()` for automatic slope/offset estimation
    - Path: Multiple path support (script dir, cwd, /mnt/data)
    - Optional: Falls back to default values if not found

  - `data/tank_coordinates.json` + `data/tank_data.json` (v3.2)
    - Format: JSON objects with `data` array containing tank information
    - Used by: `build_tank_lookup()` for Ballast_Tanks sheet generation
    - Path: Multiple path support (script dir, cwd, /mnt/data)
    - Optional: Falls back to hardcoded values if not found

  - `data/hydro_table.json` (v3.6)
    - Format: JSON array with 12 hydrostatic data points
    - Structure: `[{"Disp_t": ..., "Tmean_m": ..., "Trim_m": ..., "GM_m": ..., "Draft_FWD": ..., "Draft_AFT": ...}, ...]` or `[[...], ...]` (array format)
    - Used by: `create_hydro_table_sheet()` for Hydro_Table sheet generation
    - Path: Multiple path support (script dir, cwd, /mnt/data)
    - Optional: Falls back to 4 hardcoded points if not found

- **Output**: `LCT_BUSHRA_AGI_TR_Final_v3.xlsx` (saved in script directory)
  - Format: Excel 2010+ (.xlsx)
  - Size: ~112 KB
  - Sheets: 8 sheets

### 4.3 System Requirements

- Python 3.7+
- openpyxl library (Excel file manipulation)
- File system write access to `C:\Users\minky\Downloads\src\` directory
- UTF-8 encoding support (for JSON loading)

---

## 5. File Structure

### 5.1 Script Location

```
<project_directory>/
├── agi tr.py
├── data/
│   └── gateab_v3_tide_data.json
└── LCT_BUSHRA_AGI_TR_Final_v3.xlsx
```

### 5.2 Path Resolution

The script uses a combination of absolute and relative paths:

- **Output file**: Relative path `LCT_BUSHRA_AGI_TR_Final_v3.xlsx` (saved in script directory via `SCRIPT_DIR`)
- **Tide data JSON**: Multiple path support via `_load_json()` function
- **Frame mapping JSON** (v3.2): Multiple path support via `_load_json()`
  - Tries: Script directory → Current working directory → `/mnt/data`
  - Falls back to default values if not found
- **Tank data JSONs** (v3.2): Multiple path support via `_load_json()`
  - Tries: Script directory → Current working directory → `/mnt/data`
  - Falls back to hardcoded values if not found

Multiple path support ensures flexibility across different execution environments while maintaining backward compatibility.

---

## 6. Output Specification

### 6.1 Generated Excel Workbook

**File Name**: `LCT_BUSHRA_AGI_TR_Final_v3.xlsx`

**Sheets** (in order):
1. **Calc** - Parameter reference sheet (includes Structural Limits and Ballast Fix Check)
2. **December_Tide_2025** - Tide data (744 rows)
3. **Hourly_FWD_AFT_Heights** - Hourly calculations (744 rows, 7,440+ formulas)
4. **RORO_Stage_Scenarios** - Stage analysis (9 stages, 51 columns, Excel Table, header_row=19, freeze_panes=B20) (v4.0.0: updated from 49 columns, header_row=17)
5. **Ballast_Tanks** - Ballast tank reference data (8 tanks, JSON-based with fallback, enhanced in v3.2)
6. **Hydro_Table** - Hydrostatic data table (12 entries from JSON, or 4 if fallback, used for GM lookup) (v3.6: JSON-based)
7. **Frame_to_x_Table** - Frame number to x-coordinate conversion table (121 rows, from JSON)
8. **CAPTAIN_REPORT** - Captain summary sheet (DAS Method v4.3: operational limits and stage-by-stage safety checks)

### 6.2 Sheet Statistics

| Sheet | Rows | Columns | Formulas | Data Rows |
|-------|------|---------|----------|-----------|
| Calc | ~44 | 6 | 0 | Multiple parameters across sections (includes Structural Limits, Ballast Fix Check, RAMP GEOMETRY, HINGE STRESS, PRECISION PARAMETERS) |
| December_Tide_2025 | 745 | 2 | 0 | 744 tide entries |
| Hourly_FWD_AFT_Heights | 745 | 14 | ~7,440 | 744 calculation rows |
| RORO_Stage_Scenarios | ~27 | 48 | ~300 | 12 stage rows (includes Captain Req, Structural, Option 1, Ramp/Stress columns) |
| Ballast_Tanks | 9 | 6 | 0 | 8 tank entries (real measured data) |
| Hydro_Table | 13 (or 5 if fallback) | 6 | 0 | 12 hydrostatic entries from JSON (or 4 if fallback) (v3.6) |
| Frame_to_x_Table | 122 | 3 | 0 | 121 Frame-to-x coordinate entries |
| CAPTAIN_REPORT | ~22 | 9 | ~20 | 12 stage summaries |

### 6.3 Named Ranges

The script creates the following Excel named ranges:
- `MTC`: Moment to Change Trim (t·m/cm)
- `LCF`: Longitudinal Center of Flotation (m)
- `PumpRate`: Ballast pump rate (t/h)
- `X_Ballast`: Ballast position (m)
- `TRIM5_CM`: Stage 5 trim value (cm, v3.3: -89.58 cm)

### 6.4 Excel Tables

- **Stages Table**: Excel Table in RORO_Stage_Scenarios sheet
  - Range: A19:AY29 (header row 19, data rows 20-29, 9 stages, 51 columns)
  - Style: TableStyleMedium9
  - Features: Row striping, structured references
  - Columns: 51 total (A-S: original, T(20) removed, U-AD: Captain Req, AE-AJ: Structural, AK-AO: Option 1, AS-AW: Ramp/Stress, AX-AY: Opt C Tide)
  - Note: T(20) column is empty (Notes moved to G4-G15), freeze_panes at B20

---

## 7. Main Orchestration Function

### 7.1 Overview

The `create_workbook_from_scratch()` function is the main entry point that orchestrates the entire Excel file generation process. It coordinates all sheet creation functions and handles file I/O operations.

### 7.2 Function Signature

```python
def create_workbook_from_scratch():
    """워크북을 처음부터 생성"""
    # ... implementation
```

**Parameters**: None (uses module-level `OUTPUT_FILE` constant)
**Return Value**: None (creates file on disk)

### 7.3 Execution Flow

#### Step 1: Print Header
```python
print("=" * 80)
print("LCT_BUSHRA_AGI_TR.xlsx Creation from Scratch")
print("=" * 80)
```

#### Step 2: Create Output Directory
```python
output_dir = os.path.dirname(OUTPUT_FILE)
if output_dir and not os.path.exists(output_dir):
    os.makedirs(output_dir)
    print(f"[OK] Created output directory: {output_dir}")
```

#### Step 3: Handle File Conflicts
```python
final_output_file = OUTPUT_FILE
if os.path.exists(OUTPUT_FILE):
    try:
        with open(OUTPUT_FILE, 'r+b'):
            pass
    except PermissionError:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        base_name = os.path.splitext(OUTPUT_FILE)[0]
        final_output_file = f"{base_name}_{timestamp}.xlsx"
        print(f"[WARNING] Original file is open. Saving as: {final_output_file}")
```

**Logic**:
- Check if output file exists
- Try to open in read-write mode
- If PermissionError (file is open), create timestamped filename
- Use timestamp format: `YYYYMMDD_HHMMSS`

#### Step 4: Create Workbook
```python
print(f"\n[1/8] Creating new workbook")
wb = Workbook()
wb.remove(wb.active)  # 기본 시트 제거
```

#### Step 5: Create All Sheets
```python
    print(f"\n[2/8] Creating sheets:")
create_calc_sheet(wb)
create_tide_sheet(wb)
create_hourly_sheet(wb)
stages, first_data_row = create_roro_sheet(wb)  # Returns stages list and first data row
create_ballast_tanks_sheet(wb)
create_hydro_table_sheet(wb)
create_frame_table_sheet(wb)
```

**Execution Order**:
1. Calc sheet (parameters, includes Structural Limits and Ballast Fix Check)
2. Tide sheet (data, absolute path)
3. Hourly sheet (depends on Calc and Tide)
4. RORO sheet (depends on Calc)
5. Ballast_Tanks sheet (reference data)
6. Hydro_Table sheet (reference data for GM lookup)
7. Frame_to_x_Table sheet (reference data for Frame-to-x conversion)

**Note**: Order matters due to dependencies!

#### Step 5a: Extend RORO Sheet
```python
stages, first_data_row = create_roro_sheet(wb)  # Returns stages list and first data row
...
roro_ws = wb["RORO_Stage_Scenarios"]
extend_roro_captain_req(roro_ws, first_data_row, len(stages))  # Adds columns U-AD (v3.9.2: T(20) removed)
extend_roro_structural_opt1(roro_ws, first_data_row, len(stages))  # Adds columns AE-AW (Structural, Option 1, Ramp/Stress, v3.9.2: extended to AW)
```

#### Step 5b: Create CAPTAIN_REPORT Sheet
```python
create_captain_report_sheet(wb, stages, first_data_row)  # Depends on RORO sheet
```

#### Step 6: Save Workbook
```python
    print(f"\n[7/8] Saving workbook: {final_output_file}")
try:
    wb.save(final_output_file)
    print(f"  [OK] File saved successfully")
except Exception as e:
    print(f"  [ERROR] Failed to save: {e}")
    sys.exit(1)
```

#### Step 7: Close Workbook
```python
wb.close()
```

#### Step 8: Verify Output
```python
    print(f"\n[8/8] Verification:")
if os.path.exists(final_output_file):
    file_size = os.path.getsize(final_output_file) / 1024  # KB
    print(f"  [OK] File created: {final_output_file}")
    print(f"  [OK] File size: {file_size:.2f} KB")
    print(f"  [OK] Sheets: {len(wb.sheetnames)}")
else:
    print(f"  [ERROR] Output file was not created")
    sys.exit(1)
```

#### Step 9: Print Success Message
```python
print("\n" + "=" * 80)
print("[SUCCESS] Workbook creation from scratch complete!")
print("=" * 80)
```

### 7.4 Error Handling

#### File Permission Errors
**Scenario**: Output file is open in Excel
**Handling**: Detect PermissionError, generate timestamped filename, save to new filename, print warning message

#### Save Errors
**Scenario**: Disk full, write permission denied, etc.
**Handling**: Catch Exception during save, print error message, exit with code 1

#### Missing Output File
**Scenario**: File was not created (unexpected)
**Handling**: Check if file exists after save, print error if missing, exit with code 1

### 7.5 File Management

**Output File Path**: `OUTPUT_FILE = os.path.join(SCRIPT_DIR, "LCT_BUSHRA_AGI_TR_Final_v3.xlsx")`
**Resolution**: Relative path using script directory ensures consistent file location

**Directory Creation**: Creates output directory if it doesn't exist

**Timestamped Filenames**: Format `{base_name}_{YYYYMMDD}_{HHMMSS}.xlsx` when original file is locked/open

### 7.6 Complete Execution Sequence

```
1. Print header
   ↓
2. Create output directory (if needed)
   ↓
3. Check for file conflicts
   ↓
4. Create new workbook
   ↓
5. Remove default sheet
   ↓
6. Create Calc sheet
   ↓
7. Create December_Tide_2025 sheet
   ↓
8. Create Hourly_FWD_AFT_Heights sheet
   ↓
9. Create RORO_Stage_Scenarios sheet
   ↓
10. Create Ballast_Tanks sheet
   ↓
11. Create Hydro_Table sheet
   ↓
12. Create Frame_to_x_Table sheet
   ↓
13. Extend RORO sheet (Captain Req, Structural, Option 1, Ramp/Stress)
   ↓
14. Create CAPTAIN_REPORT sheet
   ↓
15. Save workbook
   ↓
16. Close workbook
   ↓
17. Verify output file
   ↓
18. Print success message
```

### 7.7 Main Entry Point

```python
if __name__ == "__main__":
    create_workbook_from_scratch()
```

**Usage**:
```bash
python "agi tr.py"
```

**Execution Location**: Should be run from `C:\Users\minky\Downloads\src\` directory (or adjust paths)

---

## 8. Documentation Index

This documentation is divided into multiple files for manageability:

1. **[EXCEL_GEN_01_OVERVIEW_AND_ARCHITECTURE.md](EXCEL_GEN_01_OVERVIEW_AND_ARCHITECTURE.md)** (This file)
   - System overview, architecture, and main orchestration

2. **[EXCEL_GEN_02_FUNCTIONS_AND_IMPLEMENTATION.md](EXCEL_GEN_02_FUNCTIONS_AND_IMPLEMENTATION.md)**
   - Helper functions, all sheet creation functions, and Excel formula generation

3. **[EXCEL_GEN_03_MATHEMATICS_AND_DATA_FLOW.md](EXCEL_GEN_03_MATHEMATICS_AND_DATA_FLOW.md)**
   - Mathematical formulas, derivations, and data flow

4. **[EXCEL_GEN_04_ALGORITHM_LOGIC_ARCHITECTURE.md](EXCEL_GEN_04_ALGORITHM_LOGIC_ARCHITECTURE.md)**
   - Program algorithms, logic flow, system architecture diagrams, and design patterns

---

## Summary

The main orchestration function:
- **Coordinates** all sheet creation
- **Manages** file I/O operations
- **Handles** errors gracefully
- **Verifies** output file
- **Provides** user feedback

**Next:**
- [EXCEL_GEN_02_FUNCTIONS_AND_IMPLEMENTATION.md](EXCEL_GEN_02_FUNCTIONS_AND_IMPLEMENTATION.md) for detailed function documentation
- [EXCEL_GEN_04_ALGORITHM_LOGIC_ARCHITECTURE.md](EXCEL_GEN_04_ALGORITHM_LOGIC_ARCHITECTURE.md) for algorithm analysis and architecture diagrams

---

**End of Overview and Architecture Document**

