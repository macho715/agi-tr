# -*- coding: utf-8 -*-
"""탱크 좌표 데이터를 JSON으로 변환"""
import json
import csv
from io import StringIO
from pathlib import Path

# 제공된 CSV 데이터
csv_data = """Tank_Name,Fr_Start,Fr_End,Mid_Fr,X_LCG_m,Y_TCG_m,Z_VCG_m,Weight_MT,Volume_m3
DO.P,24,25,24.5,11.25,-6.25,-2.83,3.05,3.50
DO.S,24,25,24.5,11.25,6.25,-2.83,3.05,3.50
FODB1.C,22,27,24.5,12.29,0.00,-0.67,21.89,25.20
FODB1.P,22,27,24.5,12.30,-4.32,-0.74,13.77,15.80
FODB1.S,22,27,24.5,12.30,4.32,-0.74,13.77,15.80
FOW1.P,24,27,25.5,13.16,-6.25,-2.32,10.39,11.90
FOW1.S,24,27,25.5,13.16,6.25,-2.32,10.39,11.90
LRFO.P,27,33,30.0,19.50,-3.92,-1.91,154.89,178.00
LRFO.S,27,33,30.0,19.50,3.92,-1.91,154.89,178.00
FW1.P,6,21,13.5,5.98,-6.09,-3.13,23.16,23.20
FW1.S,6,21,13.5,5.98,6.09,-3.13,23.16,23.20
FW2.P,0,6,3.0,0.12,-4.69,-3.54,13.92,13.90
FW2.S,0,6,3.0,0.12,4.69,-3.54,13.92,13.90
FWCARGO1.P,43,48,45.5,42.75,-3.92,-1.91,148.35,148.40
FWCARGO1.S,43,48,45.5,42.75,3.92,-1.91,148.35,148.40
FWCARGO2.P,38,43,40.5,35.25,-3.92,-1.91,148.36,148.40
FWCARGO2.S,38,43,40.5,35.25,3.92,-1.91,148.36,148.40
FWB1.P,56,65,60.5,57.52,-2.38,-2.49,50.57,50.60
FWB1.S,56,65,60.5,57.52,2.38,-2.49,50.57,50.60
FWB2.P,48,53,50.5,50.04,-4.37,-2.06,109.98,110.00
FWB2.S,48,53,50.5,50.04,4.37,-2.06,109.98,110.00
CL.P,56,59,57.5,56.25,-4.75,-4.23,7.12,6.90
CL.S,56,59,57.5,56.25,4.75,-4.23,7.12,6.90
VOID3.P,33,38,35.5,27.75,-3.92,-1.91,152.08,148.40
VOID3.S,33,38,35.5,27.75,3.92,-1.91,152.08,148.40
SLUDGE.C,19,22,20.5,8.79,0.00,-1.08,5.42,6.20
SEWAGE.P,19,22,20.5,8.85,-4.11,-1.14,2.73,2.70"""

def convert_csv_to_json():
    """CSV 데이터를 JSON으로 변환"""
    # CSV 파싱
    reader = csv.DictReader(StringIO(csv_data))
    data = []

    for row in reader:
        # 숫자 필드 변환
        converted_row = {}
        for key, value in row.items():
            if key in ['Fr_Start', 'Fr_End', 'Mid_Fr', 'X_LCG_m', 'Y_TCG_m', 'Z_VCG_m', 'Weight_MT', 'Volume_m3']:
                try:
                    converted_row[key] = float(value) if value else None
                except (ValueError, TypeError):
                    converted_row[key] = value
            else:
                converted_row[key] = value
        data.append(converted_row)

    return data

if __name__ == "__main__":
    base_dir = Path(__file__).parent
    data_dir = base_dir / "data"
    data_dir.mkdir(exist_ok=True)

    # JSON 변환
    tank_data = convert_csv_to_json()

    # JSON 파일로 저장 (제목 포함)
    json_path = data_dir / "tank_coordinates.json"
    output = {
        "title": "Tank 좌표",
        "data": tank_data
    }

    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=2, default=str)

    print(f"Successfully converted tank coordinates data to JSON")
    print(f"  Output file: {json_path}")
    print(f"  Total tanks: {len(tank_data)}")
    print(f"  Columns: {list(tank_data[0].keys()) if tank_data else 'No data'}")
    print(f"\nFirst 3 records:")
    for i, tank in enumerate(tank_data[:3], 1):
        print(f"\n  [{i}] {tank['Tank_Name']}")
        print(f"      Frame: {tank['Fr_Start']}-{tank['Fr_End']} (Mid: {tank['Mid_Fr']})")
        print(f"      LCG: {tank['X_LCG_m']} m, TCG: {tank['Y_TCG_m']} m, VCG: {tank['Z_VCG_m']} m")
        print(f"      Weight: {tank['Weight_MT']} MT, Volume: {tank['Volume_m3']} m³")

