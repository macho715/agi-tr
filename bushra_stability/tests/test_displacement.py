"""
Test suite for displacement calculations matching BUSHRA Stability workbook.

These tests verify that Python implementation produces identical results
to the Excel workbook calculations.
"""
from typing import List
import sys
from pathlib import Path
import pytest

# Add src to Python path
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))

from displacement import (
    calculate_displacement,
    WeightItem,
    DisplacementResult,
)


# Test fixtures extracted from Excel workbook
@pytest.fixture
def light_ship_items() -> List[WeightItem]:
    """Light ship base items from PRINCIPAL PARTICULARS sheet."""
    return [
        WeightItem(name="Light Ship", weight=770.16, lcg=26.349, vcg=3.884, tcg=-0.004, fsm=0.0),
        WeightItem(name="Crew + Effects", weight=11.0, lcg=5.5, vcg=8.174, tcg=0.0, fsm=0.0),
        WeightItem(name="Deck Cargo 1", weight=431.1172, lcg=34.5, vcg=7.161, tcg=0.0, fsm=0.0),
    ]


@pytest.fixture
def fuel_oil_items() -> List[WeightItem]:
    """Fuel oil tank items from Volum sheet."""
    return [
        WeightItem(
            name="DAILY OIL TANK (P)",
            weight=0.82,
            lcg=11.251,
            vcg=2.825,
            tcg=-6.247,
            fsm=0.34,
            group="FUEL OIL (DENSITY - 0.821)",
        ),
        WeightItem(
            name="DAILY OIL TANK (S)",
            weight=0.82,
            lcg=11.251,
            vcg=2.825,
            tcg=6.247,
            fsm=0.34,
            group="FUEL OIL (DENSITY - 0.821)",
        ),
        WeightItem(
            name="NO.1 FO TANK (D.BTM-P)",
            weight=3.28,
            lcg=12.287,
            vcg=0.669,
            tcg=0.0,
            fsm=48.1,
            group="FUEL OIL (DENSITY - 0.821)",
        ),
        WeightItem(
            name="NO.1 FO TANK (D.BTM-S)",
            weight=3.28,
            lcg=12.295,
            vcg=0.741,
            tcg=-4.319,
            fsm=23.21,
            group="FUEL OIL (DENSITY - 0.821)",
        ),
        WeightItem(
            name="NO.1 FO TANK (D.BTM-C)",
            weight=1.64,
            lcg=12.295,
            vcg=0.741,
            tcg=4.319,
            fsm=23.21,
            group="FUEL OIL (DENSITY - 0.821)",
        ),
        WeightItem(
            name="NO.1 FO TANK (W-P)",
            weight=0.0,
            lcg=13.159,
            vcg=2.319,
            tcg=-6.249,
            fsm=1.04,
            group="FUEL OIL (DENSITY - 0.821)",
        ),
        WeightItem(
            name="NO.1 FO TANK (W-S)",
            weight=0.0,
            lcg=13.159,
            vcg=2.319,
            tcg=6.249,
            fsm=1.04,
            group="FUEL OIL (DENSITY - 0.821)",
        ),
        WeightItem(
            name="LONG RANGE FO TANK (P)",
            weight=18.6386,
            lcg=19.5,
            vcg=1.909,
            tcg=-3.921,
            fsm=133.89,
            group="FUEL OIL (DENSITY - 0.821)",
        ),
        WeightItem(
            name="LONG RANGE FO TANK (S)",
            weight=18.6386,
            lcg=19.5,
            vcg=1.909,
            tcg=3.921,
            fsm=133.89,
            group="FUEL OIL (DENSITY - 0.821)",
        ),
    ]


@pytest.fixture
def fresh_water_items() -> List[WeightItem]:
    """Fresh water tank items from Volum sheet."""
    return [
        WeightItem(
            name="NO. 1 FW TANK (P)",
            weight=17.0,
            lcg=5.982,
            vcg=3.125,
            tcg=-6.094,
            fsm=1.15,
            group="FRESH WATER (DENSITY - 1.00)",
        ),
        WeightItem(
            name="NO. 1 FW TANK (S)",
            weight=19.5,
            lcg=5.982,
            vcg=3.125,
            tcg=6.094,
            fsm=1.15,
            group="FRESH WATER (DENSITY - 1.00)",
        ),
        WeightItem(
            name="NO. 2 FW TANK (P)",
            weight=14.0,
            lcg=0.119,
            vcg=3.543,
            tcg=-4.686,
            fsm=3.71,
            group="FRESH WATER (DENSITY - 1.00)",
        ),
        WeightItem(
            name="NO. 2 FW TANK (S)",
            weight=14.0,
            lcg=0.119,
            vcg=3.543,
            tcg=4.686,
            fsm=3.71,
            group="FRESH WATER (DENSITY - 1.00)",
        ),
        WeightItem(
            name="NO. 2 FW CARGO TANK (P)",
            weight=113.6,
            lcg=35.25,
            vcg=1.909,
            tcg=-3.921,
            fsm=128.25,
            group="FRESH WATER (DENSITY - 1.00)",
        ),
        WeightItem(
            name="NO. 2 FW CARGO TANK (S)",
            weight=113.6,
            lcg=35.25,
            vcg=1.909,
            tcg=3.921,
            fsm=128.25,
            group="FRESH WATER (DENSITY - 1.00)",
        ),
    ]


