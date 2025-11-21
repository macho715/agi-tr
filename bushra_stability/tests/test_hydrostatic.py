"""
Tests for hydrostatic interpolation engine.
"""
import pytest
import numpy as np
import pandas as pd
from pathlib import Path
import tempfile
import os

import sys
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from hydrostatic import HydroEngine


@pytest.fixture
def sample_hydro_csv(tmp_path):
    """Create sample hydrostatics CSV file."""
    data = {
        "Displacement": [1000, 1000, 1500, 1500, 2000, 2000],
        "Trim": [0.0, 1.0, 0.0, 1.0, 0.0, 1.0],
        "Draft": [2.0, 2.1, 2.5, 2.6, 3.0, 3.1],
        "LCB": [10.0, 10.1, 10.5, 10.6, 11.0, 11.1],
        "KMT": [5.0, 5.1, 5.5, 5.6, 6.0, 6.1],
        "MTC": [100.0, 101.0, 150.0, 151.0, 200.0, 201.0],
    }
    df = pd.DataFrame(data)
    file_path = tmp_path / "hydrostatics.csv"
    df.to_csv(file_path, index=False)
    return file_path


@pytest.fixture
def sample_kn_csv(tmp_path):
    """Create sample KN table CSV file."""
    data = {
        "Displacement": [1000, 1000, 1500, 1500, 2000, 2000],
        "Trim": [0.0, 1.0, 0.0, 1.0, 0.0, 1.0],
        "Heel_0": [0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        "Heel_10": [1.0, 1.1, 1.5, 1.6, 2.0, 2.1],
        "Heel_20": [2.0, 2.1, 2.5, 2.6, 3.0, 3.1],
        "Heel_30": [3.0, 3.1, 3.5, 3.6, 4.0, 4.1],
        "Heel_40": [3.5, 3.6, 4.0, 4.1, 4.5, 4.6],
    }
    df = pd.DataFrame(data)
    file_path = tmp_path / "kn_table.csv"
    df.to_csv(file_path, index=False)
    return file_path


def test_hydro_engine_initialization(sample_hydro_csv, sample_kn_csv):
    """Test HydroEngine initialization."""
    engine = HydroEngine(sample_hydro_csv, sample_kn_csv)
    assert engine is not None
    assert len(engine._hydro_disps) > 0
    assert len(engine._hydro_trims) > 0
    assert len(engine._heel_deg) > 0


def test_mean_draft_interpolation(sample_hydro_csv, sample_kn_csv):
    """Test mean draft interpolation."""
    engine = HydroEngine(sample_hydro_csv, sample_kn_csv)
    
    # Test interpolation at known point
    draft = engine.mean_draft(1000.0, 0.0)
    assert abs(draft - 2.0) < 0.01
    
    # Test interpolation between points
    draft = engine.mean_draft(1250.0, 0.5)
    assert 2.0 < draft < 2.5


def test_lcb_interpolation(sample_hydro_csv, sample_kn_csv):
    """Test LCB interpolation."""
    engine = HydroEngine(sample_hydro_csv, sample_kn_csv)
    
    lcb = engine.LCB(1000.0, 0.0)
    assert abs(lcb - 10.0) < 0.01


def test_kmt_interpolation(sample_hydro_csv, sample_kn_csv):
    """Test KMT interpolation."""
    engine = HydroEngine(sample_hydro_csv, sample_kn_csv)
    
    kmt = engine.KMT(1000.0, 0.0)
    assert abs(kmt - 5.0) < 0.01


def test_mtc_interpolation(sample_hydro_csv, sample_kn_csv):
    """Test MTC interpolation."""
    engine = HydroEngine(sample_hydro_csv, sample_kn_csv)
    
    mtc = engine.MTC(1000.0, 0.0)
    assert abs(mtc - 100.0) < 0.01


def test_kn_interpolation(sample_hydro_csv, sample_kn_csv):
    """Test KN interpolation."""
    engine = HydroEngine(sample_hydro_csv, sample_kn_csv)
    
    # Test single point
    kn = engine.KN(1000.0, 10.0, 0.0)
    assert abs(kn - 1.0) < 0.1
    
    # Test curve
    kn_curve = engine.KN_curve(1000.0, [0, 10, 20, 30], 0.0)
    assert len(kn_curve) == 4
    assert 0 in kn_curve
    assert 10 in kn_curve


def test_kn_curve_clipping(sample_hydro_csv, sample_kn_csv):
    """Test KN curve clipping to valid heel range."""
    engine = HydroEngine(sample_hydro_csv, sample_kn_csv)
    
    # Request angles outside valid range
    kn_curve = engine.KN_curve(1000.0, [-10, 0, 10, 50], 0.0)
    # Should clip to valid range
    assert len(kn_curve) == 4


def test_displacement_range(sample_hydro_csv, sample_kn_csv):
    """Test displacement range property."""
    engine = HydroEngine(sample_hydro_csv, sample_kn_csv)
    
    disp_min, disp_max = engine.displacement_range
    assert disp_min <= 1000.0
    assert disp_max >= 2000.0


def test_trim_range(sample_hydro_csv, sample_kn_csv):
    """Test trim range property."""
    engine = HydroEngine(sample_hydro_csv, sample_kn_csv)
    
    trim_min, trim_max = engine.trim_range
    assert trim_min <= 0.0
    assert trim_max >= 1.0


def test_heel_angles_property(sample_hydro_csv, sample_kn_csv):
    """Test heel angles property."""
    engine = HydroEngine(sample_hydro_csv, sample_kn_csv)
    
    heels = engine.heel_angles_deg
    assert len(heels) > 0
    assert 0 in heels
    assert 10 in heels

