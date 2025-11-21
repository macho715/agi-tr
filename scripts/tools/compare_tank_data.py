#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tank Capacity Plan.xlsx 기준 master_tanks.csv와 scripts/special의 탱크 데이터 비교
"""

import pandas as pd
from pathlib import Path
import sys

# 프로젝트 루트를 경로에 추가
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

def compare_tank_data():
    """탱크 데이터 비교"""
    # Excel 기준 master_tanks.csv 읽기
    csv_path = project_root / 'bushra_stability' / 'data' / 'master_tanks.csv'
    excel_df = pd.read_csv(csv_path)
    
    # scripts/special에서 사용하는 탱크
    special_tanks = {
        'VOID3.P': {'LCG_AP': 27.750, 'VCG': 1.909, 'TCG': -3.921, 'Cap_m3': 148.4, 'Density': 1.025},
        'VOID3.S': {'LCG_AP': 27.750, 'VCG': 1.909, 'TCG': 3.921, 'Cap_m3': 148.4, 'Density': 1.025},
        'FW1.P': {'LCG_AP': 57.519, 'VCG': 2.490, 'TCG': -2.379, 'Cap_m3': 50.6, 'Density': 1.000},
        'FW1.S': {'LCG_AP': 57.519, 'VCG': 2.490, 'TCG': 2.379, 'Cap_m3': 50.6, 'Density': 1.000},
        'FW2.P': {'LCG_AP': 50.038, 'VCG': 2.059, 'TCG': -4.368, 'Cap_m3': 110.0, 'Density': 1.000},
        'FW2.S': {'LCG_AP': 50.038, 'VCG': 2.059, 'TCG': 4.368, 'Cap_m3': 110.0, 'Density': 1.000},
        'VOIDDB2.C': {'LCG_AP': 30.750, 'VCG': 0.400, 'TCG': 0.000, 'Cap_m3': 47.9, 'Density': 1.025},
        'FWCARGO2.P': {'LCG_AP': 35.250, 'VCG': 1.909, 'TCG': -3.921, 'Cap_m3': 148.4, 'Density': 1.000},
        'FWCARGO2.S': {'LCG_AP': 35.250, 'VCG': 1.909, 'TCG': 3.921, 'Cap_m3': 148.4, 'Density': 1.000},
        'SEWAGE.C': {'LCG_AP': 8.794, 'VCG': 1.082, 'TCG': 0.000, 'Cap_m3': 2.7, 'Density': 1.025},
        'D.O.P': {'LCG_AP': 11.251, 'VCG': 2.825, 'TCG': -6.247, 'Cap_m3': 3.5, 'Density': 0.820},
    }
    
    print("=" * 80)
    print("탱크 데이터 비교: Excel 기준 vs scripts/special")
    print("=" * 80)
    
    print(f"\nExcel 기준 master_tanks.csv: {len(excel_df)}개 탱크")
    print(f"scripts/special: {len(special_tanks)}개 탱크\n")
    
    # 비교
    differences = []
    matches = []
    missing = []
    
    for tank_id, special_data in special_tanks.items():
        if tank_id in excel_df['Tank_ID'].values:
            excel_row = excel_df[excel_df['Tank_ID'] == tank_id].iloc[0]
            
            # 값 비교
            diff_found = False
            diff_details = []
            
            # LCG 비교 (주의: scripts/special은 LCG_AP, Excel은 LCG_m)
            # scripts/special의 LCG_AP와 Excel의 LCG_m이 같은 값인지 확인
            excel_lcg = excel_row['LCG_m']
            special_lcg_ap = special_data['LCG_AP']
            if abs(excel_lcg - special_lcg_ap) > 0.001:
                diff_found = True
                diff_details.append(f"LCG: Excel={excel_lcg:.3f} vs Special_AP={special_lcg_ap:.3f}")
            
            # VCG 비교
            excel_vcg = excel_row['VCG_m']
            special_vcg = special_data['VCG']
            if abs(excel_vcg - special_vcg) > 0.001:
                diff_found = True
                diff_details.append(f"VCG: Excel={excel_vcg:.3f} vs Special={special_vcg:.3f}")
            
            # TCG 비교
            excel_tcg = excel_row['TCG_m']
            special_tcg = special_data['TCG']
            if abs(excel_tcg - special_tcg) > 0.001:
                diff_found = True
                diff_details.append(f"TCG: Excel={excel_tcg:.3f} vs Special={special_tcg:.3f}")
            
            # Capacity 비교
            excel_cap = excel_row['Capacity_m3']
            special_cap = special_data['Cap_m3']
            if abs(excel_cap - special_cap) > 0.01:
                diff_found = True
                diff_details.append(f"Capacity: Excel={excel_cap:.1f} vs Special={special_cap:.1f}")
            
            # SG/Density 비교
            excel_sg = excel_row['SG_Master']
            special_density = special_data['Density']
            if abs(excel_sg - special_density) > 0.001:
                diff_found = True
                diff_details.append(f"SG: Excel={excel_sg:.3f} vs Special={special_density:.3f}")
            
            if diff_found:
                differences.append({
                    'Tank_ID': tank_id,
                    'details': diff_details
                })
            else:
                matches.append(tank_id)
        else:
            missing.append(tank_id)
    
    # 결과 출력
    print(f"\n✅ 일치하는 탱크: {len(matches)}개")
    for tank_id in matches:
        print(f"   - {tank_id}")
    
    if differences:
        print(f"\n⚠️  차이가 있는 탱크: {len(differences)}개")
        for diff in differences:
            print(f"\n   {diff['Tank_ID']}:")
            for detail in diff['details']:
                print(f"     - {detail}")
    
    if missing:
        print(f"\n❌ Excel에 없는 탱크: {len(missing)}개")
        for tank_id in missing:
            print(f"   - {tank_id}")
    
    # Excel에만 있는 탱크
    excel_only = set(excel_df['Tank_ID'].values) - set(special_tanks.keys())
    if excel_only:
        print(f"\n📋 Excel에만 있는 탱크: {len(excel_only)}개")
        for tank_id in sorted(excel_only):
            print(f"   - {tank_id}")
    
    print("\n" + "=" * 80)
    print("비교 완료!")
    print("=" * 80)
    
    return {
        'matches': matches,
        'differences': differences,
        'missing': missing,
        'excel_only': list(excel_only)
    }

if __name__ == "__main__":
    compare_tank_data()

