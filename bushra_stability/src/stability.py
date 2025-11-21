"""
Stability calculation module for GZ curves and trim calculations.

This module extends basic displacement calculations with:
- Trim iterative calculation
- GZ curve calculation
- KG correction with FSM
"""
from dataclasses import dataclass
from typing import Dict, List, Optional, Any
import numpy as np

try:
    from .displacement import DisplacementResult, WeightItem, calculate_displacement
    from .hydrostatic import HydroEngine
except ImportError:
    # Fallback for direct import (testing)
    from displacement import DisplacementResult, WeightItem, calculate_displacement
    from hydrostatic import HydroEngine


@dataclass
class StabilityResult(DisplacementResult):
    """Extended displacement result with stability calculations."""
    kg_corrected: float  # VCG corrected with FSM
    kmt: float  # Transverse metacentric height
    gm: float  # Metacentric height
    trim: float  # Trim in meters (positive = aft)
    draft_mean: float  # Mean draft
    draft_fwd: float  # Forward draft
    draft_aft: float  # Aft draft
    lcb: float  # Longitudinal center of buoyancy
    mtc: float  # Moment to change trim (t·m/cm)
    kn_curve: Dict[int, float]  # Heel angle (deg) -> KN (m)
    gz_curve: Dict[int, float]  # Heel angle (deg) -> GZ (m)
    trim_history: Optional[List[Dict[str, float]]] = None  # Trim iteration history


def calculate_trim_iterative(
    displacement: float,
    lcg: float,
    hydro: HydroEngine,
    iterations: int = 5,
    trim_limit_m: float = 2.0,
    convergence_tol: float = 0.001
) -> Dict[str, Any]:
    """
    Calculate trim iteratively using LCB and MTC with enhanced stability.
    
    Args:
        displacement: Total displacement in tons
        lcg: Longitudinal center of gravity in meters
        hydro: HydroEngine instance
        iterations: Number of trim iterations (increased default to 5)
        trim_limit_m: Maximum trim limit (safety check)
        convergence_tol: Convergence tolerance in meters (default: 1mm)
        
    Returns:
        Dictionary with trim, drafts, LCB, MTC, convergence status, and trim_history
        
    Raises:
        Warning: If trim exceeds limit or doesn't converge
    """
    trim = 0.0
    converged = False
    prev_trim = None
    trim_history = []  # Store iteration history
    
    for i in range(iterations):
        # Get LCB and MTC at current displacement and trim
        try:
            lcb = hydro.LCB(displacement, trim)
            mtc = hydro.MTC(displacement, trim)  # t·m/cm
        except Exception as e:
            print(f"[Warning] Hydrostatic interpolation failed at iter {i+1}: {e}")
            break
        
        # Validation checks
        if np.isnan(lcb) or np.isnan(mtc):
            print(f"[Warning] NaN detected at iter {i+1}: LCB={lcb}, MTC={mtc}")
            break
        
        if abs(mtc) < 1e-6:  # Avoid division by near-zero
            print(f"[Warning] MTC too small ({mtc:.6f}) at iter {i+1}")
            break
        
        # Calculate new trim: trim = Δ * (LCB - LCG) / (MTC / 100)
        # MTC in t·m/cm, so divide by 100 to get t·m/m
        new_trim = displacement * (lcb - lcg) / (mtc / 100.0)
        
        # Record iteration history
        trim_history.append({
            "iter": i + 1,
            "trim": float(trim),
            "LCB": float(lcb),
            "MTC": float(mtc),
            "new_trim": float(new_trim)
        })
        
        # Check trim limit
        if abs(new_trim) > trim_limit_m:
            print(f"[Warning] Trim {new_trim:.3f}m exceeds limit {trim_limit_m:.2f}m at iter {i+1}")
            # Use last valid trim
            new_trim = np.clip(new_trim, -trim_limit_m, trim_limit_m)
            trim = new_trim
            break
        
        # Check convergence
        if prev_trim is not None:
            delta = abs(new_trim - prev_trim)
            if delta < convergence_tol:
                converged = True
                trim = new_trim
                print(f"[Info] Trim converged at iter {i+1}: {trim:.4f}m (Δ={delta:.5f}m)")
                break
        
        prev_trim = trim
        trim = new_trim
    
    if not converged and iterations > 1:
        print(f"[Warning] Trim did not converge after {iterations} iterations: {trim:.4f}m")
    
    # Get final hydrostatic properties
    try:
        mean_draft = hydro.mean_draft(displacement, trim)
    except Exception as e:
        print(f"[Error] Failed to get mean draft: {e}")
        mean_draft = 0.0
    
    draft_fwd = mean_draft - trim / 2.0
    draft_aft = mean_draft + trim / 2.0
    
    return {
        "trim": trim,
        "draft_mean": mean_draft,
        "draft_fwd": draft_fwd,
        "draft_aft": draft_aft,
        "lcb": lcb if not np.isnan(lcb) else 0.0,
        "mtc": mtc if not np.isnan(mtc) else 0.0,
        "converged": converged,
        "iterations_used": i + 1 if 'i' in locals() else 0,
        "trim_history": trim_history,
    }


