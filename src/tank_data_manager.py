"""
Tank Data Management Module

Converts Tank Capacity_Plan.xlsx → tank_coordinates.json + tank_data.json
Integrated into agi tr.py pre-flight check for automatic JSON generation
"""

from pathlib import Path
import pandas as pd
import json
from typing import Dict, List, Tuple, Optional
import logging
import os

# Verified constants from BUSHRA_STABILITY_VALUES.md
AP_TO_MIDSHIP_M = 30.151  # Lpp/2, where Lpp = 60.302 m


def load_tank_capacity_plan(excel_path: str = "Tank Capacity_Plan.xlsx") -> Optional[pd.DataFrame]:
    """
    Load Tank Capacity Plan Excel
    
    Args:
        excel_path: Path to Tank Capacity_Plan.xlsx
    
    Returns:
        DataFrame with tank data, or None if failed
    """
    try:
        # Try different possible sheet names
        possible_sheets = ["Tank Data", "Tanks", "Sheet1", 0]
        
        for sheet in possible_sheets:
            try:
                df = pd.read_excel(excel_path, sheet_name=sheet)
                logging.info(f"[TANK] Loaded {len(df)} rows from {excel_path}, sheet: {sheet}")
                return df
            except:
                continue
        
        # If all failed, just load first sheet
        df = pd.read_excel(excel_path)
        logging.info(f"[TANK] Loaded {len(df)} rows from {excel_path} (default sheet)")
        return df
        
    except Exception as e:
        logging.error(f"[TANK] Failed to load Excel: {e}")
        return None


def parse_tank_dataframe(df: pd.DataFrame) -> List[Dict]:
    """
    Parse tank DataFrame and extract tank records
    
    Expected columns:
    - Tank_ID or Tank ID or similar
    - Capacity_m3 or Capacity or similar
    - SG_Master or SG or Density
    - LCG_m or LCG
    - VCG_m or VCG
    - TCG_m or TCG
    - FSM_full_tm or FSM
    
    Returns:
        List of tank dictionaries
    """
    # Find header row
    header_row = None
    for idx, row in df.iterrows():
        # Check if row contains column names
        row_str = '|'.join(str(v).lower() for v in row.values if pd.notna(v))
        if 'tank' in row_str and ('capacity' in row_str or 'lcg' in row_str):
            header_row = idx
            break
    
    if header_row is not None:
        df.columns = df.iloc[header_row]
        df = df[header_row + 1:]
    
    # Map column names (case-insensitive)
    col_map = {}
    for col in df.columns:
        col_lower = str(col).lower().replace(' ', '_')
        if 'tank' in col_lower and 'id' in col_lower:
            col_map['tank_id'] = col
        elif 'capacity' in col_lower:
            col_map['capacity_m3'] = col
        elif 'sg' in col_lower or 'density' in col_lower:
            col_map['sg_master'] = col
        elif 'lcg' in col_lower:
            col_map['lcg_m'] = col
        elif 'vcg' in col_lower:
            col_map['vcg_m'] = col
        elif 'tcg' in col_lower:
            col_map['tcg_m'] = col
        elif 'fsm' in col_lower:
            col_map['fsm_full_tm'] = col
    
    # Extract tanks
    tanks = []
    for idx, row in df.iterrows():
        try:
            tank_id = row[col_map.get('tank_id', df.columns[0])]
            if pd.isna(tank_id) or str(tank_id).strip() == '':
                continue
            
            tank = {
                'Tank_ID': str(tank_id).strip(),
                'Capacity_m3': float(row[col_map.get('capacity_m3', df.columns[1])]),
                'SG_Master': float(row[col_map.get('sg_master', df.columns[2])]),
                'LCG_m': float(row[col_map.get('lcg_m', df.columns[3])]),
                'VCG_m': float(row[col_map.get('vcg_m', df.columns[4])]),
                'TCG_m': float(row[col_map.get('tcg_m', df.columns[5])]),
                'FSM_full_tm': float(row[col_map.get('fsm_full_tm', df.columns[6])])
            }
            tanks.append(tank)
        except Exception as e:
            # Skip invalid rows
            continue
    
    logging.info(f"[TANK] Parsed {len(tanks)} valid tank records")
    return tanks


