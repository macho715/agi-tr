"""
Tests for stability calculation module.
"""
import pytest
import numpy as np
from pathlib import Path
import tempfile
import pandas as pd

import sys
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))

from displacement import WeightItem, calculate_displacement
from stability import calculate_stability, StabilityResult, calculate_trim_iterative, calculate_gz_curve
from hydrostatic import HydroEngine


@pytest.fixture
def sample_items():
    """Create sample weight items."""
    return [
        WeightItem(name="Light Ship", weight=770.16, lcg=26.35, vcg=3.88, tcg=0.0, fsm=0.0),
        WeightItem(name="Fuel Oil", weight=100.0, lcg=20.0, vcg=2.0, tcg=0.0, fsm=5.0),
        WeightItem(name="Fresh Water", weight=50.0, lcg=30.0, vcg=4.0, tcg=0.0, fsm=2.0),
    ]


@pytest.fixture
def sample_hydro_engine(tmp_path):
    """Create sample hydrostatic engine."""
    # Create hydrostatics CSV
    hydro_data = {
        "Displacement": [900, 900, 920, 920, 1000, 1000],
        "Trim": [0.0, 0.5, 0.0, 0.5, 0.0, 0.5],
        "Draft": [2.0, 2.1, 2.05, 2.15, 2.2, 2.3],
        "LCB": [26.0, 26.1, 26.2, 26.3, 26.5, 26.6],
        "KMT": [5.0, 5.1, 5.05, 5.15, 5.2, 5.3],
        "MTC": [100.0, 101.0, 102.0, 103.0, 105.0, 106.0],
    }
    hydro_df = pd.DataFrame(hydro_data)
    hydro_path = tmp_path / "hydro.csv"
    hydro_df.to_csv(hydro_path, index=False)
    
    # Create KN table CSV
    kn_data = {
        "Displacement": [900, 900, 920, 920, 1000, 1000],
        "Trim": [0.0, 0.5, 0.0, 0.5, 0.0, 0.5],
        "Heel_0": [0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        "Heel_10": [1.0, 1.05, 1.02, 1.07, 1.1, 1.15],
        "Heel_20": [2.0, 2.05, 2.02, 2.07, 2.1, 2.15],
        "Heel_30": [3.0, 3.05, 3.02, 3.07, 3.1, 3.15],
        "Heel_40": [3.5, 3.55, 3.52, 3.57, 3.6, 3.65],
    }
    kn_df = pd.DataFrame(kn_data)
    kn_path = tmp_path / "kn.csv"
    kn_df.to_csv(kn_path, index=False)
    
    return HydroEngine(hydro_path, kn_path)


def test_calculate_stability_basic(sample_items, sample_hydro_engine):
    """Test basic stability calculation."""
    result = calculate_stability(sample_items, sample_hydro_engine)
    
    assert isinstance(result, StabilityResult)
    assert result.total_weight > 0
    assert result.lcg is not None
    assert result.vcg is not None
    assert result.kg_corrected >= result.vcg  # KG corrected should be >= VCG (FSM effect)
    assert result.kmt > 0
    assert result.gm is not None
    assert len(result.kn_curve) > 0
    assert len(result.gz_curve) > 0


def test_kg_corrected_includes_fsm(sample_items, sample_hydro_engine):
    """Test that KG corrected includes FSM effect."""
    result = calculate_stability(sample_items, sample_hydro_engine)
    
    # KG corrected = VCG + FSM / displacement
    expected_kg = result.vcg + (result.total_fsm / result.total_weight)
    assert abs(result.kg_corrected - expected_kg) < 0.01


def test_gz_curve_calculation(sample_items, sample_hydro_engine):
    """Test GZ curve calculation."""
    result = calculate_stability(sample_items, sample_hydro_engine)
    
    # GZ should be calculated for all heel angles
    assert len(result.gz_curve) == len(result.kn_curve)
    
    # GZ at 0° should be 0 (or very close)
    if 0 in result.gz_curve:
        assert abs(result.gz_curve[0]) < 0.01
    
    # GZ should generally increase then decrease
    gz_values = [result.gz_curve[h] for h in sorted(result.gz_curve.keys())]
    # At least some positive GZ values
    assert any(gz > 0 for gz in gz_values)


def test_trim_calculation(sample_items, sample_hydro_engine):
    """Test trim calculation."""
    result = calculate_stability(sample_items, sample_hydro_engine)
    
    assert result.trim is not None
    assert result.draft_mean > 0
    assert result.draft_fwd > 0
    assert result.draft_aft > 0
    assert result.draft_aft >= result.draft_fwd  # Aft draft >= forward draft (trim positive = aft)


def test_gm_calculation(sample_items, sample_hydro_engine):
    """Test GM calculation."""
    result = calculate_stability(sample_items, sample_hydro_engine)
    
    # GM = KMT - KG corrected
    expected_gm = result.kmt - result.kg_corrected
    assert abs(result.gm - expected_gm) < 0.01


def test_trim_iterative(sample_hydro_engine):
    """Test iterative trim calculation."""
    # Test with known displacement and LCG
    trim_data = calculate_trim_iterative(
        displacement=920.0,
        lcg=26.2,
        hydro=sample_hydro_engine,
        iterations=3
    )
    
    assert "trim" in trim_data
    assert "draft_mean" in trim_data
    assert "draft_fwd" in trim_data
    assert "draft_aft" in trim_data
    assert "lcb" in trim_data
    assert "mtc" in trim_data


def test_gz_curve_function(sample_hydro_engine):
    """Test GZ curve calculation function."""
    # Calculate displacement first
    items = [
        WeightItem(name="Test", weight=920.0, lcg=26.2, vcg=3.5, tcg=0.0, fsm=0.0)
    ]
    disp_result = calculate_displacement(items)
    
    # Calculate GZ curve
    kg_corrected = disp_result.vcg  # No FSM
    trim = 0.0
    heel_angles = [0, 10, 20, 30, 40]
    
    gz_curve = calculate_gz_curve(
        displacement=disp_result.total_weight,
        kg_corrected=kg_corrected,
        trim=trim,
        heel_angles_deg=heel_angles,
        hydro=sample_hydro_engine
    )
    
    assert len(gz_curve) == len(heel_angles)
    for angle in heel_angles:
        assert angle in gz_curve


def test_stability_with_custom_heel_angles(sample_items, sample_hydro_engine):
    """Test stability calculation with custom heel angles."""
    custom_heels = [0, 15, 30, 45]
    result = calculate_stability(
        sample_items,
        sample_hydro_engine,
        heel_angles_deg=custom_heels
    )
    
    assert len(result.gz_curve) == len(custom_heels)
    for angle in custom_heels:
        assert angle in result.gz_curve


def test_trim_history_in_result(sample_items, sample_hydro_engine):
    """Test that trim_history is included in StabilityResult."""
    result = calculate_stability(sample_items, sample_hydro_engine)
    
    # trim_history should be available
    assert result.trim_history is not None
    assert isinstance(result.trim_history, list)
    assert len(result.trim_history) > 0
    
    # Each entry should have required fields
    for hist in result.trim_history:
        assert "iter" in hist
        assert "trim" in hist
        assert "LCB" in hist
        assert "MTC" in hist
        assert "new_trim" in hist
        assert isinstance(hist["iter"], int)
        assert isinstance(hist["trim"], (int, float))
        assert isinstance(hist["new_trim"], (int, float))


def test_trim_iterative_returns_history(sample_hydro_engine):
    """Test that calculate_trim_iterative returns trim_history."""
    trim_data = calculate_trim_iterative(
        displacement=920.0,
        lcg=26.2,
        hydro=sample_hydro_engine,
        iterations=5
    )
    
    assert "trim_history" in trim_data
    assert isinstance(trim_data["trim_history"], list)
    assert len(trim_data["trim_history"]) > 0
    
    # Check history structure
    for hist in trim_data["trim_history"]:
        assert "iter" in hist
        assert "trim" in hist
        assert "LCB" in hist
        assert "MTC" in hist
        assert "new_trim" in hist

