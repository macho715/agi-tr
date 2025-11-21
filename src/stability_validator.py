"""
Stability Validation Module

Integrates bushra_stability for post-generation validation
- Reads RORO stages from generated Excel
- Calculates basic displacement
- Validates stability if hydro data available
- Checks IMO A.749 compliance
"""

from pathlib import Path
from typing import Dict, List, Any, Optional
import logging
import os

# Try to import bushra_stability modules
try:
    import sys
    # Add bushra_stability to path if needed
    bushra_path = Path(__file__).parent.parent / "bushra_stability"
    if bushra_path.exists() and str(bushra_path) not in sys.path:
        sys.path.insert(0, str(bushra_path))
    
    from bushra_stability.src.displacement import WeightItem, calculate_displacement
    from bushra_stability.src.stability import calculate_stability
    from bushra_stability.src.hydrostatic import HydroEngine
    from bushra_stability.src.imo_check import check_imo_compliance
    STABILITY_AVAILABLE = True
except ImportError as e:
    STABILITY_AVAILABLE = False
    logging.warning(f"[STABILITY] bushra_stability not available: {e}")


def read_stages_from_excel(
    excel_path: str, 
    sheet_name: str = "RORO_Stage_Scenarios"
) -> List[WeightItem]:
    """
    Read RORO stages from generated Excel and convert to WeightItem list
    
    Maps Excel columns:
        Column A (Stage name) → name
        Column C (W_stage_t) → weight
        Column D (x_stage_m) → lcg
        
    Note: VCG/TCG not available in RORO sheet, defaults used
    
    Args:
        excel_path: Path to generated Excel file
        sheet_name: Sheet name (default: RORO_Stage_Scenarios)
    
    Returns:
        List of WeightItem objects
    """
    import pandas as pd
    
    try:
        df = pd.read_excel(excel_path, sheet_name=sheet_name)
    except Exception as e:
        logging.error(f"[STABILITY] Failed to read Excel: {e}")
        return []
    
    # Find header row (contains "Stage" or similar)
    header_row = None
    for idx, row in df.iterrows():
        row_str = '|'.join(str(v) for v in row.values if pd.notna(v))
        if 'stage' in row_str.lower():
            header_row = idx
            break
    
    if header_row is None:
        logging.error(f"[STABILITY] Cannot find header row in {sheet_name}")
        return []
    
    # Read data rows
    items = []
    for idx in range(header_row + 1, len(df)):
        row = df.iloc[idx]
        
        # Get stage name (Column A or first column)
        stage_name = row.iloc[0] if len(row) > 0 else None
        if pd.isna(stage_name) or str(stage_name).strip() == "":
            break  # End of data
        
        # Get W_stage (Column C, index 2)
        w_stage = row.iloc[2] if len(row) > 2 else 0.0
        
        # Get x_stage (Column D, index 3)
        x_stage = row.iloc[3] if len(row) > 3 else None
        
        item = WeightItem(
            name=str(stage_name),
            weight=float(w_stage) if not pd.isna(w_stage) else 0.0,
            lcg=float(x_stage) if not pd.isna(x_stage) and x_stage is not None else None,
            vcg=None,  # Not available in RORO sheet
            tcg=0.0,   # Assume centerline
            fsm=0.0    # RORO stages don't have FSM
        )
        items.append(item)
    
    logging.info(f"[STABILITY] Read {len(items)} stages from {excel_path}")
    return items


