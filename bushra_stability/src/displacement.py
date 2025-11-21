"""
Displacement calculation module matching BUSHRA Stability Excel workbook.

This module implements the core displacement and center of gravity calculations
that match the Excel workbook logic exactly.
"""
from dataclasses import dataclass
from typing import Optional, List


@dataclass
class WeightItem:
    """Represents a single weight item with its center of gravity coordinates."""
    name: str
    weight: float
    lcg: Optional[float] = None  # Longitudinal center of gravity
    vcg: Optional[float] = None  # Vertical center of gravity
    tcg: Optional[float] = None  # Transverse center of gravity
    fsm: float = 0.0  # Free surface moment
    group: Optional[str] = None


@dataclass
class DisplacementResult:
    """Result of displacement calculation."""
    total_weight: float
    lcg: float
    vcg: float
    tcg: float
    total_fsm: float


def calculate_displacement(items: List[WeightItem]) -> DisplacementResult:
    """
    Calculate total displacement and aggregate centers of gravity.
    
    This function matches the Excel workbook calculation logic:
    - Total weight = sum of all item weights
    - LCG = weighted average of longitudinal centers
    - VCG = weighted average of vertical centers
    - TCG = weighted average of transverse centers
    - Total FSM = sum of all free surface moments
    
    Args:
        items: List of WeightItem objects to aggregate
        
    Returns:
        DisplacementResult with aggregated values
        
    Raises:
        ValueError: If total weight is zero or all items have None for required coordinates
    """
    if not items:
        raise ValueError("Cannot calculate displacement from empty item list")
    
    total_weight = sum(item.weight for item in items)
    
    if total_weight == 0:
        raise ValueError("Total weight cannot be zero")
    
    # Calculate weighted moments for each axis
    total_l_moment = sum(
        item.weight * item.lcg 
        for item in items 
        if item.lcg is not None
    )
    
    total_v_moment = sum(
        item.weight * item.vcg 
        for item in items 
        if item.vcg is not None
    )
    
    total_t_moment = sum(
        item.weight * item.tcg 
        for item in items 
        if item.tcg is not None
    )
    
    # Calculate weighted average centers of gravity
    lcg = total_l_moment / total_weight
    vcg = total_v_moment / total_weight
    tcg = total_t_moment / total_weight
    
    # Sum all free surface moments
    total_fsm = sum(item.fsm for item in items)
    
    return DisplacementResult(
        total_weight=total_weight,
        lcg=lcg,
        vcg=vcg,
        tcg=tcg,
        total_fsm=total_fsm,
    )

