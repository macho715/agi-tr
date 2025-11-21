"""
IMO A.749 stability criteria verification module.

This module implements IMO Resolution A.749(18) stability criteria checks
using Simpson integration for area calculations.
"""
from typing import Dict, Any, List
import numpy as np
try:
    from scipy.integrate import simpson as simps
except ImportError:
    # Fallback for older scipy versions
    try:
        from scipy.integrate import simps
    except ImportError:
        # Use numpy trapz as fallback
        from numpy import trapz as simps


def check_imo_a749(
    heel_angles_deg: List[float],
    gz_values_m: List[float],
    gm_m: float
) -> Dict[str, Any]:
    """
    Check IMO A.749 stability criteria.
    
    IMO A.749(18) Criteria:
    1. GM >= 0.15 m
    2. Area under GZ curve from 0° to 30° >= 0.055 m·rad
    3. Area under GZ curve from 0° to 40° >= 0.090 m·rad
    4. Area under GZ curve from 30° to 40° >= 0.030 m·rad
    5. GZ at 30° >= 0.20 m
    6. Maximum GZ >= 0.15 m
    7. Angle at maximum GZ > 15°
    
    Args:
        heel_angles_deg: List of heel angles in degrees
        gz_values_m: List of GZ values in meters (corresponding to heel angles)
        gm_m: Metacentric height in meters
        
    Returns:
        Dictionary with IMO check results
    """
    heels = np.array(heel_angles_deg, dtype=float)
    gz = np.array(gz_values_m, dtype=float)
    
    # Interpolate to 1° intervals (0° to 40°)
    fine_angles = np.arange(0.0, 41.0, 1.0)
    gz_interp = np.interp(fine_angles, heels, gz)
    
    # Convert to radians for integration
    fine_rad = np.deg2rad(fine_angles)
    
    # Calculate areas using Simpson integration
    # Note: simps/simpson expects (y, x) or (y, dx)
    area_0_30 = float(simps(gz_interp[:31], x=fine_rad[:31]))  # 0° to 30°
    area_0_40 = float(simps(gz_interp, x=fine_rad))  # 0° to 40°
    area_30_40 = float(simps(gz_interp[30:], x=fine_rad[30:]))  # 30° to 40°
    
    # Get GZ at 30°
    gz_30 = float(np.interp(30.0, heels, gz))
    
    # Get maximum GZ and angle
    gz_max = float(gz.max())
    angle_max = float(heels[np.argmax(gz)])
    
    # Perform checks
    checks = {
        "GM >= 0.15m": {
            "Value": round(gm_m, 2),
            "Required": 0.15,
            "Pass": gm_m >= 0.15
        },
        "Area 0-30 (m·rad)": {
            "Value": round(area_0_30, 3),
            "Required": 0.055,
            "Pass": area_0_30 >= 0.055
        },
        "Area 0-40 (m·rad)": {
            "Value": round(area_0_40, 3),
            "Required": 0.090,
            "Pass": area_0_40 >= 0.090
        },
        "Area 30-40 (m·rad)": {
            "Value": round(area_30_40, 3),
            "Required": 0.030,
            "Pass": area_30_40 >= 0.030
        },
        "GZ at 30° (m)": {
            "Value": round(gz_30, 2),
            "Required": 0.20,
            "Pass": gz_30 >= 0.20
        },
        "GZmax (m)": {
            "Value": round(gz_max, 2),
            "Required": 0.15,
            "Pass": gz_max >= 0.15
        },
        "Angle@GZmax (deg)": {
            "Value": round(angle_max, 1),
            "Required": 15.0,
            "Pass": angle_max > 15.0
        },
    }
    
    # Overall pass (all criteria must pass)
    checks["Overall_Pass"] = all(
        v["Pass"] for k, v in checks.items() if k != "Overall_Pass"
    )
    
    # Additional summary values
    checks["Area_0_30_mrad"] = round(area_0_30, 3)
    checks["Area_0_40_mrad"] = round(area_0_40, 3)
    checks["Area_30_40_mrad"] = round(area_30_40, 3)
    checks["GZ_30deg_m"] = round(gz_30, 3)
    checks["GZmax_m"] = round(gz_max, 3)
    checks["Angle_at_GZmax_deg"] = round(angle_max, 1)
    
    return checks

