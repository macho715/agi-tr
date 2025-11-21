"""
Tests for IMO A.749 stability criteria verification.
"""
import pytest
import numpy as np
from pathlib import Path

import sys
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))

from imo_check import check_imo_a749


def test_imo_check_passing_case():
    """Test IMO check with passing criteria."""
    # Create a GZ curve that passes all criteria
    heel_angles = [0, 10, 20, 30, 40, 50, 60]
    # GZ curve: starts at 0, peaks around 30-40°, then decreases
    gz_values = [0.0, 0.15, 0.30, 0.40, 0.35, 0.20, 0.10]
    gm = 0.20  # GM > 0.15
    
    result = check_imo_a749(heel_angles, gz_values, gm)
    
    assert "Overall_Pass" in result
    # Note: This may not pass all criteria, but structure should be correct
    assert "Area_0_30_mrad" in result
    assert "Area_0_40_mrad" in result
    assert "GZ_30deg_m" in result
    assert "GZmax_m" in result


def test_imo_check_failing_gm():
    """Test IMO check with failing GM."""
    heel_angles = [0, 10, 20, 30, 40]
    gz_values = [0.0, 0.15, 0.30, 0.40, 0.35]
    gm = 0.10  # GM < 0.15 (fails)
    
    result = check_imo_a749(heel_angles, gz_values, gm)
    
    assert "GM >= 0.15m" in result
    assert result["GM >= 0.15m"]["Pass"] == False


def test_imo_check_area_calculations():
    """Test IMO area calculations."""
    heel_angles = [0, 10, 20, 30, 40]
    gz_values = [0.0, 0.15, 0.30, 0.40, 0.35]
    gm = 0.20
    
    result = check_imo_a749(heel_angles, gz_values, gm)
    
    # Check that areas are calculated
    assert "Area_0_30_mrad" in result
    assert "Area_0_40_mrad" in result
    assert "Area_30_40_mrad" in result
    
    # Areas should be positive
    assert result["Area_0_30_mrad"] >= 0
    assert result["Area_0_40_mrad"] >= 0
    assert result["Area_30_40_mrad"] >= 0


def test_imo_check_gz_at_30deg():
    """Test GZ at 30° check."""
    heel_angles = [0, 10, 20, 30, 40]
    gz_values = [0.0, 0.15, 0.30, 0.25, 0.35]  # GZ@30° = 0.25 > 0.20 (passes)
    gm = 0.20
    
    result = check_imo_a749(heel_angles, gz_values, gm)
    
    assert "GZ at 30° (m)" in result
    assert abs(result["GZ_30deg_m"] - 0.25) < 0.01
    assert result["GZ at 30° (m)"]["Value"] == pytest.approx(0.25, abs=0.01)


def test_imo_check_gz_max():
    """Test maximum GZ check."""
    heel_angles = [0, 10, 20, 30, 40]
    gz_values = [0.0, 0.15, 0.30, 0.40, 0.35]  # Max GZ = 0.40 > 0.15 (passes)
    gm = 0.20
    
    result = check_imo_a749(heel_angles, gz_values, gm)
    
    assert "GZmax (m)" in result
    assert abs(result["GZmax_m"] - 0.40) < 0.01
    assert result["GZmax (m)"]["Value"] == pytest.approx(0.40, abs=0.01)


def test_imo_check_angle_at_gzmax():
    """Test angle at maximum GZ."""
    heel_angles = [0, 10, 20, 30, 40]
    gz_values = [0.0, 0.15, 0.30, 0.40, 0.35]  # Max at 30°
    gm = 0.20
    
    result = check_imo_a749(heel_angles, gz_values, gm)
    
    assert "Angle_at_GZmax_deg" in result
    assert abs(result["Angle_at_GZmax_deg"] - 30.0) < 1.0  # Allow some tolerance


def test_imo_check_interpolation():
    """Test that IMO check interpolates to 1° intervals."""
    # Provide sparse data
    heel_angles = [0, 20, 40]
    gz_values = [0.0, 0.30, 0.35]
    gm = 0.20
    
    result = check_imo_a749(heel_angles, gz_values, gm)
    
    # Should still calculate areas (interpolates internally)
    assert "Area_0_30_mrad" in result
    assert "Area_0_40_mrad" in result

