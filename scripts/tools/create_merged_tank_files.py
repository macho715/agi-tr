#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
병합된 탱크 데이터 파일 생성 (CSV 및 JSON)

사용자가 제공한 데이터를 기준으로:
1. master_tanks.csv 생성 (Type 필드 포함)
2. master_tanks.json 생성 (Type 필드 포함)
"""

import pandas as pd
import json
from pathlib import Path
import sys

# 프로젝트 루트를 경로에 추가
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

def create_merged_tank_files():
    """
    사용자가 제공한 데이터를 기준으로 CSV와 JSON 파일 생성
    """
    # 사용자가 제공한 데이터
    tank_data = [
        {"Tank_ID": "CL.P", "Type": "SW", "Capacity_m3": 6.9, "SG_Master": 1.025, "LCG_m": 56.25, "VCG_m": 4.225, "TCG_m": -4.75, "FSM_full_tm": 0.41, "Content": "SALT WATER (SpGr 1.025)", "Location": "Fr.56~59"},
        {"Tank_ID": "CL.S", "Type": "SW", "Capacity_m3": 6.9, "SG_Master": 1.025, "LCG_m": 56.25, "VCG_m": 4.225, "TCG_m": 4.75, "FSM_full_tm": 0.41, "Content": "SALT WATER (SpGr 1.025)", "Location": "Fr.56~59"},
        {"Tank_ID": "DO.P", "Type": "FUEL", "Capacity_m3": 3.5, "SG_Master": 0.87, "LCG_m": 11.251, "VCG_m": 2.825, "TCG_m": -6.247, "FSM_full_tm": 0.34, "Content": "FUEL OIL (SpGr 0.870)", "Location": "Fr.24~25"},
        {"Tank_ID": "DO.S", "Type": "FUEL", "Capacity_m3": 3.5, "SG_Master": 0.87, "LCG_m": 11.251, "VCG_m": 2.825, "TCG_m": 6.247, "FSM_full_tm": 0.34, "Content": "FUEL OIL (SpGr 0.870)", "Location": "Fr.24~25"},
        {"Tank_ID": "FODB1.C", "Type": "FUEL", "Capacity_m3": 25.2, "SG_Master": 0.87, "LCG_m": 12.287, "VCG_m": 0.669, "TCG_m": 0.0, "FSM_full_tm": 48.1, "Content": "FUEL OIL (SpGr 0.870)", "Location": "Fr.22~27"},
        {"Tank_ID": "FODB1.P", "Type": "FUEL", "Capacity_m3": 15.8, "SG_Master": 0.87, "LCG_m": 12.295, "VCG_m": 0.741, "TCG_m": -4.319, "FSM_full_tm": 23.21, "Content": "FUEL OIL (SpGr 0.870)", "Location": "Fr.22~27"},
        {"Tank_ID": "FODB1.S", "Type": "FUEL", "Capacity_m3": 15.8, "SG_Master": 0.87, "LCG_m": 12.295, "VCG_m": 0.741, "TCG_m": 4.319, "FSM_full_tm": 23.21, "Content": "FUEL OIL (SpGr 0.870)", "Location": "Fr.22~27"},
        {"Tank_ID": "FOW1.P", "Type": "FUEL", "Capacity_m3": 11.9, "SG_Master": 0.87, "LCG_m": 13.159, "VCG_m": 2.319, "TCG_m": -6.249, "FSM_full_tm": 1.04, "Content": "FUEL OIL (SpGr 0.870)", "Location": "Fr.24~27"},
        {"Tank_ID": "FOW1.S", "Type": "FUEL", "Capacity_m3": 11.9, "SG_Master": 0.87, "LCG_m": 13.159, "VCG_m": 2.319, "TCG_m": 6.249, "FSM_full_tm": 1.04, "Content": "FUEL OIL (SpGr 0.870)", "Location": "Fr.24~27"},
        {"Tank_ID": "FW1.P", "Type": "FW", "Capacity_m3": 23.2, "SG_Master": 1.0, "LCG_m": 5.982, "VCG_m": 3.125, "TCG_m": -6.094, "FSM_full_tm": 1.15, "Content": "FRESH WATER (SpGr 1.000)", "Location": "Fr.6~21"},
        {"Tank_ID": "FW1.S", "Type": "FW", "Capacity_m3": 23.2, "SG_Master": 1.0, "LCG_m": 5.982, "VCG_m": 3.125, "TCG_m": 6.094, "FSM_full_tm": 1.15, "Content": "FRESH WATER (SpGr 1.000)", "Location": "Fr.6~21"},
        {"Tank_ID": "FW2.P", "Type": "FW", "Capacity_m3": 13.9, "SG_Master": 1.0, "LCG_m": 0.119, "VCG_m": 3.543, "TCG_m": -4.686, "FSM_full_tm": 3.71, "Content": "FRESH WATER (SpGr 1.000)", "Location": "Fr.0~6"},
        {"Tank_ID": "FW2.S", "Type": "FW", "Capacity_m3": 13.9, "SG_Master": 1.0, "LCG_m": 0.119, "VCG_m": 3.543, "TCG_m": 4.686, "FSM_full_tm": 3.71, "Content": "FRESH WATER (SpGr 1.000)", "Location": "Fr.0~6"},
        {"Tank_ID": "FWB1.P", "Type": "FW", "Capacity_m3": 50.6, "SG_Master": 1.0, "LCG_m": 57.519, "VCG_m": 2.49, "TCG_m": -2.379, "FSM_full_tm": 74.26, "Content": "FRESH WATER (SpGr 1.000)", "Location": "Fr.56~FE"},
        {"Tank_ID": "FWB1.S", "Type": "FW", "Capacity_m3": 50.6, "SG_Master": 1.0, "LCG_m": 57.519, "VCG_m": 2.49, "TCG_m": 2.379, "FSM_full_tm": 74.26, "Content": "FRESH WATER (SpGr 1.000)", "Location": "Fr.56~FE"},
        {"Tank_ID": "FWB2.P", "Type": "FW", "Capacity_m3": 110.0, "SG_Master": 1.0, "LCG_m": 50.038, "VCG_m": 2.059, "TCG_m": -4.368, "FSM_full_tm": 72.01, "Content": "FRESH WATER (SpGr 1.000)", "Location": "Fr.48~53"},
        {"Tank_ID": "FWB2.S", "Type": "FW", "Capacity_m3": 110.0, "SG_Master": 1.0, "LCG_m": 50.038, "VCG_m": 2.059, "TCG_m": 4.368, "FSM_full_tm": 72.01, "Content": "FRESH WATER (SpGr 1.000)", "Location": "Fr.48~53"},
        {"Tank_ID": "FWCARGO1.P", "Type": "FW", "Capacity_m3": 148.4, "SG_Master": 1.0, "LCG_m": 42.75, "VCG_m": 1.909, "TCG_m": -3.921, "FSM_full_tm": 128.25, "Content": "FRESH WATER (SpGr 1.000)", "Location": "Fr.43~48"},
        {"Tank_ID": "FWCARGO1.S", "Type": "FW", "Capacity_m3": 148.4, "SG_Master": 1.0, "LCG_m": 42.75, "VCG_m": 1.909, "TCG_m": 3.921, "FSM_full_tm": 128.25, "Content": "FRESH WATER (SpGr 1.000)", "Location": "Fr.43~48"},
        {"Tank_ID": "FWCARGO2.P", "Type": "FW", "Capacity_m3": 148.4, "SG_Master": 1.0, "LCG_m": 35.25, "VCG_m": 1.909, "TCG_m": -3.921, "FSM_full_tm": 128.25, "Content": "FRESH WATER (SpGr 1.000)", "Location": "Fr.38~43"},
        {"Tank_ID": "FWCARGO2.S", "Type": "FW", "Capacity_m3": 148.4, "SG_Master": 1.0, "LCG_m": 35.25, "VCG_m": 1.909, "TCG_m": 3.921, "FSM_full_tm": 128.25, "Content": "FRESH WATER (SpGr 1.000)", "Location": "Fr.38~43"},
        {"Tank_ID": "LRFO.P", "Type": "FUEL", "Capacity_m3": 178.0, "SG_Master": 0.87, "LCG_m": 19.5, "VCG_m": 1.909, "TCG_m": -3.921, "FSM_full_tm": 133.89, "Content": "FUEL OIL (SpGr 0.870)", "Location": "Fr.27~33"},
        {"Tank_ID": "LRFO.S", "Type": "FUEL", "Capacity_m3": 178.0, "SG_Master": 0.87, "LCG_m": 19.5, "VCG_m": 1.909, "TCG_m": 3.921, "FSM_full_tm": 133.89, "Content": "FUEL OIL (SpGr 0.870)", "Location": "Fr.27~33"},
        {"Tank_ID": "SEWAGE.P", "Type": "SEWAGE", "Capacity_m3": 2.7, "SG_Master": 1.025, "LCG_m": 8.848, "VCG_m": 1.137, "TCG_m": -4.112, "FSM_full_tm": 2.39, "Content": "SEWAGE (SpGr 1.025)", "Location": "Fr.19~22"},
        {"Tank_ID": "SLUDGE.C", "Type": "SLUDGE", "Capacity_m3": 6.2, "SG_Master": 0.87, "LCG_m": 8.794, "VCG_m": 1.082, "TCG_m": 0.0, "FSM_full_tm": 15.2, "Content": "SLUDGE (SpGr 0.870)", "Location": "Fr.19~22"},
        {"Tank_ID": "VOID3.P", "Type": "SW", "Capacity_m3": 148.4, "SG_Master": 1.025, "LCG_m": 27.75, "VCG_m": 1.909, "TCG_m": -3.921, "FSM_full_tm": 131.46, "Content": "SALT WATER (SpGr 1.025)", "Location": "Fr.33~38"},
        {"Tank_ID": "VOID3.S", "Type": "SW", "Capacity_m3": 148.4, "SG_Master": 1.025, "LCG_m": 27.75, "VCG_m": 1.909, "TCG_m": 3.921, "FSM_full_tm": 131.46, "Content": "SALT WATER (SpGr 1.025)", "Location": "Fr.33~38"},
        {"Tank_ID": "VOIDDB1.C", "Type": "SW", "Capacity_m3": 32.6, "SG_Master": 1.025, "LCG_m": 51.786, "VCG_m": 0.571, "TCG_m": -0.02, "FSM_full_tm": 67.83, "Content": "SALT WATER (SpGr 1.025)", "Location": "Fr.48~56"},
        {"Tank_ID": "VOIDDB2.C", "Type": "SW", "Capacity_m3": 47.9, "SG_Master": 1.025, "LCG_m": 30.75, "VCG_m": 0.4, "TCG_m": 0.0, "FSM_full_tm": 20.45, "Content": "SALT WATER (SpGr 1.025)", "Location": "Fr.27~48"},
        {"Tank_ID": "VOIDDB4.P", "Type": "SW", "Capacity_m3": 2.3, "SG_Master": 1.025, "LCG_m": 9.783, "VCG_m": 1.423, "TCG_m": -6.137, "FSM_full_tm": 0.39, "Content": "SALT WATER (SpGr 1.025)", "Location": "Fr.21~24"},
        {"Tank_ID": "VOIDDB4.S", "Type": "SW", "Capacity_m3": 4.9, "SG_Master": 1.025, "LCG_m": 9.278, "VCG_m": 1.269, "TCG_m": 5.043, "FSM_full_tm": 8.19, "Content": "SALT WATER (SpGr 1.025)", "Location": "Fr.19~24"},
    ]
    
    # 프로젝트 루트 경로
    project_root = Path(__file__).parent.parent.parent
    output_dir = project_root / "bushra_stability" / "data"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # DataFrame 생성
    df = pd.DataFrame(tank_data)
    
    # 정렬 (Tank_ID 기준)
    df = df.sort_values('Tank_ID').reset_index(drop=True)
    
    print("=" * 80)
    print("병합된 탱크 데이터 파일 생성")
    print("=" * 80)
    print(f"\n총 탱크 수: {len(df)}")
    print(f"컬럼: {df.columns.tolist()}")
    
    # CSV 파일 저장
    csv_path = output_dir / "master_tanks.csv"
    df.to_csv(csv_path, index=False)
    print(f"\n✅ CSV 파일 생성 완료!")
    print(f"   경로: {csv_path}")
    print(f"   파일 크기: {csv_path.stat().st_size} bytes")
    
    # JSON 파일 저장
    json_path = output_dir / "master_tanks.json"
    save_to_json(df, json_path)
    print(f"\n✅ JSON 파일 생성 완료!")
    print(f"   경로: {json_path}")
    print(f"   파일 크기: {json_path.stat().st_size} bytes")
    
    # 데이터 통계
    print("\n📊 데이터 통계:")
    print(f"   - 총 탱크 수: {len(df)}")
    print(f"   - 탱크 타입: {df['Type'].value_counts().to_dict()}")
    print(f"   - Capacity_m3: {df['Capacity_m3'].min():.2f} ~ {df['Capacity_m3'].max():.2f} m³")
    print(f"   - SG_Master: {df['SG_Master'].min():.3f} ~ {df['SG_Master'].max():.3f}")
    
    # 샘플 데이터 출력
    print("\n📋 샘플 데이터 (처음 3개):")
    print(df.head(3).to_string(index=False))
    
    return df

def save_to_json(df: pd.DataFrame, json_path: Path):
    """
    DataFrame을 JSON 파일로 저장합니다.
    
    Args:
        df: 탱크 데이터 DataFrame
        json_path: 출력 JSON 파일 경로
    """
    # DataFrame을 딕셔너리 리스트로 변환
    tanks_data = df.fillna("").to_dict(orient='records')
    
    # 숫자 타입 컬럼은 숫자로 유지
    numeric_columns = ['Capacity_m3', 'SG_Master', 'LCG_m', 'VCG_m', 'TCG_m', 'FSM_full_tm']
    for tank in tanks_data:
        for col in numeric_columns:
            if col in tank and tank[col] != "":
                try:
                    tank[col] = float(tank[col])
                except (ValueError, TypeError):
                    pass
    
    # JSON 형식으로 변환
    json_data = {
        "metadata": {
            "source": "Tank Capacity_Plan.xlsx",
            "total_tanks": len(tanks_data),
            "format_version": "1.1",
            "description": "LCT BUSHRA 탱크 마스터 데이터 (Type 필드 포함)",
            "coordinate_system": {
                "LCG_reference": "AP",
                "TCG_reference": "CL_port",
                "VCG_reference": "keel",
                "TCG_convention": "negative=port, positive=starboard"
            },
            "tank_types": {
                "SW": "Salt Water",
                "FUEL": "Fuel Oil",
                "FW": "Fresh Water",
                "SEWAGE": "Sewage",
                "SLUDGE": "Sludge"
            }
        },
        "tanks": tanks_data
    }
    
    # JSON 파일 저장
    json_path.parent.mkdir(parents=True, exist_ok=True)
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(json_data, f, ensure_ascii=False, indent=2)

def verify_files(csv_path: Path, json_path: Path):
    """
    생성된 파일들을 검증합니다.
    
    Args:
        csv_path: CSV 파일 경로
        json_path: JSON 파일 경로
    """
    print("\n" + "=" * 80)
    print("파일 검증")
    print("=" * 80)
    
    # CSV 검증
    if csv_path.exists():
        df_csv = pd.read_csv(csv_path)
        print(f"\n✅ CSV 파일 읽기 성공: {len(df_csv)}개 탱크")
        print(f"   컬럼: {df_csv.columns.tolist()}")
        
        # 필수 컬럼 확인
        required_columns = ['Tank_ID', 'Type', 'Capacity_m3', 'SG_Master', 'LCG_m', 'VCG_m', 'TCG_m', 'FSM_full_tm']
        missing_columns = [col for col in required_columns if col not in df_csv.columns]
        if missing_columns:
            print(f"   ⚠️  누락된 컬럼: {missing_columns}")
        else:
            print(f"   ✅ 모든 필수 컬럼 존재")
    else:
        print(f"\n❌ CSV 파일을 찾을 수 없습니다: {csv_path}")
    
    # JSON 검증
    if json_path.exists():
        with open(json_path, 'r', encoding='utf-8') as f:
            json_data = json.load(f)
        print(f"\n✅ JSON 파일 읽기 성공")
        print(f"   총 탱크 수: {json_data['metadata']['total_tanks']}")
        print(f"   형식 버전: {json_data['metadata']['format_version']}")
        print(f"   좌표 시스템: {json_data['metadata'].get('coordinate_system', {})}")
        print(f"   탱크 타입: {json_data['metadata'].get('tank_types', {})}")
    else:
        print(f"\n❌ JSON 파일을 찾을 수 없습니다: {json_path}")

def main():
    """메인 실행 함수"""
    # 프로젝트 루트 경로
    project_root = Path(__file__).parent.parent.parent
    output_dir = project_root / "bushra_stability" / "data"
    
    # 파일 생성
    df = create_merged_tank_files()
    
    # 파일 검증
    csv_path = output_dir / "master_tanks.csv"
    json_path = output_dir / "master_tanks.json"
    verify_files(csv_path, json_path)
    
    print("\n" + "=" * 80)
    print("✅ 파일 생성 및 검증 완료!")
    print("=" * 80)
    print(f"\n생성된 파일:")
    print(f"  - {csv_path}")
    print(f"  - {json_path}")

if __name__ == "__main__":
    main()