def generate_tank_coordinates_json(tanks: List[Dict]) -> Dict:
    """
    Generate tank_coordinates.json format
    
    Format:
    {
        "FWB1.P": {"lcg_m": 57.519, "vcg_m": X, "tcg_m": X},
        ...
    }
    """
    coordinates = {}
    for tank in tanks:
        tank_id = tank["Tank_ID"]
        coordinates[tank_id] = {
            "lcg_m": tank["LCG_m"],
            "vcg_m": tank["VCG_m"],
            "tcg_m": tank["TCG_m"]
        }
    return coordinates


def generate_tank_data_json(tanks: List[Dict]) -> Dict:
    """
    Generate tank_data.json format
    
    Format:
    {
        "FWB1.P": {
            "capacity_m3": 50.6,
            "sg_master": 1.025,
            "fsm_full_tm": X,
            "x_from_midship_m": 57.52
        },
        ...
    }
    """
    tank_data = {}
    
    for tank in tanks:
        tank_id = tank["Tank_ID"]
        lcg_ap = tank["LCG_m"]
        
        # Convert LCG from AP to midship coordinate
        # x_from_midship = AP_to_midship - LCG_AP
        x_from_midship = AP_TO_MIDSHIP_M - lcg_ap
        
        tank_data[tank_id] = {
            "capacity_m3": tank["Capacity_m3"],
            "sg_master": tank["SG_Master"],
            "fsm_full_tm": tank["FSM_full_tm"],
            "x_from_midship_m": round(x_from_midship, 2)
        }
    
    return tank_data


def ensure_tank_jsons(
    source_excel: str = "Tank Capacity_Plan.xlsx",
    output_dir: str = "data/"
) -> Tuple[bool, str]:
    """
    Ensure tank JSONs exist and are up-to-date
    
    Strategy:
    1. Check if Tank Capacity_Plan.xlsx exists
    2. Check if JSONs need regeneration (missing or outdated)
    3. Regenerate if needed
    
    Args:
        source_excel: Path to Tank Capacity_Plan.xlsx
        output_dir: Output directory for JSON files
    
    Returns:
        (success: bool, message: str)
    """
    coord_path = Path(output_dir) / "tank_coordinates.json"
    data_path = Path(output_dir) / "tank_data.json"
    excel_path = Path(source_excel)
    
    # Check if Excel exists
    if not excel_path.exists():
        return False, f"Source Excel not found: {source_excel}"
    
    # Check if JSONs need regeneration
    needs_regen = (
        not coord_path.exists() or 
        not data_path.exists() or
        excel_path.stat().st_mtime > coord_path.stat().st_mtime
    )
    
    if not needs_regen:
        logging.info("[TANK] JSONs up-to-date, skipping")
        return True, "Tank JSONs already up-to-date"
    
    # Regenerate
    logging.info(f"[TANK] Regenerating JSONs from {source_excel}")
    df = load_tank_capacity_plan(source_excel)
    
    if df is None:
        return False, "Failed to load Tank Capacity Plan Excel"
    
    tanks = parse_tank_dataframe(df)
    
    if not tanks:
        return False, "No valid tank data found in Excel"
    
    # Generate and save
    coordinates = generate_tank_coordinates_json(tanks)
    tank_data = generate_tank_data_json(tanks)
    
    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)
    
    with open(coord_path, "w", encoding="utf-8") as f:
        json.dump(coordinates, f, indent=2, ensure_ascii=False)
    
    with open(data_path, "w", encoding="utf-8") as f:
        json.dump(tank_data, f, indent=2, ensure_ascii=False)
    
    logging.info(f"[TANK] Generated {coord_path.name} ({len(coordinates)} tanks)")
    logging.info(f"[TANK] Generated {data_path.name} ({len(tank_data)} tanks)")
    
    return True, f"Generated {len(coordinates)} tank JSONs"


if __name__ == "__main__":
    # Test module
    import sys
    
    logging.basicConfig(level=logging.INFO)
    
    success, msg = ensure_tank_jsons()
    print(msg)
    
    if success:
        sys.exit(0)
    else:
        sys.exit(1)
