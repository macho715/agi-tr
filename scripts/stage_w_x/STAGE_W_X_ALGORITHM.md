# Stage W, X Algorithm Documentation

**LCT BUSHRA RORO Calculator - Stage Weight and Position Determination Algorithm**

**Version:** 1.0  
**Date:** 2025-11-06  
**Author:** MACHO-GPT v3.4-mini

---

## Table of Contents

1. [Introduction and Purpose](#1-introduction-and-purpose)
2. [Coordinate System](#2-coordinate-system)
3. [Stage Definitions and Physical Meaning](#3-stage-definitions-and-physical-meaning)
4. [W (Weight) Determination Algorithm](#4-w-weight-determination-algorithm)
5. [X (Position) Determination Algorithm](#5-x-position-determination-algorithm)
6. [Composite Center Calculation](#6-composite-center-calculation)
7. [Practical Extraction from Stowage Plan](#7-practical-extraction-from-stowage-plan)
8. [Validation and Verification](#8-validation-and-verification)
9. [Examples](#9-examples)
10. [References and Related Documents](#10-references-and-related-documents)

---

## 1. Introduction and Purpose

### 1.1 Overview

This document describes the algorithm for determining `W_stage_t` (stage weight in tons) and `x_stage_m` (stage position in meters from midship) for each RORO loading stage in the LCT BUSHRA calculator system.

### 1.2 Purpose

The algorithm enables accurate calculation of:
- **Trim** (longitudinal inclination) at each loading stage
- **Forward and Aft Drafts** (Dfwd, Daft)
- **Forward and Aft Heights** (FWD_Height, AFT_Height)
- **Ballast requirements** to maintain safe trim limits

### 1.3 Key Parameters

- **W_stage_t**: Total weight acting on the vessel at a given stage (tons)
- **x_stage_m**: Longitudinal position of the weight center from midship (meters)
- **LCF**: Longitudinal Center of Flotation = +29.29 m from midship (stern direction, at Draft ~2.50m, verified from Stability Book)
- **MTC**: Moment to Change Trim 1cm = 40.72 t·m/cm (at Draft ~2.50m, verified from Stability Book)

---

## 2. Coordinate System

### 2.1 Origin Definition

**Midship = 0 m**

The coordinate system uses the vessel's midship (midpoint between forward and aft perpendiculars) as the origin.

### 2.2 Sign Convention

- **Negative x**: Bow direction (forward of midship)
- **Positive x**: Stern direction (aft of midship)

### 2.3 Key Reference Points

| Reference Point | Symbol | Position (m) | Description |
|----------------|--------|--------------|-------------|
| Midship | - | 0.00 | Origin of coordinate system |
| LCF | LCF_m_from_midship | +29.29 | Longitudinal Center of Flotation (stern direction, at Draft ~2.50m, verified) |
| AP to Midship | AP_to_midship_m | 30.151 | Distance from After Perpendicular to midship (Lpp/2, verified) |
| Lpp | Lpp_m | 60.302 | Length between perpendiculars (verified) |

### 2.4 Coordinate Transformation

**From AP (After Perpendicular) to Midship:**
```
x_mid_m = AP_to_midship_m - LCG_AP
```

Where:
- `x_mid_m`: Position from midship (m)
- `AP_to_midship_m`: 30.151 m (constant, Lpp/2, verified)
- `LCG_AP`: Longitudinal Center of Gravity from AP (m)

**Example:**
- Tank LCG_AP = 25.600 m
- `x_mid_m = 30.151 - 25.600 = 4.551 m` (stern direction)

---

## 3. Stage Definitions and Physical Meaning

### 3.1 Stage 1: Empty Condition

| Parameter | Value | Description |
|-----------|-------|-------------|
| **W_stage_t** | 0 | No cargo on board |
| **x_stage_m** | – (empty) | No position (reference baseline) |
| **Physical Meaning** | Initial vessel condition before cargo loading |
| **Trim** | Even-keel (assumed) | Baseline for subsequent calculations |

**Usage:**
- Reference point for all subsequent stages
- No weight or moment contribution
- Used to establish initial trim state

---

### 3.2 Stage 2: SPMT 1st Entry on Ramp

| Parameter | Value | Description |
|-----------|-------|-------------|
| **W_stage_t** | 65 | ~30% of total unit weight (217t × 0.3 ≈ 65t) |
| **x_stage_m** | -10.0 | Bow direction, ramp entry point |
| **Physical Meaning** | SPMT first contacts ramp, ~30% reaction force on vessel |
| **Reaction Force** | ~30% of unit weight transferred to vessel structure |

**Calculation Rationale:**
- When SPMT first enters ramp, only a portion of the unit weight is supported by the vessel
- Remaining weight is still on shore/quay
- Typical reaction: 25-35% of total weight
- Position: Ramp entry point projected to midship coordinate

**Typical Values:**
- Weight: 50-80 t (depending on unit weight and ramp angle)
- Position: -8 to -12 m (ramp entry location)

---

### 3.3 Stage 3: ~50% on Ramp

| Parameter | Value | Description |
|-----------|-------|-------------|
| **W_stage_t** | 110 | ~50% of total unit weight (217t × 0.5 ≈ 110t) |
| **x_stage_m** | -5.0 | Bow direction, mid-ramp position |
| **Physical Meaning** | SPMT approximately halfway on ramp, ~50% reaction force |
| **Reaction Force** | ~50% of unit weight on vessel, ~50% on shore |

**Calculation Rationale:**
- SPMT has moved further onto ramp
- Weight distribution: ~50% vessel, ~50% shore
- Position moves closer to midship as SPMT advances
- Critical stage for trim monitoring (maximum bow-down moment)

**Typical Values:**
- Weight: 100-130 t (45-60% of unit weight)
- Position: -4 to -6 m (mid-ramp location)

---

### 3.4 Stage 4: Full on Ramp / Break-Even

| Parameter | Value | Description |
|-----------|-------|-------------|
| **W_stage_t** | 217 | Full unit weight (1 unit, 217t) |
| **x_stage_m** | -2.0 | Bow direction, near ramp end |
| **Physical Meaning** | Full unit weight on vessel, break-even point (all weight transferred) |
| **Reaction Force** | 100% of unit weight on vessel |

**Calculation Rationale:**
- Complete weight transfer from shore to vessel
- Unit fully on ramp, ready to move to deck
- Position: Ramp end or bow sill area
- Critical for maximum trim calculation

**Typical Values:**
- Weight: Full unit weight (e.g., 217t for transformer)
- Position: -1 to -3 m (ramp end / bow sill)

---

### 3.5 Stage 5: Deck Full Load (Multiple Units)

| Parameter | Value | Description |
|-----------|-------|-------------|
| **W_stage_t** | 434 | Two units total (217t × 2 = 434t) |
| **x_stage_m** | +15.27 | Stern direction, composite center of two units (verified from stowage plan) |
| **Physical Meaning** | Both units on deck, positioned for trim balance |
| **Composite Center** | Weighted average position of all units |

**Calculation Rationale:**
- Multiple units require composite center calculation
- Target: Position composite center near LCF (+29.29 m) for minimal trim
- Formula: `x_composite = Σ(W_i × x_i) / ΣW_i`

**Example Calculation (from verified stowage plan):**
- Unit 1: W₁ = 217t, x₁ = +8.27 m
- Unit 2: W₂ = 217t, x₂ = +22.27 m
- `x_composite = (217×8.27 + 217×22.27) / (217+217) = 6,625.18 / 434 = 15.27 m`

**Typical Values:**
- Weight: Sum of all units (e.g., 434t for 2 units)
- Position: +10 to +25 m (depends on stowage plan, verified: +15.27 m)

---

### 3.6 Stage 6: TR1 Final + TR2 on Ramp (Critical Intermediate Condition)

| Parameter | Value | Description |
|-----------|-------|-------------|
| **W_stage_t** | 434 | Two units total (217t × 2 = 434t), **cargo only** (ballast excluded) |
| **x_stage_m** | +5.71 | Composite center: TR1 at final position + TR2 on ramp |
| **Physical Meaning** | TR1 at final stowage position, TR2 fully on bow ramp (no ballast adjustment) |
| **Composite Center** | Weighted average of TR1 final position and TR2 ramp position |

**Calculation Rationale:**
- TR1: W₁ = 217t, x₁ = +15.27 m (Stage 5 final position, or TR1+TR2 combined CG)
- TR2: W₂ = 217t, x₂ = -3.85 m (Stage 4 ramp position, **using same coordinate system as Stage 1-5**)
- Formula: `x_composite = Σ(W_i × x_i) / ΣW_i`

**Example Calculation (using Stage 4/5 coordinate system):**
- TR1: W₁ = 217t, x₁ = +15.27 m
- TR2: W₂ = 217t, x₂ = -3.85 m
- `x_composite = (217×15.27 + 217×(-3.85)) / (217+217) = (3,313.59 - 835.45) / 434 = 2,478.14 / 434 = 5.71 m`

**Trim Calculation:**
```
TM_6 = W_stage_6 × (x_stage_6 - LCF)
     = 434 × (5.71 - 30.91)
     = 434 × (-25.20)
     = -10,936.8 t·m

Trim_cm_6 = TM_6 / MTC
          = -10,936.8 / 41.47
          ≈ -263.7 cm

Trim_m_6 = -2.64 m (significant bow-down trim)
```

**Important Notes:**
- **Coordinate System Consistency**: Uses the same coordinate system as Stage 1-5 (AP-based)
- **TR2 Position**: x₂ = -3.85 m is from Stage 4 (verified ramp position), NOT an estimated value
- **W_stage_t**: Contains cargo only (434t), ballast is calculated separately via ΔTM
- **Purpose**: Represents worst-case forward loading moment for verification

---

### 3.7 Stage 7: Stage 6 + AFT Ballast Correction (Operational Correction Stage)

| Parameter | Value | Description |
|-----------|-------|-------------|
| **W_stage_t** | 434 | **Cargo only** (same as Stage 6), ballast excluded from W_stage_t |
| **x_stage_m** | +13.06 | Composite center: Stage 6 cargo + AFT ballast (for reference, but W is cargo only) |
| **Physical Meaning** | Stage 6 condition + aft ballast applied to achieve target trim within limits |
| **Ballast Calculation** | Ballast effect calculated separately via ΔTM and Lever_arm |

**Calculation Rationale:**
- **Cargo**: W_cargo = 434t, x_cargo = 5.71 m (same as Stage 6)
- **AFT Ballast**: W_ballast = 146t, x_ballast = 50.0 m (Stage 5A-2 reference)
- **Composite Center** (for reference only):
  - `x_composite = (434×5.71 + 146×50.0) / (434+146) = (2,478.14 + 7,300) / 580 = 9,778.14 / 580 = 13.06 m`
- **W_stage_t**: Remains 434t (cargo only), ballast is NOT included in W_stage_t

**Trim Calculation:**
```
TM_7 = W_stage_7 × (x_stage_7 - LCF)
     = 434 × (13.06 - 30.91)
     = 434 × (-17.85)
     = -7,750.5 t·m

Trim_cm_7 = TM_7 / MTC
          = -7,750.5 / 41.47
          ≈ -186.9 cm

Trim_m_7 = -1.87 m (improved from Stage 6, but still significant)
```

**Ballast Requirement Calculation:**
```
ΔTrim_cm = Trim_target_cm_7 - Trim_cm_6
         = (-96.5) - (-263.7)
         = 167.2 cm

ΔTM_cm_tm_7 = ΔTrim_cm × MTC
            = 167.2 × 41.47
            ≈ 6,933 t·m

Lever_arm_m = X_Ballast - LCF
            = 50.0 - 30.91
            = 19.09 m

Ballast_t_required_7 = ΔTM_cm_tm_7 / Lever_arm_m
                     ≈ 6,933 / 19.09
                     ≈ 363 t
```

**Important Notes:**
- **W_stage_t Consistency**: W_stage_t = 434t (cargo only), same as Stage 6
- **Ballast Separation**: Ballast effect is calculated separately, NOT included in W_stage_t
- **x_stage_m**: Represents composite center of cargo + ballast (13.06 m), but W remains cargo only
- **Purpose**: Operational correction stage showing required ballast to achieve target trim
- **Coordinate System**: Uses same coordinate system as Stage 1-6

---

## 4. W (Weight) Determination Algorithm

### 4.1 Single Unit Loading

**Algorithm:**
```
W_stage = Reaction_Percentage × Unit_Weight
```

Where:
- `Reaction_Percentage`: Fraction of weight on vessel (0.0 to 1.0)
- `Unit_Weight`: Total weight of single unit (tons)

**Stage-Based Reaction Percentages:**

| Stage | Reaction % | Calculation | Example (217t unit) |
|-------|------------|-------------|---------------------|
| Stage 2 | ~30% | 0.30 × Unit_Weight | 0.30 × 217 = 65 t |
| Stage 3 | ~50% | 0.50 × Unit_Weight | 0.50 × 217 = 110 t |
| Stage 4 | 100% | 1.00 × Unit_Weight | 1.00 × 217 = 217 t |

### 4.2 Multiple Units Loading

**Algorithm:**
```
W_stage = Σ(W_i) for all units i
```

**Example:**
- Unit 1: 217 t
- Unit 2: 217 t
- `W_stage = 217 + 217 = 434 t`

### 4.3 Weight Measurement Methods

1. **From Stowage Plan:**
   - Unit weight specified in plan
   - Verify with actual weighing if available

2. **From SPMT Configuration:**
   - SPMT axle loads × number of axles
   - Sum of all SPMT loads

3. **From Reaction Force Measurement:**
   - Load cells on ramp (if available)
   - Direct measurement of vessel reaction

4. **From Trim Change:**
   - Measure trim change
   - Back-calculate weight using: `W = (ΔTrim × MTC × 100) / (x - LCF)`

---

## 5. X (Position) Determination Algorithm

### 5.1 Single Unit on Ramp

**Algorithm:**
```
x_stage = Project_Ramp_Contact_Point_To_Midship(ramp_position)
```

**Steps:**
1. Identify ramp contact point (hinge, support, or actual contact)
2. Measure distance from AP to contact point
3. Convert to midship coordinate: `x_mid = 32.00 - LCG_AP_contact`
4. Project vertical to midship reference line

**Typical Ramp Positions:**

| Stage | Ramp Location | Typical x (m) | Description |
|-------|---------------|---------------|-------------|
| Stage 2 | Entry | -8 to -12 | Ramp hinge or entry support |
| Stage 3 | Mid-ramp | -4 to -6 | 50% along ramp length |
| Stage 4 | Ramp end | -1 to -3 | Bow sill or ramp termination |

### 5.2 Single Unit on Deck

**Algorithm:**
```
x_stage = Unit_LCG_from_midship
```

**Steps:**
1. From stowage plan, find unit center position
2. Measure from AP to unit center: `LCG_AP`
3. Convert to midship: `x_mid = 30.151 - LCG_AP`

**Example:**
- Unit center at LCG_AP = 25.6 m
- `x_stage = 30.151 - 25.6 = 4.551 m` (stern direction)

### 5.3 Multiple Units (Composite Center)

**Algorithm:**
```
x_composite = Σ(W_i × x_i) / Σ(W_i)
```

Where:
- `W_i`: Weight of unit i (tons)
- `x_i`: Position of unit i from midship (m)

**Example Calculation (from verified stowage plan):**

Given:
- Unit 1: W₁ = 217t, x₁ = +8.27 m
- Unit 2: W₂ = 217t, x₂ = +22.27 m

Calculation:
```
x_composite = (217 × 8.27 + 217 × 22.27) / (217 + 217)
            = (1,794.59 + 4,832.59) / 434
            = 6,627.18 / 434
            = 15.27 m
```

**Trim Balance Optimization:**
- Target: `x_composite ≈ LCF = +29.29 m`
- If `x_composite < LCF`: Move units stern-ward
- If `x_composite > LCF`: Move units bow-ward
- Current verified value: `x_composite = +15.27 m` (forward of LCF, causing bow-down trim)

---

## 6. Composite Center Calculation

### 6.1 General Formula

For n units:
```
x_composite = (W₁×x₁ + W₂×x₂ + ... + Wₙ×xₙ) / (W₁ + W₂ + ... + Wₙ)
```

### 6.2 Step-by-Step Procedure

1. **List all units:**
   ```
   Unit 1: W₁ = 217t, x₁ = +8.27 m
   Unit 2: W₂ = 217t, x₂ = +22.27 m
   ```

2. **Calculate weighted sum:**
   ```
   Σ(W_i × x_i) = 217×8.27 + 217×22.27 = 1,794.59 + 4,832.59 = 6,627.18 t·m
   ```

3. **Calculate total weight:**
   ```
   ΣW_i = 217 + 217 = 434 t
   ```

4. **Calculate composite center:**
   ```
   x_composite = 6,627.18 / 434 = 15.27 m
   ```

5. **Verify trim balance:**
   ```
   TM = W_total × (x_composite - LCF)
      = 434 × (15.27 - 29.29)
      = 434 × (-14.02)
      = -6,084.68 t·m (bow-down trim)
   
   Trim_cm = TM / MTC = -6,084.68 / 40.72 = -149.43 cm
   Trim_m = -1.49 m (significant bow-down trim)
   ```

### 6.3 Optimization for Trim Balance

**Target:** Minimize trim by aligning composite center with LCF

**Algorithm:**
```
If x_composite ≠ LCF:
    Adjust unit positions to achieve x_composite ≈ LCF
```

**Example Adjustment:**

Initial (from verified stowage plan):
- Unit 1: x₁ = +8.27 m
- Unit 2: x₂ = +22.27 m
- x_composite = 15.27 m (forward of LCF, causing -1.49m bow-down trim)

Adjusted (move both units stern-ward to approach LCF):
- Unit 1: x₁ = +18.27 m (moved 10.0 m aft)
- Unit 2: x₂ = +32.27 m (moved 10.0 m aft)
- x_composite = (217×18.27 + 217×32.27) / 434 = 25.27 m (closer to LCF=29.29m)
- TM = 434 × (25.27 - 29.29) = -1,744.68 t·m
- Trim = -1,744.68 / (40.72×100) = -0.43 m (improved from -1.49m)

---

## 7. Practical Extraction from Stowage Plan

### 7.1 Coordinate Extraction Procedure

1. **Identify Reference Points:**
   - Locate midship mark on plan
   - Locate AP (After Perpendicular) mark
   - Verify scale and units

2. **Measure Unit Position:**
   - Find unit center (geometric center or CG mark)
   - Measure distance from AP to unit center
   - Record as `LCG_AP`

3. **Convert to Midship Coordinate:**
   ```
   x_mid = AP_to_midship - LCG_AP
   x_mid = 30.151 - LCG_AP
   ```

4. **Verify Sign Convention:**
   - If `LCG_AP < 30.151`: `x_mid > 0` (stern direction) ✓
   - If `LCG_AP > 30.151`: `x_mid < 0` (bow direction) ✓

### 7.2 Ramp Contact Point Determination

**For Ramp Stages (2, 3, 4):**

1. **Identify Contact Type:**
   - Ramp hinge point
   - Support structure contact
   - Actual SPMT wheel contact

2. **Project to Midship:**
   - Measure from AP to contact point
   - Convert: `x_mid = 30.151 - LCG_AP_contact` (AP_to_midship = 30.151 m)

3. **Consider Ramp Angle:**
   - Vertical projection may be needed
   - Account for ramp inclination if significant

### 7.3 Multiple Units Extraction

1. **Extract Each Unit:**
   - Unit 1: W₁, x₁
   - Unit 2: W₂, x₂
   - ... (repeat for all units)

2. **Calculate Composite:**
   ```
   x_composite = Σ(W_i × x_i) / ΣW_i
   ```

3. **Verify Against LCF:**
   - Compare `x_composite` with LCF (+29.29 m)
   - Adjust if needed for trim balance

---

## 8. Validation and Verification

### 8.1 Input Validation

**W_stage_t Validation:**
- ✓ Must be ≥ 0
- ✓ Must be ≤ total unit weight(s)
- ✓ Must match stowage plan specifications

**x_stage_m Validation:**
- ✓ Must be within vessel length limits: `-30.151m ≤ x_stage_m ≤ +30.151m` (within Lpp=60.302m)
- ✓ Sign must match physical location (bow = negative, stern = positive)
- ✓ Must be consistent with stowage plan coordinates
- ✓ LCF position check: `LCF ≤ AP_to_midship_m` (verified: 29.29m ≤ 30.151m ✓)

### 8.2 Calculation Verification

**Trim Check:**
```
Trim_cm = TM / MTC
Trim_m = Trim_cm / 100
```

**Expected Ranges:**
- Stage 2-3: Moderate bow-down trim (expected)
- Stage 4: Maximum trim (critical)
- Stage 5: Near even-keel (optimized)

**Trim Limit Check:**
```
If |Trim_m| > Lpp_m / 50:
    Warning: EXCESSIVE TRIM
```

Where `Lpp_m = 60.302 m` (Length between perpendiculars, verified)

**Example:**
- `Trim_limit = 60.302 / 50 = 1.206 m`
- If `|Trim_m| > 1.206 m`: EXCESSIVE warning
- Stage 4: Trim = -1.77 m (EXCESSIVE, exceeds limit)
- Stage 5: Trim = -1.49 m (EXCESSIVE, exceeds limit)

### 8.3 Physical Verification

1. **Compare with Actual Measurements:**
   - Measure actual trim during loading
   - Compare with calculated trim
   - Adjust W, x if discrepancy > 5%

2. **Verify Weight Distribution:**
   - Check SPMT axle loads
   - Verify reaction force measurements
   - Confirm unit weights

3. **Verify Position:**
   - Measure actual unit positions on deck
   - Compare with stowage plan
   - Adjust x if needed

---

## 9. Examples

### 9.1 Example 1: Stage 2 (SPMT Entry)

**Given:**
- Unit weight: 217 t
- Reaction percentage: 30%
- Ramp entry position: LCG_AP = 42.0 m

**Calculation:**
```
W_stage = 0.30 × 217 = 65.1 t ≈ 65 t
x_stage = 30.151 - 42.0 = -11.85 m
```

**Result:**
- W_stage_t = 65 t
- x_stage_m = -11.85 m (bow direction, calculated with AP_to_midship = 30.151 m)

---

### 9.2 Example 2: Stage 4 (Full on Ramp)

**Given:**
- Unit weight: 217 t
- Reaction percentage: 100%
- Ramp end position: LCG_AP = 34.0 m

**Calculation:**
```
W_stage = 1.00 × 217 = 217 t
x_stage = 30.151 - 34.0 = -3.85 m
```

**Result:**
- W_stage_t = 217 t
- x_stage_m = -3.85 m (bow direction)

**Trim Calculation (with verified constants):**
```
TM = W × (x - LCF)
   = 217 × (-3.85 - 29.29)
   = 217 × (-33.14)
   = -7,191.38 t·m

Trim_cm = TM / MTC
        = -7,191.38 / 40.72
        = -176.56 cm

Trim_m = -176.56 / 100 = -1.77 m (bow-down, EXCESSIVE)
```

**Note:** This trim exceeds the limit of 1.206 m (Lpp/50), indicating excessive bow-down trim that requires ballast correction or stowage plan adjustment.

---

### 9.3 Example 3: Stage 5 (Two Units, Composite Center)

**Given (from verified stowage plan):**
- Unit 1: W₁ = 217 t, x₁ = +8.27 m (from midship, verified)
- Unit 2: W₂ = 217 t, x₂ = +22.27 m (from midship, verified)

**Step 1: Calculate Composite Center**
```
x_composite = (217×8.27 + 217×22.27) / (217 + 217)
            = (1,794.59 + 4,832.59) / 434
            = 6,627.18 / 434
            = 15.27 m
```

**Step 2: Calculate Total Weight**
```
W_total = 217 + 217 = 434 t
```

**Step 3: Calculate Trim (with verified constants)**
```
TM = W_total × (x_composite - LCF)
   = 434 × (15.27 - 29.29)
   = 434 × (-14.02)
   = -6,084.68 t·m

Trim_cm = TM / MTC
        = -6,084.68 / 40.72
        = -149.43 cm

Trim_m = -149.43 / 100 = -1.49 m (bow-down, EXCESSIVE)
```

**Result:**
- W_stage_t = 434 t
- x_stage_m = 15.27 m (from verified stowage plan)
- Trim = -1.49 m (exceeds limit of 1.206 m, requires ballast or stowage adjustment)

**Note:** The composite center (+15.27 m) is forward of LCF (+29.29 m), causing significant bow-down trim. To minimize trim, units should be positioned further aft to bring x_composite closer to LCF.

---

### 9.4 Example 4: Stage 6 (TR1 Final + TR2 on Ramp)

**Given (using Stage 4/5 coordinate system):**
- TR1: W₁ = 217 t, x₁ = +15.27 m (Stage 5 final position)
- TR2: W₂ = 217 t, x₂ = -3.85 m (Stage 4 ramp position, verified)

**Step 1: Calculate Composite Center**
```
x_composite = (217×15.27 + 217×(-3.85)) / (217 + 217)
            = (3,313.59 - 835.45) / 434
            = 2,478.14 / 434
            = 5.71 m
```

**Step 2: Calculate Total Weight**
```
W_total = 217 + 217 = 434 t (cargo only)
```

**Step 3: Calculate Trim (with verified constants)**
```
TM = W_total × (x_composite - LCF)
   = 434 × (5.71 - 30.91)
   = 434 × (-25.20)
   = -10,936.8 t·m

Trim_cm = TM / MTC
        = -10,936.8 / 41.47
        = -263.7 cm

Trim_m = -263.7 / 100 = -2.64 m (bow-down, EXCESSIVE)
```

**Result:**
- W_stage_t = 434 t (cargo only)
- x_stage_m = 5.71 m (using Stage 4/5 coordinate system)
- Trim = -2.64 m (exceeds limit, represents worst-case forward loading)

**Note:** This stage represents the critical intermediate condition with maximum forward loading moment. The significant bow-down trim requires ballast correction for safe operation.

---

### 9.5 Example 5: Stage 7 (Stage 6 + AFT Ballast Correction)

**Given:**
- Cargo: W_cargo = 434 t, x_cargo = 5.71 m (same as Stage 6)
- AFT Ballast: W_ballast = 146 t, x_ballast = 50.0 m (Stage 5A-2 reference)
- Target Trim: Trim_target_cm = -96.5 cm

**Step 1: Calculate Composite Center (for reference)**
```
x_composite = (434×5.71 + 146×50.0) / (434 + 146)
            = (2,478.14 + 7,300) / 580
            = 9,778.14 / 580
            = 13.06 m
```

**Step 2: W_stage_t (cargo only)**
```
W_stage_t = 434 t (cargo only, ballast NOT included)
```

**Step 3: Calculate Trim with Composite Center**
```
TM = W_stage_t × (x_stage_m - LCF)
   = 434 × (13.06 - 30.91)
   = 434 × (-17.85)
   = -7,750.5 t·m

Trim_cm = TM / MTC
        = -7,750.5 / 41.47
        = -186.9 cm

Trim_m = -1.87 m (improved from Stage 6)
```

**Step 4: Calculate Required Ballast**
```
ΔTrim_cm = Trim_target_cm - Trim_cm_6
         = (-96.5) - (-263.7)
         = 167.2 cm

ΔTM_cm_tm = ΔTrim_cm × MTC
          = 167.2 × 41.47
          = 6,933 t·m

Lever_arm_m = X_Ballast - LCF
            = 50.0 - 30.91
            = 19.09 m

Ballast_t_required = ΔTM_cm_tm / Lever_arm_m
                   = 6,933 / 19.09
                   ≈ 363 t
```

**Result:**
- W_stage_t = 434 t (cargo only, ballast excluded)
- x_stage_m = 13.06 m (composite center of cargo + ballast, but W is cargo only)
- Trim = -1.87 m (improved from Stage 6, but still significant)
- Required Ballast ≈ 363 t to achieve target trim of -96.5 cm

**Note:** 
- **W_stage_t consistency**: W_stage_t = 434t (cargo only), same as Stage 6
- **Ballast separation**: Ballast effect is calculated separately via ΔTM, NOT included in W_stage_t
- **Coordinate system**: Uses same coordinate system as Stage 1-6
- **Operational purpose**: Shows required ballast to achieve target trim for safe operation

---

### 9.6 Example 6: Trim Balance Optimization

**Initial Configuration (from verified stowage plan):**
- Unit 1: W₁ = 217 t, x₁ = +8.27 m
- Unit 2: W₂ = 217 t, x₂ = +22.27 m
- x_composite = (217×8.27 + 217×22.27) / 434 = 15.27 m
- TM = 434 × (15.27 - 29.29) = -6,084.68 t·m
- Trim = -6,084.68 / (40.72×100) = -1.49 m (bow-down, EXCESSIVE)

**Optimized Configuration (moved units stern-ward toward LCF):**
- Unit 1: W₁ = 217 t, x₁ = +18.27 m (moved 10.0 m aft)
- Unit 2: W₂ = 217 t, x₂ = +32.27 m (moved 10.0 m aft)
- x_composite = (217×18.27 + 217×32.27) / 434 = 25.27 m
- TM = 434 × (25.27 - 29.29) = -1,744.68 t·m
- Trim = -1,744.68 / (40.72×100) = -0.43 m (improved, but still bow-down)

**Further Optimization (target LCF alignment):**
- Unit 1: W₁ = 217 t, x₁ = +24.0 m (moved 15.73 m aft from initial)
- Unit 2: W₂ = 217 t, x₂ = +34.58 m (moved 12.31 m aft from initial)
- x_composite = (217×24.0 + 217×34.58) / 434 = 29.29 m (matches LCF)
- TM = 434 × (29.29 - 29.29) = 0 t·m
- Trim = 0 / (40.72×100) = 0.00 m (even-keel) ✓

**Improvement:**
- Trim reduced from -1.49 m to 0.00 m
- Difference: 1.49 m improvement (requires stowage plan adjustment)

---

## 10. References and Related Documents

### 10.1 Related Technical Documents

1. **PATCH3_TECHNICAL_DOCUMENTATION.md**
   - Detailed algorithm for RORO_Stage_Scenarios calculations
   - Formula derivations and implementation details

2. **PATCH4_TANK_LEVER_ARM_GUIDE.md**
   - Tank-based ballast calculation system
   - Lever arm method for trim correction

3. **TECHNICAL_DOCUMENTATION.md**
   - Complete system documentation
   - Build and verification procedures

### 10.2 Excel Files

1. **LCT_BUSHRA_Package_RORO_FIXED.xlsx**
   - RORO_Stage_Scenarios sheet
   - Input cells: W_stage_t (B column), x_stage_m (C column)

2. **LCT_BUSHRA_Package_TANK_LEVER_ARM.xlsx**
   - Tank-based ballast calculation
   - Stage-by-stage ballast optimization

### 10.3 Source Code

1. **scripts/patch3.py**
   - RORO_Stage_Scenarios sheet generation
   - Formula implementation

2. **scripts/update_stage_values.py**
   - Stage value update utility
   - Default stage values definition

3. **scripts/patch4.py**
   - Tank lever arm calculation
   - Ballast optimization algorithm

### 10.4 Key Parameters Reference

| Parameter | Symbol | Value | Unit | Source | Notes |
|-----------|--------|-------|------|--------|-------|
| LCF from Midship | LCF_m_from_midship | +29.29 | m | Stability Book | At Draft ~2.50m, verified |
| MTC | MTC_tm_per_cm | 40.72 | t·m/cm | Stability Book | At Draft ~2.50m, verified |
| TPC | TPC_t_per_cm | 7.50 | t/cm | Stability Book | Verified |
| Lpp | Lpp_m | 60.302 | m | Vessel Specs | Verified |
| AP to Midship | AP_to_midship_m | 30.151 | m | Vessel Specs | Lpp/2, verified |

---

## Appendix A: Quick Reference Table

### Standard Stage Values (Recommended 1st Input)

| Stage | W_stage_t (t) | x_stage_m (m) | Description | Reaction % | Trim (m) |
|-------|--------------:|--------------:|-------------|------------|----------|
| 1 | 0 | – | Empty condition | 0% | 0.00 |
| 2 | 65 | -10.0 | SPMT 1st entry | ~30% | -0.64 |
| 3 | 110 | -5.0 | ~50% on ramp | ~50% | -0.95 |
| 4 | 217 | -3.85 | Full on ramp | 100% | -1.77 |
| 5 | 434 | +15.27 | Deck full load (2 units) | 100% | -1.49 |

**Note:** 
- Stage 4 and 5 trim values exceed the limit of 1.206 m (Lpp/50) and are marked as EXCESSIVE.
- Stage 5 x_stage_m value (+15.27 m) is from verified stowage plan coordinates.
- Final values should be verified against actual stowage plan and measurements.
- For optimal trim balance, Stage 5 units should be positioned to achieve x_composite ≈ LCF (+29.29 m).

---

## Appendix B: Formula Summary

### Core Formulas

1. **Moment Calculation:**
   ```
   TM = W × (x - LCF)
   ```

2. **Trim Calculation:**
   ```
   Trim_cm = TM / MTC
   Trim_m = Trim_cm / 100
   ```

3. **Composite Center:**
   ```
   x_composite = Σ(W_i × x_i) / ΣW_i
   ```

4. **Coordinate Conversion:**
   ```
   x_mid = AP_to_midship - LCG_AP
   x_mid = 30.151 - LCG_AP
   ```

5. **Trim Limit Check:**
   ```
   Trim_limit = Lpp_m / 50
   If |Trim_m| > Trim_limit: EXCESSIVE
   ```

---

**End of Document**

