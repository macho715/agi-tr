"""
CSV file reader for master tanks and condition files.

This module reads CSV files in the standard format:
- master_tanks.csv: Tank master data
- tank_mapping.csv: Condition name to Tank_ID mapping
- condition_*.csv: Condition-specific tank fill percentages

See docs/USER_GUIDE.md for detailed CSV format specifications.
"""
from pathlib import Path
from typing import List, Optional, Dict
import pandas as pd

from .displacement import WeightItem


def read_master_tanks(master_path: Path) -> pd.DataFrame:
    """
    Read master tanks CSV file.
    
    Expected columns:
    - Tank_ID: Tank identifier
    - Capacity_m3: Tank capacity in cubic meters
    - SG_Master: Specific gravity (master value)
    - FSM_full_tm: Free surface moment when full (t·m)
    - LCG, LCG_m: Longitudinal center of gravity (m)
    - VCG, VCG_m: Vertical center of gravity (m)
    - TCG, TCG_m: Transverse center of gravity (m)
    
    Args:
        master_path: Path to master tanks CSV file
        
    Returns:
        DataFrame with master tank data
    """
    df = pd.read_csv(master_path)
    
    # Normalize column names
    if "LCG_m" not in df.columns and "LCG" in df.columns:
        df["LCG_m"] = df["LCG"]
    if "VCG_m" not in df.columns and "VCG" in df.columns:
        df["VCG_m"] = df["VCG"]
    if "TCG_m" not in df.columns and "TCG" in df.columns:
        df["TCG_m"] = df["TCG"]
    
    return df


def read_tank_mapping(mapping_path: Path) -> pd.DataFrame:
    """
    Read tank mapping CSV file.
    
    Expected columns:
    - Condition_Name: Condition name (matches condition CSV)
    - Tank_ID: Tank identifier (matches master CSV)
    
    Args:
        mapping_path: Path to tank mapping CSV file
        
    Returns:
        DataFrame with mapping data
    """
    df = pd.read_csv(mapping_path)
    
    # Normalize Tank_ID to string
    if "Tank_ID" in df.columns:
        df["Tank_ID"] = df["Tank_ID"].astype(str).str.strip()
    
    return df


def read_condition(condition_path: Path) -> pd.DataFrame:
    """
    Read condition CSV file.
    
    Expected columns:
    - Condition_Name: Condition name (matches mapping CSV)
    - Percent_Fill: Fill percentage (0-100)
    - SG_Override: Optional specific gravity override
    
    Args:
        condition_path: Path to condition CSV file
        
    Returns:
        DataFrame with condition data
    """
    df = pd.read_csv(condition_path)
    
    # Normalize Percent_Fill
    if "Percent_Fill" in df.columns:
        df["Percent_Fill"] = df["Percent_Fill"].fillna(0.0).clip(0, 100)
    
    return df


def apply_condition_to_master(
    master_df: pd.DataFrame,
    mapping_df: pd.DataFrame,
    condition_df: pd.DataFrame
) -> pd.DataFrame:
    """
    Apply condition to master tanks data.
    
    Args:
        master_df: Master tanks DataFrame
        mapping_df: Tank mapping DataFrame
        condition_df: Condition DataFrame
        
    Returns:
        Merged DataFrame with condition applied
    """
    # Normalize Tank_ID in all DataFrames
    for df in [master_df, mapping_df]:
        if "Tank_ID" in df.columns:
            df["Tank_ID"] = df["Tank_ID"].astype(str).str.strip()
    
    # Merge condition with mapping
    merged_cond = condition_df.merge(
        mapping_df,
        on="Condition_Name",
        how="left"
    )
    
    # Check for unmapped tanks
    if merged_cond["Tank_ID"].isnull().any():
        missing = merged_cond[merged_cond["Tank_ID"].isnull()]["Condition_Name"].unique()
        print(f"[Warning] Unmapped tanks: {missing}. (ignored)")
    
    # Merge with master
    final_df = master_df.merge(
        merged_cond,
        on="Tank_ID",
        how="left"
    )
    
    # Determine SG (override or master)
    if "SG_Override" in final_df.columns and "SG_Master" in final_df.columns:
        final_df["SG"] = final_df["SG_Override"].fillna(final_df["SG_Master"])
    elif "SG_Master" in final_df.columns:
        final_df["SG"] = final_df["SG_Master"]
    else:
        raise ValueError("SG_Master column not found in master data")
    
    # Ensure Percent_Fill
    if "Percent_Fill" not in final_df.columns:
        final_df["Percent_Fill"] = 0.0
    else:
        final_df["Percent_Fill"] = final_df["Percent_Fill"].fillna(0.0)
    
    return final_df


def calculate_fsm_effect(percent_fill: float, fsm_full: float) -> float:
    """
    Calculate effective FSM based on fill percentage.
    
    FSM is only effective when tank is partially filled (slack condition).
    Formula: FSM_eff = FSM_full * max(0, 1 - ((percent - 50) / 40)^2)
    
    Args:
        percent_fill: Fill percentage (0-100)
        fsm_full: Full FSM value (t·m)
        
    Returns:
        Effective FSM (t·m)
    """
    if percent_fill <= 10.0 or percent_fill >= 90.0:
        return 0.0
    
    x = (percent_fill - 50.0) / 40.0
    return fsm_full * max(0.0, 1.0 - x * x)


def csv_to_weight_items(
    master_path: Path,
    mapping_path: Path,
    condition_path: Path
) -> List[WeightItem]:
    """
    Convert CSV files to WeightItem list.
    
    Args:
        master_path: Path to master tanks CSV
        mapping_path: Path to tank mapping CSV
        condition_path: Path to condition CSV
        
    Returns:
        List of WeightItem objects
    """
    # Read all CSV files
    master_df = read_master_tanks(master_path)
    mapping_df = read_tank_mapping(mapping_path)
    condition_df = read_condition(condition_path)
    
    # Apply condition
    final_df = apply_condition_to_master(master_df, mapping_df, condition_df)
    
    # Convert to WeightItems
    items = []
    for _, row in final_df.iterrows():
        # Calculate weight
        if "Capacity_m3" in row and "Percent_Fill" in row and "SG" in row:
            weight = row["Capacity_m3"] * (row["Percent_Fill"] / 100.0) * row["SG"]
        else:
            weight = 0.0
        
        # Calculate FSM
        if "FSM_full_tm" in row and "Percent_Fill" in row:
            fsm = calculate_fsm_effect(row["Percent_Fill"], row["FSM_full_tm"])
        else:
            fsm = 0.0
        
        # Get coordinates
        lcg = row.get("LCG_m") if pd.notna(row.get("LCG_m")) else None
        vcg = row.get("VCG_m") if pd.notna(row.get("VCG_m")) else None
        tcg = row.get("TCG_m") if pd.notna(row.get("TCG_m")) else None
        
        # Get name
        name = str(row.get("Tank_ID", "Unknown"))
        if "Content" in row and pd.notna(row["Content"]):
            name = f"{name} ({row['Content']})"
        
        items.append(
            WeightItem(
                name=name,
                weight=weight,
                lcg=lcg,
                vcg=vcg,
                tcg=tcg,
                fsm=fsm,
                group=None,  # Can be set from Content column if needed
            )
        )
    
    return items

