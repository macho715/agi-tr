# -*- coding: utf-8 -*-
"""
Tank 좌표.csv와 Tank Capacity.csv를 JSON으로 변환
NASCA DRM 파일 형식 처리
"""
import json
import os
from pathlib import Path

def read_nasca_drm_file(file_path):
    """
    NASCA DRM 파일을 읽어서 구조화된 데이터로 변환
    파일이 바이너리 형식이므로, Excel에서 CSV로 내보낸 후 사용하거나
    실제 CSV 형식으로 변환된 파일이 필요합니다.
    """
    print(f"Attempting to read: {file_path}")

    # 여러 인코딩 시도
    encodings = ['utf-8-sig', 'utf-8', 'cp949', 'euc-kr', 'latin-1', 'iso-8859-1']

    for encoding in encodings:
        try:
            with open(file_path, 'r', encoding=encoding, errors='replace') as f:
                lines = f.readlines()

            # NASCA DRM 헤더 확인
            if lines and '<## NASCA DRM FILE' in lines[0]:
                print(f"  Detected NASCA DRM file format")
                print(f"  File appears to be binary/encrypted format")
                print(f"  Please export from Excel as CSV (UTF-8) first")
                return None

            # 일반 CSV로 처리 시도
            import csv
            from io import StringIO

            content = ''.join(lines)
            reader = csv.DictReader(StringIO(content))
            data = list(reader)

            if data and len(data[0]) > 1:  # 유효한 CSV 데이터
                print(f"  Successfully read as CSV (encoding: {encoding})")
                return data

        except Exception as e:
            continue

    return None

def create_sample_json_structure():
    """샘플 JSON 구조 생성 (실제 데이터가 없을 경우)"""
    tank_coordinates = {
        "description": "Tank 좌표 데이터",
        "note": "원본 파일이 NASCA DRM 바이너리 형식입니다. Excel에서 CSV로 내보낸 후 다시 시도하세요.",
        "expected_columns": [
            "TankName",
            "x_from_mid_m",
            "y_from_mid_m",
            "z_from_bottom_m",
            "max_t",
            "SG"
        ],
        "data": []
    }

    tank_capacity = {
        "description": "Tank Capacity 데이터",
        "note": "원본 파일이 NASCA DRM 바이너리 형식입니다. Excel에서 CSV로 내보낸 후 다시 시도하세요.",
        "expected_columns": [
            "TankName",
            "Capacity_m3",
            "MaxWeight_t"
        ],
        "data": []
    }

    return tank_coordinates, tank_capacity

if __name__ == "__main__":
    base_dir = Path(__file__).parent
    data_dir = base_dir / "data"

    # 파일 경로
    files = [
        (data_dir / "Tank 좌표.csv", data_dir / "tank_coordinates.json"),
        (data_dir / "Tank Capacity.csv", data_dir / "tank_capacity.json")
    ]

    for csv_path, json_path in files:
        print(f"\n{'='*60}")
        print(f"Processing: {csv_path.name}")
        print(f"{'='*60}")

        if not csv_path.exists():
            print(f"  ERROR: File not found: {csv_path}")
            continue

        # 파일 읽기 시도
        data = read_nasca_drm_file(csv_path)

        if data is None:
            print(f"  WARNING: Could not parse as standard CSV")
            print(f"  Creating template JSON structure...")

            if "좌표" in csv_path.name:
                tank_coords, _ = create_sample_json_structure()
                output_data = tank_coords
            else:
                _, tank_cap = create_sample_json_structure()
                output_data = tank_cap
        else:
            # 유효한 데이터가 있는 경우
            output_data = data
            print(f"  Successfully parsed {len(data)} rows")
            if data:
                print(f"  Columns: {list(data[0].keys())}")

        # JSON 저장
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, ensure_ascii=False, indent=2, default=str)

        print(f"  Saved to: {json_path}")

    print(f"\n{'='*60}")
    print("Conversion complete!")
    print(f"{'='*60}")
    print("\nNOTE: If files are NASCA DRM format, please:")
    print("  1. Open in Excel")
    print("  2. Save As -> CSV (UTF-8)")
    print("  3. Run this script again")

