#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Verify bridge: Excel → JSON using original workbook with Stage_Tanks"""

import sys
from pathlib import Path

# Add project root to Python path
script_dir = Path(__file__).parent
project_root = script_dir.parent
sys.path.insert(0, str(project_root))

from bushra_excel_bridge_v1 import stage_workbook_to_stability_json

# Paths (relative to script location)
master_tanks_path = project_root / "bushra_stability/data/master_tanks.json"
workbook_path = project_root / "LCT_BUSHRA_AGI_TR.xlsx"
verification_json = script_dir / "bushra_stability_verification.json"

print("=" * 80)
print("Bridge Verification: Excel → JSON")
print("=" * 80)
print(f"Input Excel: {workbook_path}")
print(f"Master tanks: {master_tanks_path}")
print(f"Output JSON: {verification_json}")
print()

try:
    result_json = stage_workbook_to_stability_json(
        workbook_path=workbook_path,
        master_tanks_path=master_tanks_path,
        out_json_path=verification_json
    )
    print(f"[OK] JSON verification created: {result_json}")
    print()
    print("=" * 80)
    print("[SUCCESS] Bridge verification complete!")
    print("=" * 80)
    
except Exception as e:
    print(f"[ERROR] {e}")
    import traceback
    traceback.print_exc()

