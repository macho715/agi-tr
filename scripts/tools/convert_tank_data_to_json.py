# -*- coding: utf-8 -*-
"""제공된 탱크 데이터를 JSON으로 변환"""
import json
import csv
from io import StringIO
from pathlib import Path

# 제공된 CSV 데이터
csv_data = """Tank_Name,Location,Load_pct,Weight_MT,LCG_m,TCG_m,VCG_m,Volume_m3,Max_FSM_MT_m
DO.P,Fr.24-25,100.00,3.05,11.25f,6.25p,2.83,3.50,0.34
DO.S,Fr.24-25,100.00,3.05,11.25f,6.25s,2.83,3.50,0.34
FODB1.C,Fr.22-27,100.00,21.89,12.29f,0.00,0.67,25.20,48.10
FODB1.P,Fr.22-27,100.00,13.77,12.30f,4.32p,0.74,15.80,23.21
FODB1.S,Fr.22-27,100.00,13.77,12.30f,4.32s,0.74,15.80,23.21
FOW1.P,Fr.24-27,100.00,10.39,13.16f,6.25p,2.32,11.90,1.04
FOW1.S,Fr.24-27,100.00,10.39,13.16f,6.25s,2.32,11.90,1.04
LRFO.P,Fr.27-33,100.00,154.89,19.50f,3.92p,1.91,178.00,133.89
LRFO.S,Fr.27-33,100.00,154.89,19.50f,3.92s,1.91,178.00,133.89
FW1.P,Fr.6-21,100.00,23.16,5.98f,6.09p,3.13,23.20,1.15
FW1.S,Fr.6-21,100.00,23.16,5.98f,6.09s,3.13,23.20,1.15
FW2.P,Fr.0-6,100.00,13.92,0.12f,4.69p,3.54,13.90,3.71
FW2.S,Fr.0-6,100.00,13.92,0.12f,4.69s,3.54,13.90,3.71
FWCARGO1.P,Fr.43-48,100.00,148.35,42.75f,3.92p,1.91,148.40,128.25
FWCARGO1.S,Fr.43-48,100.00,148.35,42.75f,3.92s,1.91,148.40,128.25
FWCARGO2.P,Fr.38-43,100.00,148.36,35.25f,3.92p,1.91,148.40,128.25
FWCARGO2.S,Fr.38-43,100.00,148.36,35.25f,3.92s,1.91,148.40,128.25
FWB1.P,Fr.56-FE,100.00,50.57,57.52f,2.38p,2.49,50.60,74.26
FWB1.S,Fr.56-FE,100.00,50.57,57.52f,2.38s,2.49,50.60,74.26
FWB2.P,Fr.48-53,100.00,109.98,50.04f,4.37p,2.06,110.00,72.01
FWB2.S,Fr.48-53,100.00,109.98,50.04f,4.37s,2.06,110.00,72.01
CL.P,Fr.56-59,100.00,7.12,56.25f,4.75p,4.23,6.90,0.41
CL.S,Fr.56-59,100.00,7.12,56.25f,4.75s,4.23,6.90,0.41
VOID3.P,Fr.33-38,100.00,152.08,27.75f,3.92p,1.91,148.40,131.46
VOID3.S,Fr.33-38,100.00,152.08,27.75f,3.92s,1.91,148.40,131.46
SLUDGE.C,Fr.19-22,100.00,5.42,8.79f,0.00,1.08,6.20,15.20
SEWAGE.P,Fr.19-22,100.00,2.73,8.85f,4.11p,1.14,2.70,2.39"""

def convert_csv_to_json():
    """CSV 데이터를 JSON으로 변환"""
    # CSV 파싱
    reader = csv.DictReader(StringIO(csv_data))
    data = []

    for row in reader:
        # 숫자 필드 변환
        converted_row = {}
        for key, value in row.items():
            if key in ['Load_pct', 'Weight_MT', 'LCG_m', 'TCG_m', 'VCG_m', 'Volume_m3', 'Max_FSM_MT_m']:
                try:
                    # 'f', 'p', 's' 같은 접미사 제거 후 숫자 변환
                    if isinstance(value, str) and value:
                        # 숫자 부분만 추출
                        numeric_value = ''.join(c for c in value if c.isdigit() or c == '.' or c == '-')
                        if numeric_value:
                            converted_row[key] = float(numeric_value)
                        else:
                            converted_row[key] = value
                    else:
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

    # JSON 파일로 저장
    json_path = data_dir / "tank_data.json"
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(tank_data, f, ensure_ascii=False, indent=2, default=str)

    print(f"Successfully converted tank data to JSON")
    print(f"  Output file: {json_path}")
    print(f"  Total tanks: {len(tank_data)}")
    print(f"  Columns: {list(tank_data[0].keys()) if tank_data else 'No data'}")
    print(f"\nFirst 3 records:")
    for i, tank in enumerate(tank_data[:3], 1):
        print(f"\n  [{i}] {tank['Tank_Name']}")
        print(f"      Location: {tank['Location']}")
        print(f"      Weight: {tank['Weight_MT']} MT")
        print(f"      Volume: {tank['Volume_m3']} m³")

