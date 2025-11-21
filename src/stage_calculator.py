"""
Stage W/X Calculator Module

Implements STAGE_W_X_ALGORITHM.md (952 lines)
- Composite center calculation (weighted average)
- Stage 6 (TR1 Final + TR2 on Ramp) calculation
- Verified coordinate system (Midship = 0, LCF = +29.29m)
"""

from typing import Dict, Optional, List, Tuple
from dataclasses import dataclass
import logging

# Verified constants from STAGE_W_X_ALGORITHM.md
LCF_FROM_MIDSHIP_M = 29.29  # m (@ Draft ~2.50m, verified from Stability Book)
AP_TO_MIDSHIP_M = 30.151    # m (Lpp/2, Lpp = 60.302m)


@dataclass
class StageData:
    """Single stage W/X data"""
    name: str
    W_stage_t: float
    x_stage_m: Optional[float]  # None for Stage 1 (empty)
    physical_meaning: str


def calculate_composite_center(units: List[Tuple[float, float]]) -> float:
    """
    Calculate weighted average composite center
    
    From STAGE_W_X_ALGORITHM.md Section 6.1
    Formula: x_composite = Σ(W_i × x_i) / ΣW_i
    
    Args:
        units: List of (weight_t, position_m) tuples
    
    Returns:
        x_composite in meters from midship
    
    Example:
        units = [(217, 8.27), (217, 22.27)]
        x_composite = 15.27m (verified from algorithm doc)
    
    Raises:
        ValueError: If units list is empty or total weight is zero
    """
    if not units:
        raise ValueError("Cannot calculate composite center from empty list")
    
    total_weight = sum(w for w, x in units)
    weighted_sum = sum(w * x for w, x in units)
    
    if total_weight == 0:
        raise ValueError("Total weight cannot be zero")
    
    x_composite = weighted_sum / total_weight
    
    logging.info(f"[STAGE] Composite center: {x_composite:.2f}m from {len(units)} units")
    return x_composite


def calculate_stage_6_composite() -> Tuple[float, float]:
    """
    Calculate Stage 6 (TR1 Final + TR2 on Ramp) composite center
    
    From STAGE_W_X_ALGORITHM.md Section 3.6 and Example 4
    
    Configuration:
        - TR1: At final position (Stage 5 composite)
        - TR2: On ramp (Stage 4 position)
    
    Returns:
        (W_stage_t, x_stage_m)
    
    Verified Values:
        - TR1: W=217t, x=+15.27m (Stage 5 final position)
        - TR2: W=217t, x=-3.85m (Stage 4 ramp position, VERIFIED)
        - Result: W=434t, x=+5.71m
    """
    # TR1 at final position (Stage 5)
    TR1_W = 217.0
    TR1_x = 15.27  # Verified Stage 5 composite position
    
    # TR2 on ramp (Stage 4 position)
    TR2_W = 217.0
    TR2_x = -3.85  # Verified Stage 4 ramp position (LCG_AP=34.0 → x=-3.85)
    
    x_composite = calculate_composite_center([(TR1_W, TR1_x), (TR2_W, TR2_x)])
    
    # Verify against expected value from algorithm doc
    expected_x = 5.71
    if abs(x_composite - expected_x) > 0.01:
        logging.warning(f"[STAGE] Stage 6 composite mismatch: calculated={x_composite:.2f}m, expected={expected_x}m")
    
    return 434.0, x_composite