def calculate_gz_curve(
    displacement: float,
    kg_corrected: float,
    trim: float,
    heel_angles_deg: List[int],
    hydro: HydroEngine
) -> Dict[int, float]:
    """
    Calculate GZ (righting arm) curve.
    
    GZ = KN - KGc × sin(heel)
    
    Args:
        displacement: Total displacement in tons
        kg_corrected: Corrected vertical center of gravity (with FSM)
        trim: Trim in meters
        heel_angles_deg: List of heel angles in degrees
        hydro: HydroEngine instance
        
    Returns:
        Dictionary mapping heel angle (deg) to GZ (m)
    """
    # Get KN curve
    kn_curve = hydro.KN_curve(displacement, heel_angles_deg, trim)
    
    # Calculate GZ for each angle
    gz_curve = {}
    for heel_deg in heel_angles_deg:
        kn = kn_curve[heel_deg]
        heel_rad = np.deg2rad(heel_deg)
        gz = kn - kg_corrected * np.sin(heel_rad)
        gz_curve[heel_deg] = gz
    
    return gz_curve


def calculate_stability(
    items: List[WeightItem],
    hydro: HydroEngine,
    heel_angles_deg: Optional[List[int]] = None,
    trim_iterations: int = 3,
    trim_limit_m: float = 2.0
) -> StabilityResult:
    """
    Calculate full stability including GZ curve and trim.
    
    Args:
        items: List of WeightItem objects
        hydro: HydroEngine instance
        heel_angles_deg: List of heel angles for GZ curve (default: [0, 10, 20, 30, 40, 50, 60])
        trim_iterations: Number of trim iterations
        trim_limit_m: Maximum trim limit
        
    Returns:
        StabilityResult with all stability parameters
        
    Raises:
        ValueError: If displacement calculation fails
    """
    # Calculate basic displacement
    disp_result = calculate_displacement(items)
    
    # Default heel angles
    if heel_angles_deg is None:
        heel_angles_deg = [0, 10, 20, 30, 40, 50, 60]
    
    # Calculate KG corrected (VCG + FSM effect)
    kg_corrected = disp_result.vcg
    if disp_result.total_weight > 0:
        kg_corrected += disp_result.total_fsm / disp_result.total_weight
    
    # Calculate trim iteratively
    trim_data = calculate_trim_iterative(
        disp_result.total_weight,
        disp_result.lcg,
        hydro,
        iterations=trim_iterations,
        trim_limit_m=trim_limit_m
    )
    
    # Get KMT at final trim
    kmt = hydro.KMT(disp_result.total_weight, trim_data["trim"])
    
    # Calculate GM
    gm = kmt - kg_corrected
    
    # Calculate GZ curve
    kn_curve = hydro.KN_curve(
        disp_result.total_weight,
        heel_angles_deg,
        trim_data["trim"]
    )
    gz_curve = calculate_gz_curve(
        disp_result.total_weight,
        kg_corrected,
        trim_data["trim"],
        heel_angles_deg,
        hydro
    )
    
    return StabilityResult(
        total_weight=disp_result.total_weight,
        lcg=disp_result.lcg,
        vcg=disp_result.vcg,
        tcg=disp_result.tcg,
        total_fsm=disp_result.total_fsm,
        kg_corrected=kg_corrected,
        kmt=kmt,
        gm=gm,
        trim=trim_data["trim"],
        draft_mean=trim_data["draft_mean"],
        draft_fwd=trim_data["draft_fwd"],
        draft_aft=trim_data["draft_aft"],
        lcb=trim_data["lcb"],
        mtc=trim_data["mtc"],
        kn_curve=kn_curve,
        gz_curve=gz_curve,
        trim_history=trim_data.get("trim_history"),
    )