def validate_stability(
    excel_path: str,
    hydro_csv: str = "data/hydrostatics.csv",
    kn_csv: str = "data/kn_table.csv"
) -> Dict[str, Any]:
    """
    Full stability validation with IMO checks
    
    Args:
        excel_path: Path to generated Excel file
        hydro_csv: Path to hydrostatics CSV (optional)
        kn_csv: Path to KN table CSV (optional)
    
    Returns:
        Dictionary with validation results:
        {
            "status": "OK" | "WARNING" | "FAIL" | "SKIP",
            "total_weight": float (if available),
            "lcg": float (if available),
            "gm": float (if hydro available),
            "gz_curve": Dict[int, float] (if hydro available),
            "imo_compliance": Dict (if hydro available),
            "warnings": List[str],
            "errors": List[str]
        }
    """
    if not STABILITY_AVAILABLE:
        return {
            "status": "SKIP",
            "message": "bushra_stability module not installed",
            "warnings": [],
            "errors": []
        }
    
    result = {
        "status": "OK",
        "warnings": [],
        "errors": []
    }
    
    try:
        # Step 1: Read stages
        logging.info("[STABILITY] Reading stages from Excel")
        items = read_stages_from_excel(excel_path)
        
        if not items:
            result["status"] = "SKIP"
            result["warnings"].append("No stages found in Excel")
            return result
        
        # Step 2: Basic displacement calculation
        logging.info("[STABILITY] Calculating displacement")
        disp_result = calculate_displacement(items)
        
        result["total_weight"] = disp_result.total_weight
        result["lcg"] = disp_result.lcg
        result["vcg"] = disp_result.vcg if disp_result.vcg else None
        result["tcg"] = disp_result.tcg
        
        logging.info(f"[STABILITY] Total Weight: {disp_result.total_weight:.1f}t")
        logging.info(f"[STABILITY] LCG: {disp_result.lcg:.2f}m")
        
        # Step 3: Stability calculation (if hydro data available)
        hydro_path = Path(hydro_csv)
        kn_path = Path(kn_csv)
        
        if hydro_path.exists() and kn_path.exists():
            logging.info("[STABILITY] Hydro data found, running stability calculations")
            
            try:
                hydro = HydroEngine(str(hydro_path), str(kn_path))
                stab_result = calculate_stability(items, hydro)
                
                result["gm"] = stab_result.gm
                result["trim"] = stab_result.trim
                result["draft_mean"] = stab_result.draft_mean
                result["gz_curve"] = stab_result.gz_curve
                
                logging.info(f"[STABILITY] GM: {stab_result.gm:.2f}m")
                logging.info(f"[STABILITY] Trim: {stab_result.trim:.2f}m")
                
                # Step 4: IMO validation
                logging.info("[STABILITY] Running IMO A.749 compliance check")
                imo = check_imo_compliance(stab_result)
                
                result["imo_compliance"] = {
                    "passed": imo.passed,
                    "area_30": imo.area_30,
                    "area_40": imo.area_40,
                    "gz_max": imo.gz_max,
                    "details": imo.details if hasattr(imo, 'details') else {}
                }
                
                if not imo.passed:
                    result["status"] = "FAIL"
                    result["errors"].append("IMO A.749 compliance FAILED")
                    logging.error("[STABILITY] IMO A.749 compliance FAILED")
                else:
                    logging.info("[STABILITY] ✓ IMO A.749 compliance PASSED")
                    
            except Exception as e:
                result["status"] = "WARNING"
                result["warnings"].append(f"Stability calculation failed: {e}")
                logging.warning(f"[STABILITY] Stability calc failed: {e}")
        else:
            result["warnings"].append(f"Hydro data not found, stability calc skipped")
            logging.info("[STABILITY] Hydro data missing, skipped advanced validation")
    
    except Exception as e:
        result["status"] = "FAIL"
        result["errors"].append(str(e))
        logging.error(f"[STABILITY] Validation failed: {e}")
    
    return result


def save_validation_report(
    result: Dict, 
    output_path: str = "stability_report.json"
):
    """
    Save validation result to JSON file
    
    Args:
        result: Validation result dictionary
        output_path: Output file path
    """
    import json
    
    try:
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
        logging.info(f"[STABILITY] Report saved: {output_path}")
    except Exception as e:
        logging.error(f"[STABILITY] Failed to save report: {e}")


if __name__ == "__main__":
    # Test module
    import sys
    
    logging.basicConfig(level=logging.INFO, format='%(message)s')
    
    print("=" * 60)
    print("Stability Validator Test")
    print("=" * 60)
    
    # Check if bushra_stability is available
    print(f"\nbushra_stability available: {STABILITY_AVAILABLE}")
    
    if not STABILITY_AVAILABLE:
        print("  [SKIP] Install bushra_stability to enable validation")
        sys.exit(0)
    
    # Test with most recent Excel file
    excel_files = list(Path(".").glob("LCT_BUSHRA_AGI_TR_Final_v3*.xlsx"))
    if excel_files:
        excel_file = sorted(excel_files, key=lambda x: x.stat().st_mtime)[-1]
        print(f"\n[Test] Validating: {excel_file.name}")
        
        result = validate_stability(str(excel_file))
        
        print(f"\nStatus: {result['status']}")
        print(f"Total Weight: {result.get('total_weight', 'N/A')} t")
        print(f"LCG: {result.get('lcg', 'N/A')} m")
        
        if 'gm' in result:
            print(f"GM: {result['gm']:.2f} m")
        
        if 'imo_compliance' in result:
            imo = result['imo_compliance']
            print(f"IMO A.749: {'✓ PASS' if imo['passed'] else '✗ FAIL'}")
        
        if result['warnings']:
            print("\nWarnings:")
            for w in result['warnings']:
                print(f"  - {w}")
        
        if result['errors']:
            print("\nErrors:")
            for e in result['errors']:
                print(f"  - {e}")
    else:
        print("\n[SKIP] No Excel file found for testing")
    
    print("\n" + "=" * 60)