@pytest.fixture
def all_items(
    light_ship_items, fuel_oil_items, fresh_water_items
) -> List[WeightItem]:
    """All items from the workbook matching Displacement Condition."""
    # Additional items to match workbook total
    additional = [
        WeightItem(
            name="NO. 1 FW BALLAST TANK (P)",
            weight=50.6,
            lcg=57.519,
            vcg=2.49,
            tcg=-2.379,
            fsm=74.26,
            group="FRESH WATER BALLAST",
        ),
        WeightItem(
            name="NO. 1 FW BALLAST TANK (S)",
            weight=50.6,
            lcg=57.519,
            vcg=2.49,
            tcg=2.379,
            fsm=74.26,
            group="FRESH WATER BALLAST",
        ),
        WeightItem(
            name="SLUDGE TANK (D.BTM-C)",
            weight=0.4698,
            lcg=8.794,
            vcg=1.082,
            tcg=0.0,
            fsm=15.2,
            group="MISCELLANEOUS",
        ),
        WeightItem(
            name="NO.1 VOID TANK (D.BTM-C)",
            weight=2.5625,
            lcg=51.74,
            vcg=0.569,
            tcg=0.0,
            fsm=69.17,
            group="MISCELLANEOUS",
        ),
        WeightItem(
            name="NO.2 VOID TANK (D.BTM-C)",
            weight=2.5625,
            lcg=30.75,
            vcg=0.4,
            tcg=0.0,
            fsm=20.45,
            group="MISCELLANEOUS",
        ),
        WeightItem(
            name="CL (P)",
            weight=0.41,
            lcg=56.25,
            vcg=4.225,
            tcg=-4.75,
            fsm=0.41,
            group="MISCELLANEOUS",
        ),
        WeightItem(
            name="CL (S)",
            weight=0.41,
            lcg=56.25,
            vcg=4.225,
            tcg=4.75,
            fsm=0.41,
            group="MISCELLANEOUS",
        ),
    ]
    return light_ship_items + fuel_oil_items + fresh_water_items + additional


class TestDisplacementCalculation:
    """Test displacement calculations match Excel workbook."""

    def test_light_ship_total(self, light_ship_items):
        """Test light ship items aggregate correctly."""
        result = calculate_displacement(light_ship_items)
        # Expected from Excel: Light Fixed Ship = 1212.2772 t
        assert abs(result.total_weight - 1212.2772) < 0.01
        # Expected LCG from Excel: 29.058527
        assert abs(result.lcg - 29.058527) < 0.0001
        # Expected VCG from Excel: 5.088313
        assert abs(result.vcg - 5.088313) < 0.0001
        # Expected TCG from Excel: -0.002541
        assert abs(result.tcg - (-0.002541)) < 0.0001

    def test_fuel_oil_subtotal(self, fuel_oil_items):
        """Test fuel oil items aggregate correctly."""
        result = calculate_displacement(fuel_oil_items)
        # Expected from Excel Volum sheet: Sub Total = 47.1172 t
        assert abs(result.total_weight - 47.1172) < 0.01
        # Expected LCG: 17.958406
        assert abs(result.lcg - 17.958406) < 0.0001
        # Expected VCG: 1.732599
        assert abs(result.vcg - 1.732599) < 0.0001
        # Expected TCG: -0.150331
        assert abs(result.tcg - (-0.150331)) < 0.0001
        # Expected FSM: 365.06
        assert abs(result.total_fsm - 365.06) < 0.01

    def test_fresh_water_subtotal(self, fresh_water_items):
        """Test fresh water items aggregate correctly."""
        result = calculate_displacement(fresh_water_items)
        # Expected from Excel: Sub Total = 291.7 t
        assert abs(result.total_weight - 291.7) < 0.01
        # Expected LCG: 28.215547
        assert abs(result.lcg - 28.215547) < 0.0001
        # Expected VCG: 2.218002
        assert abs(result.vcg - 2.218002) < 0.0001
        # Expected TCG: 0.052228
        assert abs(result.tcg - 0.052228) < 0.0001

    def test_displacement_condition_total(self, all_items):
        """Test complete displacement condition matches Excel workbook."""
        result = calculate_displacement(all_items)
        # Expected from Excel Print View: Displacement Condition
        # Weight: 1658.7092 t
        assert abs(result.total_weight - 1658.7092) < 0.01
        # LCG: 30.376737
        assert abs(result.lcg - 30.376737) < 0.0001
        # VCG: 4.313906
        assert abs(result.vcg - 4.313906) < 0.0001
        # TCG: 0.003057
        assert abs(result.tcg - 0.003057) < 0.0001