def get_stage_defaults() -> Dict[str, StageData]:
    """
    Default stage values from STAGE_W_X_ALGORITHM.md
    
    Verified coordinate system:
    - Origin: Midship = 0 m
    - Positive x: Stern direction (aft of midship)
    - Negative x: Bow direction (forward of midship)
    - LCF: +29.29 m from midship (verified)
    
    Returns:
        Dictionary of stage name → StageData
    """
    return {
        "Stage 1": StageData(
            name="Stage 1",
            W_stage_t=0.0,
            x_stage_m=None,
            physical_meaning="Empty condition (baseline)"
        ),
        "Stage 2": StageData(
            name="Stage 2 (SPMT Entry)",
            W_stage_t=65.0,  # 30% × 217t
            x_stage_m=-10.0,  # Ramp entry (bow direction)
            physical_meaning="SPMT 1st entry on ramp (~30% reaction)"
        ),
        "Stage 3": StageData(
            name="Stage 3 (~50% on Ramp)",
            W_stage_t=110.0,  # 50% × 217t
            x_stage_m=-5.0,  # Mid-ramp
            physical_meaning="SPMT halfway on ramp (~50% reaction)"
        ),
        "Stage 4": StageData(
            name="Stage 4 (Full on Ramp)",
            W_stage_t=217.0,  # 100% × 217t
            x_stage_m=-3.85,  # VERIFIED: LCG_AP=34.0 → x=30.151-34.0=-3.85
            physical_meaning="Full unit weight on vessel (break-even)"
        ),
        "Stage 5": StageData(
            name="Stage 5 (Deck Full Load)",
            W_stage_t=434.0,  # 2 units (217t × 2)
            x_stage_m=15.27,  # VERIFIED composite center
            physical_meaning="Two units on deck (composite center)"
        ),
    }


def calculate_stages(
    pdf_path: Optional[str] = None,
    use_defaults: bool = True
) -> Dict[str, StageData]:
    """
    Main API: Calculate stage W/X values
    
    Strategy:
    1. Try PDF extraction (if path provided and PyMuPDF available) - FUTURE
    2. Fallback to verified defaults from algorithm doc
    
    Args:
        pdf_path: Optional path to PDF stowage plan (not implemented yet)
        use_defaults: Whether to use default values if PDF fails
    
    Returns:
        Dictionary of stage name → StageData
    
    Example:
        stages = calculate_stages()
        stage_5 = stages["Stage 5"]
        print(f"W={stage_5.W_stage_t}t, x={stage_5.x_stage_m}m")
    """
    # PDF extraction not implemented yet
    if pdf_path:
        logging.warning("[STAGE] PDF extraction not yet implemented, using defaults")
    
    # Use verified defaults
    if use_defaults:
        stages = get_stage_defaults()
        logging.info(f"[STAGE] Using {len(stages)} verified default stages")
        return stages
    
    raise ValueError("No stage data available (PDF not implemented and defaults disabled)")


def convert_to_roro_format(stages_dict: Dict[str, StageData]) -> Dict[str, Dict]:
    """
    Convert StageData dict to format expected by agi tr.py create_roro_sheet()
    
    Args:
        stages_dict: Dictionary of stage name → StageData
    
    Returns:
        Dictionary in format: {"Stage 1": {"W_stage_t": 0.0, "x_stage_m": None}, ...}
    """
    result = {}
    for stage_name, stage_data in stages_dict.items():
        result[stage_name] = {
            "W_stage_t": stage_data.W_stage_t,
            "x_stage_m": stage_data.x_stage_m
        }
    return result


if __name__ == "__main__":
    # Test module
    import sys
    
    logging.basicConfig(level=logging.INFO, format='%(message)s')
    
    print("=" * 60)
    print("Stage Calculator Test")
    print("=" * 60)
    
    # Test 1: Composite center (Example 3 from algorithm doc)
    print("\n[Test 1] Composite Center Calculation")
    units = [(217, 8.27), (217, 22.27)]
    x = calculate_composite_center(units)
    expected = 15.27
    print(f"  Units: {units}")
    print(f"  Result: {x:.2f}m")
    print(f"  Expected: {expected}m")
    print(f"  Status: {'✓ PASS' if abs(x - expected) < 0.01 else '✗ FAIL'}")
    
    # Test 2: Stage 6 calculation
    print("\n[Test 2] Stage 6 Composite")
    W, x = calculate_stage_6_composite()
    print(f"  TR1: 217t @ +15.27m")
    print(f"  TR2: 217t @ -3.85m")
    print(f"  Result: {W}t @ {x:.2f}m")
    print(f"  Expected: 434t @ 5.71m")
    print(f"  Status: {'✓ PASS' if abs(x - 5.71) < 0.01 else '✗ FAIL'}")
    
    # Test 3: Default stages
    print("\n[Test 3] Default Stages")
    stages = get_stage_defaults()
    for name, data in stages.items():
        x_str = f"{data.x_stage_m:.2f}m" if data.x_stage_m is not None else "None"
        print(f"  {name}: W={data.W_stage_t}t, x={x_str}")
    
    print("\n" + "=" * 60)
    print("All tests completed!")
    print("=" * 60)
