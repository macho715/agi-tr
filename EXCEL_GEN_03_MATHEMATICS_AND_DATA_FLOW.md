# Excel Generation Script - Mathematics and Data Flow

**Version:** 4.0.0 (DAS Method v4.3 Final Optimized & CAPTAIN_REPORT v4.3)
**Date:** 2025-11-19
**Related:** [EXCEL_GEN_01_OVERVIEW_AND_ARCHITECTURE.md](EXCEL_GEN_01_OVERVIEW_AND_ARCHITECTURE.md)

---

## Table of Contents

1. [Mathematical Formulas](#1-mathematical-formulas)
2. [Coordinate System](#2-coordinate-system)
3. [Trim Calculations](#3-trim-calculations)
4. [Draft Calculations](#4-draft-calculations)
5. [Ramp Angle Calculations](#5-ramp-angle-calculations)
6. [Ballast Calculations](#6-ballast-calculations)
7. [Height Calculations](#7-height-calculations)
8. [Status Validation](#8-status-validation)
9. [Data Flow and Dependencies](#9-data-flow-and-dependencies)

---

## 1. Mathematical Formulas

This document provides detailed mathematical derivations and explanations for all formulas used in the Excel workbook. All formulas are based on naval architecture principles and vessel stability calculations.

---

## 2. Coordinate System

### 2.1 Origin Definition

**Midship = 0 m**

The coordinate system uses the vessel's midship (midpoint between forward and aft perpendiculars) as the origin.

```
        FWD ←-------- 0 (midship) --------→ AFT
Position:   -40m    -20m     0      +20m    +40m
x_stage:  Negative         0            Positive
```

### 2.2 Sign Convention

- **Negative x**: Forward of midship (bow direction)
- **Positive x**: Aft of midship (stern direction)
- **Negative Trim**: Bow down (vessel tilts forward)
- **Positive Trim**: Stern down (vessel tilts aft)

### 2.3 LCF Reference

**Critical**: LCF (Longitudinal Center of Flotation) must be expressed **from midship**, not from Forward Perpendicular (FP) or Aft Perpendicular (AP).

**Conversion Formula**:
```
LCF_from_midship = LCF_from_FP - (LPP / 2)
```

**Example**:
- LPP = 60.302 m
- LCF from FP = 45.856 m (from Stability Booklet)
- LCF from midship = 45.856 - (60.302 / 2) = 45.856 - 30.151 = **+15.705 m**

**Warning**: Using LCF from FP directly causes significant trim calculation errors!

### 2.4 Frame-Based Coordinate System (v3.2)

**Frame Number to x-Coordinate Conversion**:

The script uses a Frame-based coordinate system for consistency across Stage 5/6/7 definitions. Frame numbers are converted to x-coordinates using a linear transformation.

**Conversion Formula**:
```
x = _FRAME_OFFSET + _FRAME_SLOPE * Fr
```

**Where**:
- `x`: x-coordinate from midship (meters)
- `Fr`: Frame number
- `_FRAME_OFFSET`: Offset parameter (default: -30.15 m)
- `_FRAME_SLOPE`: Slope parameter (default: 1.0)

**Automatic Initialization** (v3.2):

The `_init_frame_mapping()` function automatically calculates `_FRAME_SLOPE` and `_FRAME_OFFSET` from `data/Frame_x_from_mid_m.json`:

1. Loads JSON file using `_load_json()`
2. Extracts first two entries: `(Fr1, x1)` and `(Fr2, x2)`
3. Calculates slope: `_FRAME_SLOPE = (x2 - x1) / (Fr2 - Fr1)`
4. Calculates offset: `_FRAME_OFFSET = x1 - _FRAME_SLOPE * Fr1`
5. Falls back to default values if JSON not found

**Inverse Conversion**:
```
Fr = (x - _FRAME_OFFSET) / _FRAME_SLOPE
```

**Stage 5/7 Frame-Based Coordinates** (v3.2/v3.3):

- **Stage 5**: `x = fr_to_x(52.5) ≈ 22.35 m` (Ballast only at FWB1+FWB2 combined LCG) - **v3.3**: Trim target = -89.58 cm
- **Stage 7**: `x = fr_to_x(30.15) ≈ 0.00 m` (Cargo off, symmetric ballast around midship) - **v3.3**: Trim target = 0.0 cm (Even keel)

**Implementation**: Lines 77-109 in `agi tr.py`

---

## 3. Trim Calculations

### 3.1 Trimming Moment (TM)

**Formula**:
```
TM = W × (x - LCF)
```

**Where**:
- `TM`: Trimming moment (t·m)
- `W`: Weight acting on vessel (tons)
- `x`: Longitudinal position of weight from midship (m)
- `LCF`: Longitudinal Center of Flotation from midship (m)

**Physical Meaning**: The moment created by a weight at position `x` relative to the trimming axis (LCF).

**Sign Convention**:
- Positive TM: Creates stern-down trim
- Negative TM: Creates bow-down trim

**Example**:
- W = 434 t
- x = 15.27 m (aft of midship)
- LCF = 30.91 m (aft of midship)
- TM = 434 × (15.27 - 30.91) = 434 × (-15.64) = **-6,787.76 t·m** (bow-down moment)

### 3.2 Trim in Centimeters

**Formula**:
```
Trim_cm = TM / MTC
```

**Where**:
- `Trim_cm`: Trim in centimeters
- `TM`: Trimming moment (t·m)
- `MTC`: Moment to Change Trim 1 cm (t·m/cm)

**Physical Meaning**: The amount of trim (in cm) caused by the trimming moment.

**Example**:
- TM = -6,787.76 t·m
- MTC = 33.99 t·m/cm
- Trim_cm = -6,787.76 / 33.99 = **-199.64 cm** (bow down)

### 3.3 Trim in Meters

**Formula**:
```
Trim_m = Trim_cm / 100
```

**Example**:
- Trim_cm = -199.64 cm
- Trim_m = -199.64 / 100 = **-1.9964 m** (bow down)

---

## 4. Draft Calculations

### 4.1 Mean Draft

**Formula**:
```
Tmean = (Dfwd + Daft) / 2
```

**Where**:
- `Tmean`: Mean draft (average of forward and aft drafts)
- `Dfwd`: Forward draft (m)
- `Daft`: Aft draft (m)

### 4.2 Forward Draft from Mean and Trim

**Formula**:
```
Dfwd = Tmean - Trim_m / 2
Daft = Tmean + Trim_m / 2
```

**Derivation**:
- Trim causes draft difference: `ΔD = Trim_m`
- Forward draft decreases by half: `Dfwd = Tmean - Trim_m/2`
- Aft draft increases by half: `Daft = Tmean + Trim_m/2`

**Example**:
- Tmean = 2.33 m
- Trim_m = -1.9964 m (bow down)
- Dfwd = 2.33 - (-1.9964)/2 = 2.33 + 0.9982 = **3.328 m**
- Daft = 2.33 + (-1.9964)/2 = 2.33 - 0.9982 = **1.332 m**

### 4.3 Required Forward Draft (Even Keel)

**Formula** (Hourly sheet):
```
Dfwd_req = KminusZ + Tide - L_ramp × tan(θ_max)
```

**Derivation**:
1. Maximum ramp angle constraint: `θ ≤ θ_max`
2. Ramp angle geometry: `tan(θ) = (KminusZ - Dfwd + Tide) / L_ramp`
3. At maximum angle: `tan(θ_max) = (KminusZ - Dfwd_req + Tide) / L_ramp`
4. Solving for Dfwd_req:
   ```
   L_ramp × tan(θ_max) = KminusZ - Dfwd_req + Tide
   Dfwd_req = KminusZ + Tide - L_ramp × tan(θ_max)
   ```

**Where**:
- `KminusZ`: Vertical distance from keel to reference point (m)
- `Tide`: Current tide height (m)
- `L_ramp`: Linkspan length (m)
- `θ_max`: Maximum ramp angle (degrees, converted to radians)

**Example**:
- KminusZ = 3.0 m
- Tide = 2.06 m
- L_ramp = 12.0 m
- θ_max = 6° = 0.1047 radians
- Dfwd_req = 3.0 + 2.06 - 12.0 × tan(6°) = 5.06 - 12.0 × 0.1051 = 5.06 - 1.261 = **3.799 m**

---

## 5. Ramp Angle Calculations

### 5.1 Ramp Angle from Geometry

**Formula**:
```
θ = arctan((KminusZ - Dfwd + Tide) / L_ramp)
```

**Derivation**:
1. Vertical difference: `ΔH = KminusZ - Dfwd + Tide`
2. Horizontal distance: `L_ramp`
3. Angle: `θ = arctan(ΔH / L_ramp)`

**Where**:
- `θ`: Ramp angle (radians, converted to degrees in Excel)
- `KminusZ`: Vertical distance from keel (m)
- `Dfwd`: Forward draft (m)
- `Tide`: Current tide height (m)
- `L_ramp`: Linkspan length (m)

**Physical Meaning**: The angle of the ramp connecting the vessel to the shore, based on current vessel draft and tide level.

**Example**:
- KminusZ = 3.0 m
- Dfwd = 3.328 m
- Tide = 2.06 m
- L_ramp = 12.0 m
- ΔH = 3.0 - 3.328 + 2.06 = 1.732 m
- θ = arctan(1.732 / 12.0) = arctan(0.1443) = **8.22°**

**Excel Formula**:
```excel
=DEGREES(ATAN((KminusZ - Dfwd + Tide) / L_ramp))
```

### 5.2 Ramp Angle from Physical Freeboard (RORO Sheet)

**Formula** (RORO sheet column AP):
```
θ = arcsin((Phys_Freeboard - ramp_end_clearance_min) / ramp_length)
```

**Where**:
- `θ`: Ramp angle (degrees)
- `Phys_Freeboard`: Physical freeboard (D_vessel - Dfwd) (m)
- `ramp_end_clearance_min`: Minimum ramp end clearance (0.40 m)
- `ramp_length`: Ramp length (8.30 m)

**Physical Meaning**: The ramp angle calculated from physical freeboard (without tide), accounting for minimum clearance requirement.

**Example**:
- D_vessel = 3.65 m
- Dfwd = 3.328 m
- Phys_Freeboard = 3.65 - 3.328 = 0.322 m
- ramp_end_clearance_min = 0.40 m
- ramp_length = 8.30 m
- θ = arcsin((0.322 - 0.40) / 8.30) = arcsin(-0.0094) = **-0.54°**

**Excel Formula** (RORO sheet column AS):
```excel
=DEGREES(ASIN((Y{row}-Calc!$E$35)/Calc!$E$33))
```

**Validation** (RORO sheet column AT):
- Limit: 10° maximum ramp angle
- Formula: `=IF(AS{row}<=10, "OK", "NG")`

### 5.3 Pin Stress Calculation (RORO Sheet)

**Formula** (RORO sheet column AU):
```
Pin_Stress = (Hinge_Rx / 4) / hinge_pin_area × 9.81 / 1000
```

**Where**:
- `Pin_Stress`: Pin stress (N/mm²)
- `Hinge_Rx`: Hinge reaction force (tons, from column AG)
- `4`: Number of pins
- `hinge_pin_area`: Pin area (0.117 m²)
- `9.81`: Gravitational acceleration (m/s²)
- `1000`: Conversion factor (N to kN, m² to mm²)

**Physical Meaning**: The stress on each pin (assuming 4 pins share the load equally) based on the hinge reaction force.

**Example**:
- Hinge_Rx = 201.60 t
- hinge_pin_area = 0.117 m²
- Pin_Stress = (201.60 / 4) / 0.117 × 9.81 / 1000 = 50.4 / 0.117 × 9.81 / 1000 = **4.23 N/mm²**

**Excel Formula** (RORO sheet column AU):
```excel
=(AG{row}/4)/Calc!$E$36*9.81/1000
```

**Validation** (RORO sheet column AV - Von Mises Check):
- Limit: 188 N/mm² maximum stress
- Formula: `=IF(AU{row}<=188, "OK", "NG")`

---

## 6. Ballast Calculations

### 6.1 Lever-Arm Method

#### 6.1.1 Trimming Moment Change

**Formula**:
```
ΔTM = MTC × (|TRIM5_CM| - |Trim_target_cm|)
```

**Where**:
- `ΔTM`: Required trimming moment change (t·m)
- `MTC`: Moment to Change Trim 1 cm (t·m/cm)
- `TRIM5_CM`: Stage 5 trim value (cm) - reference point
- `Trim_target_cm`: Target trim for current stage (cm)

**Physical Meaning**: The trimming moment change needed to adjust from Stage 5 trim to target trim.

**Example** (v3.3 updated values):
- MTC = 33.99 t·m/cm
- TRIM5_CM = -89.58 cm (updated from -163.68 cm in v3.3)
- Trim_target_cm = -96.5 cm (for Stage 6A/6B/6C)
- ΔTM = 33.99 × (|-89.58| - |-96.5|) = 33.99 × (89.58 - 96.5) = 33.99 × (-6.92) = **-235.2 t·m**

**Example** (Stage 7, v3.3):
- MTC = 33.99 t·m/cm
- Trim_cm = -89.58 cm (Stage 5 trim)
- Trim_target_cm = 0.0 cm (Even keel, updated from -96.5 cm in v3.3)
- ΔTM = 33.99 × (|-89.58| - |0.0|) = 33.99 × (89.58 - 0.0) = 33.99 × 89.58 = **3,044.8 t·m**

#### 6.1.2 Lever Arm

**Formula**:
```
Lever_arm = X_Ballast - LCF
```

**Where**:
- `Lever_arm`: Distance from LCF to ballast position (m)
- `X_Ballast`: Longitudinal position of ballast from midship (m)
- `LCF`: Longitudinal Center of Flotation from midship (m)

**Physical Meaning**: The distance over which ballast weight acts to create trimming moment.

**Example**:
- X_Ballast = 52.53 m (aft of midship)
- LCF = 30.91 m (aft of midship)
- Lever_arm = 52.53 - 30.91 = **21.62 m**

#### 6.1.3 Required Ballast Weight

**Formula**:
```
Ballast_t = ΔTM / Lever_arm
```

**Where**:
- `Ballast_t`: Required ballast weight (tons)
- `ΔTM`: Trimming moment change (t·m)
- `Lever_arm`: Lever arm distance (m)

**Physical Meaning**: The weight of ballast needed at the specified position to achieve the required trimming moment change.

**Example**:
- ΔTM = 2,283.4 t·m
- Lever_arm = 21.62 m
- Ballast_t = 2,283.4 / 21.62 = **105.6 t**

#### 6.1.4 Ballast Pumping Time

**Formula**:
```
Ballast_time = Ballast_t / PumpRate
```

**Where**:
- `Ballast_time`: Time to pump ballast (hours)
- `Ballast_t`: Required ballast weight (tons)
- `PumpRate`: Ballast pump rate (t/h)

**Example**:
- Ballast_t = 105.6 t
- PumpRate = 5.0 t/h
- Ballast_time = 105.6 / 5.0 = **21.1 hours**

### 6.2 Rule-of-Thumb Method

**Formula**:
```
Ballast_t = |Trim_m| × 50 × TPC
```

**Where**:
- `Ballast_t`: Estimated ballast weight (tons)
- `Trim_m`: Trim in meters (absolute value)
- `50`: Empirical factor (assumes ballast at Lpp/2 from LCF)
- `TPC`: Tons Per Centimeter (t/cm)

**Physical Meaning**: Simplified ballast estimation based on trim magnitude and TPC.

**Example**:
- Trim_m = -1.9964 m
- TPC = 7.95 t/cm
- Ballast_t = 1.9964 × 50 × 7.95 = **793.4 t**

**Note**: This method is less accurate than lever-arm method but provides quick estimation.

---

## 7. Height Calculations

### 7.1 Height Above Water (Freeboard)

**Formula**:
```
Height = D_vessel - Draft + Tide
```

**Where**:
- `Height`: Height above water (freeboard) (m)
- `D_vessel`: Molded depth (vessel height from keel) (m)
- `Draft`: Actual draft at location (m)
- `Tide`: Current tide height (m)

**Physical Meaning**: The vertical distance from the deck to the water surface, accounting for tide.

**Example - Forward Height**:
- D_vessel = 3.65 m
- Dfwd = 3.328 m
- Tide = 2.06 m
- FWD_Height = 3.65 - 3.328 + 2.06 = **2.382 m**

**Example - Aft Height**:
- D_vessel = 3.65 m
- Daft = 1.332 m
- Tide = 2.06 m
- AFT_Height = 3.65 - 1.332 + 2.06 = **4.378 m**

### 7.2 Physical Freeboard (No Tide)

**Formula**:
```
Phys_Freeboard = D_vessel - Dfwd
```

**Where**:
- `Phys_Freeboard`: Physical freeboard without tide (m)
- `D_vessel`: Molded depth (vessel height from keel) (m)
- `Dfwd`: Forward draft (m)

**Physical Meaning**: The vertical distance from the deck to the water surface at the forward location, without accounting for tide. Used for linkspan clearance checks.

**Example**:
- D_vessel = 3.65 m
- Dfwd = 3.328 m
- Phys_Freeboard = 3.65 - 3.328 = **0.322 m**

**Usage**: Used in RORO sheet column Y and validated against linkspan freeboard limit (0.28 m) in column Z.

### 7.3 Propeller Immersion Percentage

**Formula**:
```
Prop_Imm = ((Daft - D_prop_ref) / Imm_range) × 100
```

**Where**:
- `Prop_Imm`: Propeller immersion percentage (%)
- `Daft`: Aft draft (m)
- `D_prop_ref`: Propeller reference depth (2.10 m)
- `Imm_range`: Immersion range (1.25 m)

**Physical Meaning**: Percentage of propeller immersion relative to reference depth and range.

**Example**:
- Daft = 3.328 m
- D_prop_ref = 2.10 m
- Imm_range = 1.25 m
- Prop_Imm = ((3.328 - 2.10) / 1.25) × 100 = (1.228 / 1.25) × 100 = **98.24%**

**Usage**: Used in RORO sheet column AC to monitor propeller immersion.

### 7.4 GM Lookup from Hydrostatic Table

**Formula**:
```
GM = VLOOKUP(Tmean, Hydro_Table!$B:$D, 3, 1)
```

**Where**:
- `GM`: Metacentric height (m)
- `Tmean`: Mean draft (average of forward and aft draft) (m)
- `Hydro_Table!$B:$D`: Lookup range (Tmean_m to GM_m)
- `3`: Return column index (GM_m)
- `1`: Match type (approximate match, ascending order)

**Lookup Key Calculation**:
```
Tmean = (Dfwd + Daft) / 2
```

**Physical Meaning**: Looks up GM value from hydrostatic table based on mean draft. Uses approximate match (match type 1) which requires data sorted by Tmean_m in ascending order.

**Example**:
- Dfwd = 3.328 m
- Daft = 1.332 m
- Tmean = (3.328 + 1.332) / 2 = 2.33 m
- VLOOKUP finds closest Tmean_m ≤ 2.33 m in Hydro_Table
- Returns corresponding GM_m value

**Usage**: Used in RORO sheet column T to determine GM for each stage based on mean draft.

---

## 8. Status Validation

### 8.1 Draft Limits Check

**Condition**:
```
min_fwd_draft ≤ Dfwd ≤ max_fwd_draft
```

**Where**:
- `min_fwd_draft`: Minimum allowable forward draft (m)
- `max_fwd_draft`: Maximum allowable forward draft (m)
- `Dfwd`: Actual forward draft (m)

**Example**:
- min_fwd_draft = 1.5 m
- max_fwd_draft = 3.5 m
- Dfwd = 3.328 m
- Check: 1.5 ≤ 3.328 ≤ 3.5 → **TRUE** (within limits)

### 8.2 Ramp Angle Limit Check

**Condition**:
```
Ramp_Angle ≤ θ_max
```

**Where**:
- `Ramp_Angle`: Calculated ramp angle (degrees)
- `θ_max`: Maximum allowable ramp angle (degrees)

**Example**:
- Ramp_Angle = 8.22°
- θ_max = 6.0°
- Check: 8.22 ≤ 6.0 → **FALSE** (exceeds limit)

### 8.3 Trim Limit Check (Lpp/50 Rule)

**Condition**:
```
|Trim_m| ≤ Lpp / 50
```

**Where**:
- `Trim_m`: Trim in meters (absolute value)
- `Lpp`: Length Between Perpendiculars (m)

**Physical Meaning**: Rule of thumb that trim should not exceed 1/50th of vessel length.

**Example**:
- Trim_m = -1.9964 m
- Lpp = 60.302 m
- Limit = 60.302 / 50 = 1.206 m
- Check: 1.9964 ≤ 1.206 → **FALSE** (exceeds limit)

### 8.4 Combined Status Check

**Excel Formula**:
```excel
=IF(AND(
    Dfwd >= min_fwd_draft,
    Dfwd <= max_fwd_draft,
    Ramp_Angle <= θ_max
), "OK", "CHECK")
```

**Logic**:
- If all conditions met → "OK"
- If any condition fails → "CHECK"

### 8.5 Draft Limit Check (Summer Draft)

**Condition**:
```
Max_draft ≤ 2.70 m
```

**Where**:
- `Max_draft`: Maximum of forward and aft draft (m)
- `2.70 m`: Summer draft limit

**Excel Formula**:
```excel
=IF(Max_draft <= 2.70, "OK", ">2.70m")
```

**Physical Meaning**: Validates that maximum draft does not exceed summer draft limit.

**Example**:
- Dfwd = 3.328 m
- Daft = 1.332 m
- Max_draft = MAX(3.328, 1.332) = 3.328 m
- Check: 3.328 ≤ 2.70 → **FALSE** (exceeds limit)

**Usage**: Used in CAPTAIN_REPORT sheet column F (Draft_OK).

### 8.6 Freeboard Limit Check

**Condition**:
```
Phys_Freeboard ≥ 0.28 m
```

**Where**:
- `Phys_Freeboard`: Physical freeboard (D_vessel - Dfwd) (m)
- `0.28 m`: Linkspan freeboard limit

**Excel Formula**:
```excel
=IF(Phys_Freeboard >= 0.28, "OK", "<0.28m")
```

**Physical Meaning**: Validates that physical freeboard meets minimum linkspan clearance requirement.

**Example**:
- D_vessel = 3.65 m
- Dfwd = 3.328 m
- Phys_Freeboard = 3.65 - 3.328 = 0.322 m
- Check: 0.322 ≥ 0.28 → **TRUE** (meets limit)

**Usage**: Used in RORO sheet column Z (Clearance_Check) and CAPTAIN_REPORT sheet column H (Freeboard_OK).

### 8.7 GM Limit Check

**Condition**:
```
GM ≥ 1.50 m
```

**Where**:
- `GM`: Metacentric height (m)
- `1.50 m`: GM target/limit

**Excel Formula**:
```excel
=IF(GM >= 1.50, "OK", "NG")
```

**Physical Meaning**: Validates that vessel has sufficient metacentric height for stability.

**Example**:
- GM = 1.88 m (from Hydro_Table lookup)
- Check: 1.88 ≥ 1.50 → **TRUE** (meets limit)

**Usage**: Used in RORO sheet column AB (GM_Check).

### 8.8 Structural Strength Validation

#### 8.8.1 Share Load Check

**Condition**:
```
Share_Load ≤ 118.80 t
```

**Where**:
- `Share_Load`: Share load on LCT (tons)
- `118.80 t`: Maximum share load limit (Mammoet)

**Excel Formula**:
```excel
=IF(Share_Load <= 118.80, "OK", "CHECK")
```

**Usage**: Used in RORO sheet column AF (Share_Check).

#### 8.8.2 Hinge Reaction Check

**Note**: Hinge_Rx is now auto-calculated: `Hinge_Rx = 45 + Share_Load × 0.545`

**Calculation Formula**:
```
Hinge_Rx = 45 + Share_Load × 0.545
```

**Where**:
- `Hinge_Rx`: Auto-calculated hinge reaction force (tons)
- `45`: Ramp self-weight (tons)
- `Share_Load`: Share load on LCT (tons, user input)
- `0.545`: Share ratio (54.5%)

**Physical Meaning**: The hinge reaction is automatically calculated as the sum of the ramp's self-weight (45t) and 54.5% of the share load.

**Validation Condition**:
```
Hinge_Rx ≤ 201.60 t
```

**Where**:
- `Hinge_Rx`: Auto-calculated hinge reaction force (tons)
- `201.60 t`: Maximum hinge reaction limit (Aries)

**Excel Formula**:
```excel
=IF(AG{row}="", "", IF(AG{row}<=Calc!$E$23, "OK", "NG"))
```

**Output Values**: "OK" if ≤ 201.60t, "NG" if > 201.60t

**Usage**: Used in RORO sheet column AH (Rx_Check). Column AG (Hinge_Rx_t) is auto-calculated, not user input.

#### 8.8.3 Deck Pressure Calculation

**Formula**:
```
Deck_Press = Share_Load / linkspan_area
```

**Where**:
- `Deck_Press`: Deck pressure (t/m²)
- `Share_Load`: Share load on LCT (tons)
- `linkspan_area`: Linkspan contact area (12.00 m²)

**Example**:
- Share_Load = 118.80 t
- linkspan_area = 12.00 m²
- Deck_Press = 118.80 / 12.00 = **9.90 t/m²**

**Usage**: Used in RORO sheet column AI (Deck_Press_t/m²).

#### 8.8.4 Deck Pressure Check

**Condition**:
```
Deck_Press ≤ 10.00 t/m²
```

**Where**:
- `Deck_Press`: Calculated deck pressure (t/m²)
- `10.00 t/m²`: Maximum deck pressure limit (Spec)

**Excel Formula**:
```excel
=IF(Deck_Press <= 10.00, "OK", "CHECK")
```

**Usage**: Used in RORO sheet column AJ (Press_Check).

### 8.9 Option 1 Ballast Fix Check

#### 8.9.1 Required Trimming Moment Change (Option 1)

**Formula**:
```
ΔTM_needed = MTC × (|Trim_cm| - |Trim_target_cm|)
```

**Where**:
- `ΔTM_needed`: Required trimming moment change (t·m)
- `MTC`: Moment to Change Trim (t·m/cm)
- `Trim_cm`: Current trim (cm)
- `Trim_target_cm`: Target trim (cm)

**Physical Meaning**: The trimming moment change needed to adjust from current trim to target trim.

**Example** (v3.3 updated values):
- MTC = 33.99 t·m/cm
- Trim_cm = -89.58 cm (Stage 5 trim, updated from -163.68 cm in v3.3)
- Trim_target_cm = -96.5 cm (for Stage 6A/6B/6C)
- ΔTM_needed = 33.99 × (|-89.58| - |-96.5|) = 33.99 × (89.58 - 96.5) = 33.99 × (-6.92) = **-235.2 t·m**

**Example** (Stage 7, v3.3):
- MTC = 33.99 t·m/cm
- Trim_cm = -89.58 cm (Stage 5 trim)
- Trim_target_cm = 0.0 cm (Even keel, updated from -96.5 cm in v3.3)
- ΔTM_needed = 33.99 × (|-89.58| - |0.0|) = 33.99 × (89.58 - 0.0) = 33.99 × 89.58 = **3,044.8 t·m**

**Usage**: Used in RORO sheet column AK (ΔTM_needed_cm·tm).

#### 8.9.2 Required Ballast Weight (Option 1)

**Formula**:
```
Ballast_req = ΔTM_needed / Lever_arm
```

**Where**:
- `Ballast_req`: Required ballast weight (tons)
- `ΔTM_needed`: Required trimming moment change (t·m)
- `Lever_arm`: Lever arm distance (m)

**Example**:
- ΔTM_needed = 2,283.4 t·m
- Lever_arm = 21.62 m
- Ballast_req = 2,283.4 / 21.62 = **105.6 t**

**Usage**: Used in RORO sheet column AL (Ballast_req_t).

#### 8.9.3 Ballast Gap

**Formula**:
```
Ballast_gap = Ballast_req - Ballast_calc
```

**Where**:
- `Ballast_gap`: Gap between required and calculated ballast (tons)
- `Ballast_req`: Required ballast weight (Option 1 method) (tons)
- `Ballast_calc`: Calculated ballast weight (lever-arm method from column J) (tons)

**Physical Meaning**: The difference between Option 1 required ballast and the calculated ballast. Positive gap means additional ballast needed.

**Example**:
- Ballast_req = 105.6 t
- Ballast_calc = 100.0 t
- Ballast_gap = 105.6 - 100.0 = **5.6 t**

**Usage**: Used in RORO sheet column AM (Ballast_gap_t).

#### 8.9.4 Additional Pumping Time

**Formula**:
```
Time_Add = |Ballast_gap| / PumpRate
```

**Where**:
- `Time_Add`: Additional pumping time needed (hours)
- `Ballast_gap`: Ballast gap (tons)
- `PumpRate`: Ballast pump rate (10.0 t/h)

**Example**:
- Ballast_gap = 5.6 t
- PumpRate = 10.0 t/h
- Time_Add = |5.6| / 10.0 = **0.56 hours**

**Usage**: Used in RORO sheet column AN (Time_Add_h).

#### 8.9.5 Fix Status Check

**Conditions**:
```
Ballast_req ≤ 1200.00 t AND Time_Add ≤ 6.00 h
```

**Where**:
- `Ballast_req`: Required ballast weight (tons)
- `1200.00 t`: Maximum AFT ballast capacity
- `Time_Add`: Additional pumping time (hours)
- `6.00 h`: Maximum allowed pump time for fix

**Excel Formula**:
```excel
=IF(Ballast_req <= 1200.00,
    IF(Time_Add <= 6.00, "OK", "NG (Time>6h)"),
    "NG (Cap>1200t)")
```

**Output Values**:
- "OK": Both conditions met (ballast ≤ 1200t AND time ≤ 6h)
- "NG (Cap>1200t)": Ballast exceeds capacity limit
- "NG (Time>6h)": Time exceeds limit (but ballast is within capacity)

**Usage**: Used in RORO sheet column AO (Fix_Status).

---

## 9. Data Flow and Dependencies

### 9.1 Data Sources

#### External Data
**JSON Files**:

1. **Tide Data**: `C:\Users\minky\Downloads\src\data\gateab_v3_tide_data.json`
   - Format: JSON array
   - Records: 744 entries
   - Fields: `datetime`, `tide_m`
   - Loaded By: `create_tide_sheet()`
   - Destination: December_Tide_2025 sheet
   - Path: Absolute path ensures data is always loaded

2. **Frame Mapping** (v3.2/v3.6): `data/Frame_x_from_mid_m.json`
   - Format: JSON array
   - Fields: `Fr`, `x_from_mid_m`, `비고`
   - Loaded By: `_init_frame_mapping()` (v3.6: called in `if __name__ == "__main__":` block)
   - Used For: Automatic slope/offset calculation for Frame-to-x conversion
   - Path: Multiple path support (script dir, cwd, /mnt/data)
   - Optional: Falls back to default values if not found

3. **Tank Data** (v3.2): `data/tank_coordinates.json` + `data/tank_data.json`
   - Format: JSON objects with `data` array
   - Fields: `Tank_Name`, `Mid_Fr`, `Weight_MT`, `Volume_m3`, etc.
   - Loaded By: `build_tank_lookup()`
   - Used For: Ballast_Tanks sheet generation
   - Path: Multiple path support (script dir, cwd, /mnt/data)
   - Optional: Falls back to hardcoded values if not found

4. **Hydro_Table Data** (v3.6): `data/hydro_table.json`
   - Format: JSON array with 12 hydrostatic data points
   - Structure: `[{"Disp_t": ..., "Tmean_m": ..., "Trim_m": ..., "GM_m": ..., "Draft_FWD": ..., "Draft_AFT": ...}, ...]` or `[[...], ...]` (array format)
   - Fields: `Disp_t`, `Tmean_m`, `Trim_m`, `GM_m`, `Draft_FWD`, `Draft_AFT`
   - Loaded By: `create_hydro_table_sheet()`
   - Used For: Hydro_Table sheet generation
   - Path: Multiple path support (script dir, cwd, /mnt/data)
   - Optional: Falls back to 4 hardcoded points if not found

#### Hardcoded Values
**Calc Sheet Parameters**:
- L_ramp_m = 12.0
- theta_max_deg = 6.0
- KminusZ_m = 3.0
- D_vessel_m = 3.65
- min_fwd_draft_m = 1.5
- max_fwd_draft_m = 3.5
- pump_rate_tph = 10.0
- MTC_t_m_per_cm = 33.99
- LCF_m_from_midship = 30.91
- TPC_t_per_cm = 7.95
- Lpp_m = 60.302
- max_fwd_draft_ops_m = 2.70
- ramp_door_offset_m = 0.15
- linkspan_freeboard_target_m = 0.28
- gm_target_m = 1.50
- limit_reaction_t = 201.60
- limit_share_load_t = 118.80
- limit_deck_press_tpm2 = 10.00
- linkspan_area_m2 = 12.00
- max_aft_ballast_cap_t = 1200.00
- max_pump_time_h = 6.00

**RORO Sheet Parameters**:
- Tmean_baseline = 2.33
- Tide_ref = 2.0
- Pump rate = 5.0
- X_Ballast = 52.53

**Stage Defaults** (v3.2/v3.3):
- **Stage 5**: W=0.0 t, x=fr_to_x(52.5) ≈ 22.35 m (Ballast only) - **v3.3**: Trim target = -89.58 cm
- **Stage 6A**: W=434.0 t, x=fr_to_x(42.0) (Frame-based)
- **Stage 6B**: W=434.0 t, x=fr_to_x(38.0) (Frame-based)
- **Stage 6C**: W=868.0 t, x=fr_to_x(40.0) (Frame-based)
- **Stage 7**: W=0.0 t, x=fr_to_x(30.15) ≈ 0.00 m (Cargo off) - **v3.3**: Trim target = 0.0 cm (Even keel)

**Ballast_Tanks Sheet Data** (v3.2 Enhanced):
- 8 tank entries with positions, capacities, specific gravities, use flags, and air vent diameters
- Data source: JSON-based lookup via `build_tank_lookup()` with fallback values
- Coordinates (x_from_mid_m): Calculated from `Mid_Fr` using `fr_to_x()` function (Frame-based)
- Capacities (max_t): Real Weight@100% values from `tank_data.json` (preferred) or `tank_coordinates.json` (fallback)
- SG: Auto-assigned based on tank name prefix (FWB=1.025, FWCARGO=1.000)
- Air vent diameters: Auto-assigned based on tank name prefix (FWB=80mm, FWCARGO=125mm)
- Tanks: FWB1.P/S, FWB2.P/S (use_flag="Y"), FWCARGO1.P/S, FWCARGO2.P/S (use_flag="N")

**Hydro_Table Sheet Data** (v3.6):
- **Primary**: 12 hydrostatic entries loaded from `data/hydro_table.json`
- **Fallback**: 4 hardcoded entries if JSON not found
- Fields: displacement, mean draft, trim, GM, and draft values
- Used for GM lookup via VLOOKUP in RORO sheet

### 9.2 Sheet Dependencies

#### Dependency Graph
```
JSON Files
    │
    ├─→ gateab_v3_tide_data.json
    │       └─→ December_Tide_2025 Sheet
    │               └─→ Hourly_FWD_AFT_Heights Sheet
    │                       └─→ (references Calc sheet)
    │
    ├─→ Frame_x_from_mid_m.json (v3.2/v3.6)
    │       └─→ _init_frame_mapping() (v3.6: called in if __name__ == "__main__": block)
    │               └─→ Calculates _FRAME_SLOPE and _FRAME_OFFSET
    │               └─→ Used by fr_to_x() and x_to_fr() functions
    │               └─→ Used in RORO_Stage_Scenarios (Stage 5/6/7 coordinates)
    │
    ├─→ tank_coordinates.json + tank_data.json (v3.2)
    │       └─→ build_tank_lookup()
    │               └─→ create_ballast_tanks_sheet()
    │                       └─→ Ballast_Tanks Sheet (JSON-based with fallback)
    │
    └─→ data/hydro_table.json (v3.6)
            └─→ create_hydro_table_sheet()
                    └─→ Hydro_Table Sheet (12 points, falls back to 4 if JSON not found)

Calc Sheet (Parameters)
    │
    ├─→ Hourly_FWD_AFT_Heights Sheet
    ├─→ RORO_Stage_Scenarios Sheet
    └─→ CAPTAIN_REPORT Sheet (via RORO references)

Hydro_Table Sheet (v3.6: JSON-based with 12 points, fallback to 4)
    │
    └─→ RORO_Stage_Scenarios Sheet (GM lookup via VLOOKUP)

RORO_Stage_Scenarios Sheet
    │
    ├─→ Uses fr_to_x() for Stage 5/6/7 coordinates (v3.2)
    └─→ CAPTAIN_REPORT Sheet (stage summaries)

Ballast_Tanks Sheet
    └─→ JSON-based lookup with fallback values (v3.2)
```

#### Detailed Dependencies

**Calc Sheet → Hourly_FWD_AFT_Heights Sheet**:
- `KminusZ_m` → Used in Dfwd_req calculation
- `L_ramp_m` → Used in Dfwd_req and Ramp_Angle calculations
- `theta_max_deg` → Used in Dfwd_req and Status check
- `D_vessel_m` → Used in Height calculations
- `min_fwd_draft_m` → Used in Status check
- `max_fwd_draft_m` → Used in Status check

**December_Tide_2025 Sheet → Hourly_FWD_AFT_Heights Sheet**:
- Column A (datetime) → Column A of Hourly sheet
- Column B (tide_m) → Column B of Hourly sheet
- Row Mapping: Same row number in both sheets (row 2-745)

**Calc Sheet → RORO_Stage_Scenarios Sheet**:
- `MTC_t_m_per_cm` → Used in Trim_cm and ΔTM calculations
- `LCF_m_from_midship` → Used in TM and Lever_arm calculations
- `TPC_t_per_cm` → Used in rule-of-thumb ballast calculation
- `Lpp_m` → Used in Trim_Check calculation
- `max_fwd_draft_ops_m` → Used in Draft_OK check (column V)
- `linkspan_freeboard_target_m` → Used in Clearance_Check (column Z)
- `gm_target_m` → Used in GM_Check (column AB)
- `limit_reaction_t` → Used in Rx_Check (column AH)
- `limit_share_load_t` → Used in Share_Check (column AF)
- `limit_deck_press_tpm2` → Used in Press_Check (column AJ)
- `linkspan_area_m2` → Used in Deck_Press calculation (column AI)
- `max_aft_ballast_cap_t` → Used in Fix_Status (column AO)
- `max_pump_time_h` → Used in Fix_Status (column AO)
- `pump_rate_tph` → Used in Time_Add calculation (column AN)

**Hydro_Table Sheet → RORO_Stage_Scenarios Sheet**:
- Column B (Tmean_m) → Used as lookup key for VLOOKUP
- Column D (GM_m) → Returned value for GM lookup (column T)
- Lookup: VLOOKUP(AVERAGE(O, P), Hydro_Table!$B:$D, 3, 1)

**RORO_Stage_Scenarios Sheet → CAPTAIN_REPORT Sheet**:
- Column A (Stage) → Column A of CAPTAIN_REPORT
- Column O (Dfwd_m) → Column B of CAPTAIN_REPORT
- Column P (Daft_m) → Column C of CAPTAIN_REPORT
- Column F (Trim_m) → Column D of CAPTAIN_REPORT
- Column Q (FWD_Height_m) → Column G of CAPTAIN_REPORT
- Column Y (Phys_Freeboard_m) → Used in Freeboard_OK check (column H)
- Column S (Notes) → Column I of CAPTAIN_REPORT

**Frame_to_x_Table Sheet**:
- Reference data only (no formula dependencies)
- Used by `_init_frame_mapping()` for automatic slope/offset estimation
- Provides lookup table for users

**Frame Mapping Initialization** (v3.2/v3.6):
- `Frame_x_from_mid_m.json` → `_init_frame_mapping()` → `_FRAME_SLOPE` and `_FRAME_OFFSET`
- **v3.6**: Now called in `if __name__ == "__main__":` block instead of module level
- Used by `fr_to_x()` and `x_to_fr()` functions
- Used in `create_roro_sheet()` for Stage 5/6/7 coordinate definitions
- Used in `build_tank_lookup()` for tank coordinate conversion

**Tank Data Lookup** (v3.2):
- `tank_coordinates.json` + `tank_data.json` → `build_tank_lookup()` → Tank lookup dictionary
- Used by `create_ballast_tanks_sheet()` for Ballast_Tanks sheet generation
- Auto-assigns SG and air_vent based on tank name prefix

**Hydro_Table Data Lookup** (v3.6):
- `data/hydro_table.json` → `create_hydro_table_sheet()` → Hydro_Table sheet (12 points)
- Falls back to 4 hardcoded points if JSON not found
- Supports both dict list and array formats
- Used for GM lookup via VLOOKUP in RORO sheet

### 9.3 Calculation Sequence

#### Sheet Creation Order
1. **Frame Mapping Initialization** (v3.2/v3.6) - **v3.6**: `_init_frame_mapping()` called in `if __name__ == "__main__":` block
2. **Calc Sheet** (created first) - Contains all parameters, no dependencies
3. **December_Tide_2025 Sheet** (created second) - Loads data from JSON, no dependencies
4. **Hourly_FWD_AFT_Heights Sheet** (created third) - Depends on Calc and Tide sheets
5. **RORO_Stage_Scenarios Sheet** (created fourth) - Depends on Calc sheet, uses fr_to_x() for Stage 5/6/7
6. **Ballast_Tanks Sheet** (created fifth) - JSON-based lookup via build_tank_lookup() (v3.2)
7. **Hydro_Table Sheet** (created sixth) - **v3.6**: Loads from `data/hydro_table.json` (12 points), falls back to 4 hardcoded points
8. **Frame_to_x_Table Sheet** (created seventh) - Reference data for Frame-to-x conversion (from JSON)
9. **RORO Extensions** (applied eighth) - extend_roro_captain_req() and extend_roro_structural_opt1() (v3.3.1: with auto-bound row ranges)
10. **CAPTAIN_REPORT Sheet** (created last) - Depends on RORO sheet (v3.3.1: with auto-bound row mapping)

#### Formula Calculation Order (Within Hourly Sheet)
For each row (2-745):
1. Column A: DateTime from tide sheet
2. Column B: Tide from tide sheet
3. Column C: Dfwd_req (uses Calc parameters + Tide)
4. Column D: Trim input (user-entered, optional)
5. Column E: Dfwd_adj (uses C and D)
6. Column F: Daft_adj (uses C and D)
7. Column G: Ramp_Angle (uses Calc parameters + E + B)
8. Column H: Status (uses E, G, and Calc parameters)
9. Column I: FWD_Height (uses Calc parameters + E + B)
10. Column J: AFT_Height (uses Calc parameters + F + B)
11. Column K: Notes (uses D)

#### Formula Calculation Order (Within RORO Sheet)
For each stage row (15-26):
1. Columns B, C: W and x (inputs with defaults, v3.2: Stage 5/7 use fr_to_x() for x coordinates)
2. Column D: TM (uses B, C, LCF)
3. Column E: Trim_cm (uses D, MTC)
4. Column F: Trim_m (uses E)
5. Column G: Trim_target_cm (input with default, v3.3: Stage 5 = -89.58 cm, Stage 7 = 0.0 cm)
6. Column H: ΔTM (uses MTC, TRIM5_CM, G)
7. Column I: Lever_arm (uses X_Ballast, LCF)
8. Column J: Ballast_t_calc (uses H, I)
9. Column K: Ballast_time_h_calc (uses J, PumpRate)
10. Column L: Ballast_t (rule-of-thumb, uses F, TPC)
11. Column M: Ballast_time_h (uses L, PumpRate)
12. Column N: Trim_Check (uses F, Lpp)
13. Column O: Dfwd_m (uses Tmean_baseline, F)
14. Column P: Daft_m (uses Tmean_baseline, F)
15. Column Q: FWD_Height (uses D_vessel, O, Tide_ref)
16. Column R: AFT_Height (uses D_vessel, P, Tide_ref)
17. Column S: Notes (text, v3.2: Updated descriptions for Stage 2/3/5/6A/6B/6C/7)
18. Column T: GM (uses O, P, Hydro_Table via VLOOKUP)
19. Column U: Fwd Draft (copy from O)
20. Column V: vs 2.70m (uses U, Calc!E18)
21. Column W: De-ballast Qty (copy from J)
22. Column X: Timing (input)
23. Column Y: Phys_Freeboard (uses O, D_vessel)
24. Column Z: Clearance_Check (uses Y, Calc!E20)
25. Column AA: GM_calc (copy from T)
26. Column AB: GM_Check (uses AA, Calc!E21)
27. Column AC: Prop Imm (uses P)
28. Column AD: Vent_Time (uses W)
29. Column AE: Share_Load (input)
30. Column AF: Share_Check (uses AE, Calc!E24)
31. Column AG: Hinge_Rx (auto-calculated formula: 45 + AE × 0.545, not input)
32. Column AH: Rx_Check (uses AG, Calc!E37)
33. Column AI: Deck_Press (uses AE, Calc!E26)
34. Column AJ: Press_Check (uses AI, Calc!E25)
35. Column AK: ΔTM_needed (uses E, G, Calc!E14)
36. Column AL: Ballast_req (uses AK, I)
37. Column AM: Ballast_gap (uses AL, J)
38. Column AN: Time_Add (uses AM, Calc!E12)
39. Column AO: Fix_Status (uses AL, AN, Calc!E27, Calc!E28)
40. Column AS: Ramp_Angle_deg (uses Y, Calc!E33, Calc!E35)
41. Column AT: Ramp_Angle_Check (uses AS)
42. Column AU: Pin_Stress_N_mm2 (uses AG, Calc!E36)
43. Column AV: Von_Mises_Check (uses AU)

### 9.4 Data Flow Diagram

```
┌─────────────────────────────────────────────────────────┐
│                    JSON File                             │
│         (gateab_v3_tide_data.json)                      │
│                 744 entries                              │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│            December_Tide_2025 Sheet                     │
│             744 rows of tide data                       │
└────────────────────┬────────────────────────────────────┘
                     │
                     │ (references)
                     ▼
┌─────────────────────────────────────────────────────────┐
│         Hourly_FWD_AFT_Heights Sheet                    │
│           744 rows × 10 formulas                        │
│         = 7,440 formulas                                │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│                  Calc Sheet                              │
│              19 parameters                               │
│  (includes Structural Limits & Ballast Fix Check)       │
└───────┬───────────────────────────────────────┬─────────┘
        │                                       │
        │ (references)                          │ (references)
        ▼                                       ▼
┌──────────────────────────┐    ┌──────────────────────────────┐
│ Hourly_FWD_AFT_Heights   │    │ RORO_Stage_Scenarios Sheet   │
│        Sheet             │    │     12 stages, 45 columns    │
└──────────────────────────┘    └──────────────┬───────────────┘
                                               │
                                               │ (references)
                                               ▼
                                    ┌──────────────────────────┐
                                    │ CAPTAIN_REPORT Sheet     │
                                    │   Stage summaries        │
                                    └──────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│              Hydro_Table Sheet                          │
│              4 hydrostatic entries                      │
└────────────────────┬────────────────────────────────────┘
                     │
                     │ (VLOOKUP for GM)
                     ▼
        ┌──────────────────────────────┐
        │ RORO_Stage_Scenarios Sheet   │
        │      Column T (GM lookup)    │
        └──────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│            Ballast_Tanks Sheet                          │
│              6 tank entries                             │
│         (Reference data only)                           │
└─────────────────────────────────────────────────────────┘
```

---

## Summary

This document covers:
1. **Mathematical Formulas**: All formulas with derivations and examples
2. **Coordinate System**: Midship-based coordinate system and sign conventions
3. **Trim Calculations**: Trimming moment, trim in cm and m
4. **Draft Calculations**: Mean draft, forward/aft draft from trim
5. **Ramp Angle Calculations**: Geometry-based ramp angle calculation (Hourly sheet and RORO sheet), Pin Stress calculation
6. **Ballast Calculations**: Lever-arm method, rule-of-thumb method, and Option 1 fix check
7. **Height Calculations**: Freeboard calculations (with and without tide), propeller immersion
8. **GM Lookup**: VLOOKUP-based GM retrieval from hydrostatic table
9. **Status Validation**: Draft limits, ramp angle limits, trim limits, freeboard limits, GM limits
10. **Structural Strength Validation**: Share load, hinge reaction, deck pressure checks, and pin stress (Von Mises) validation
11. **Option 1 Ballast Fix Check**: Required ballast, gap calculation, time estimation, and status validation
12. **Data Flow**: Data sources, sheet dependencies, calculation sequence

All formulas are based on:
- **Naval Architecture Principles**: Trim, draft, stability, and GM calculations
- **Geometric Relationships**: Ramp angle, height, and freeboard calculations
- **Moment Balance**: Ballast and trimming moment calculations
- **Structural Engineering**: Load distribution, reaction forces, and pressure calculations
- **Safety Limits**: Validation against operational, structural, and stability constraints

**Complete Documentation Index**: See [EXCEL_GEN_01_OVERVIEW_AND_ARCHITECTURE.md](EXCEL_GEN_01_OVERVIEW_AND_ARCHITECTURE.md)

---

**End of Mathematics and Data Flow Document**

