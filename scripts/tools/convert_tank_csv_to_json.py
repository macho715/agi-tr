# -*- coding: utf-8 -*-
"""CSV 파일을 JSON으로 변환하는 스크립트"""
import csv
import json
import os
from pathlib import Path

def detect_encoding(file_path):
    """파일 인코딩 감지"""
    encodings = ['utf-8-sig', 'utf-8', 'cp949', 'euc-kr', 'latin-1', 'iso-8859-1']
    for enc in encodings:
        try:
            with open(file_path, 'r', encoding=enc) as f:
                f.read()
            return enc
        except (UnicodeDecodeError, UnicodeError):
            continue
    return None

def csv_to_json(csv_file, json_file):
    """CSV 파일을 JSON으로 변환"""
    encoding = detect_encoding(csv_file)
    if encoding is None:
        print(f"Warning: Could not detect encoding for {csv_file}, trying utf-8-sig")
        encoding = 'utf-8-sig'

    print(f"Reading {csv_file} with encoding: {encoding}")

    try:
        with open(csv_file, 'r', encoding=encoding, errors='ignore') as f:
            # CSV 읽기
            reader = csv.DictReader(f)
            data = list(reader)

            # JSON으로 저장
            with open(json_file, 'w', encoding='utf-8') as jf:
                json.dump(data, jf, ensure_ascii=False, indent=2)

            print(f"Successfully converted {csv_file} to {json_file}")
            print(f"  Rows: {len(data)}")
            if data:
                print(f"  Columns: {list(data[0].keys())}")
            return True
    except Exception as e:
        print(f"Error converting {csv_file}: {e}")
        return False

if __name__ == "__main__":
    base_dir = Path(__file__).parent
    data_dir = base_dir / "data"

    # 변환할 파일들
    files = [
        ("Tank 좌표.csv", "tank_coordinates.json"),
        ("Tank Capacity.csv", "tank_capacity.json")
    ]

    for csv_name, json_name in files:
        csv_path = data_dir / csv_name
        json_path = data_dir / json_name

        if csv_path.exists():
            csv_to_json(csv_path, json_path)
        else:
            print(f"File not found: {csv_path}")

