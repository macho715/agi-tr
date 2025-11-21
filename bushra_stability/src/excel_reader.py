"""
Excel workbook reader for BUSHRA Stability Calculation.

This module reads data from the Excel workbook format and converts it
to Python data structures for calculation.
"""
from pathlib import Path
from typing import List, Optional
import pandas as pd
import math

from .displacement import WeightItem


def read_weight_items_from_excel(
    excel_path: Path, sheet_name: str = "Volum"
) -> List[WeightItem]:
    """
    Read weight items from Excel workbook Volum sheet.
    
    Args:
        excel_path: Path to the Excel workbook
        sheet_name: Name of the sheet to read (default: "Volum")
        
    Returns:
        List of WeightItem objects extracted from the workbook
    """
    df = pd.read_excel(excel_path, sheet_name=sheet_name, header=None)
    items = []
    current_group = None
    
    for _, row in df.iterrows():
        desc = row[2] if not pd.isna(row[2]) else row[1]
        
        # Skip header rows
        if isinstance(desc, str) and desc.strip() and row[7] == "Weight":
            continue
        
        # Detect group headers (rows with description but no weight)
        if isinstance(desc, str) and desc.strip():
            if pd.isna(row[7]) or (isinstance(row[7], str) and not row[7].strip()):
                current_group = desc.strip()
                continue
        
        # Extract weight item
        try:
            weight = float(row[7]) if not pd.isna(row[7]) else 0.0
        except (TypeError, ValueError):
            weight = None
        
        if weight is None or math.isnan(weight):
            # Still check if there's a valid name for zero-weight items with FSM
            name = desc.strip() if isinstance(desc, str) else str(desc)
            if not name or name.lower() == "nan":
                continue
            # Check if this might be a zero-weight item with FSM
            try:
                fsm = float(row[16]) if not pd.isna(row[16]) else 0.0
            except (TypeError, ValueError):
                fsm = 0.0
            if fsm > 0:
                weight = 0.0
            else:
                continue
        
        name = desc.strip() if isinstance(desc, str) else str(desc)
        if not name or name.lower() == "nan":
            continue
        
        # Skip subtotal and summary rows
        if "sub total" in name.lower() or name in {
            "Light Fixed Ship",
            "Displacement Condition",
        }:
            continue
        
        # Extract coordinates
        lcg = float(row[8]) if not pd.isna(row[8]) else None
        vcg = float(row[10]) if not pd.isna(row[10]) else None
        tcg = float(row[12]) if not pd.isna(row[12]) else None
        
        # Extract FSM
        try:
            fsm = float(row[16]) if not pd.isna(row[16]) else 0.0
        except (TypeError, ValueError):
            fsm = 0.0
        
        items.append(
            WeightItem(
                name=name,
                weight=weight,
                lcg=lcg,
                vcg=vcg,
                tcg=tcg,
                fsm=fsm,
                group=current_group,
            )
        )
    
    return items

