#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tank Capacity Plan Excel 파일 분석 및 변환 스크립트

이 스크립트는 Tank Capacity_Plan.xlsx 파일을 읽어서:
1. 데이터 구조 분석
2. LCG/TCG 값 파싱 (f, p, s 접미사 제거)
3. 표준 CSV 형식으로 변환
4. 기존 코드베이스와 비교
"""

import pandas as pd
import re
from pathlib import Path
from typing import Dict, Optional

def parse_lcg_value(lcg_str: str) -> float:
    """
    LCG 값을 파싱합니다.
    예: '11.251f' -> 11.251, '5.982f' -> 5.982
    
    Args:
        lcg_str: LCG 문자열 (예: '11.251f', '57.519f')
        
    Returns:
        float: 파싱된 LCG 값
    """
    if pd.isna(lcg_str) or lcg_str == '':
        return None
    
    # 문자열로 변환
    lcg_str = str(lcg_str).strip()
    
    # 'f' 접미사 제거 (forward)
    lcg_str = re.sub(r'f$', '', lcg_str, flags=re.IGNORECASE)
    
    try:
        return float(lcg_str)
    except ValueError:
        print(f"[Warning] LCG 파싱 실패: {lcg_str}")
        return None

def parse_tcg_value(tcg_str: str) -> float:
    """
    TCG 값을 파싱합니다.
    예: '6.247p' -> -6.247 (port는 음수), '6.247s' -> 6.247 (starboard는 양수)
    
    Args:
        tcg_str: TCG 문자열 (예: '6.247p', '6.247s', '0')
        
    Returns:
        float: 파싱된 TCG 값 (port는 음수, starboard는 양수)
    """
    if pd.isna(tcg_str) or tcg_str == '' or tcg_str == 0:
        return 0.0
    
    # 문자열로 변환
    tcg_str = str(tcg_str).strip()
    
    # 숫자만 있는 경우
    if tcg_str.isdigit() or ('.' in tcg_str and tcg_str.replace('.', '').isdigit()):
        return float(tcg_str)
    
    # 'p' 접미사 (port = 음수)
    if 'p' in tcg_str.lower():
        tcg_str = re.sub(r'p$', '', tcg_str, flags=re.IGNORECASE)
        try:
            return -float(tcg_str)
        except ValueError:
            print(f"[Warning] TCG 파싱 실패: {tcg_str}")
            return 0.0
    
    # 's' 접미사 (starboard = 양수)
    if 's' in tcg_str.lower():
        tcg_str = re.sub(r's$', '', tcg_str, flags=re.IGNORECASE)
        try:
            return float(tcg_str)
        except ValueError:
            print(f"[Warning] TCG 파싱 실패: {tcg_str}")
            return 0.0
    
    # 접미사가 없는 경우
    try:
        return float(tcg_str)
    except ValueError:
        print(f"[Warning] TCG 파싱 실패: {tcg_str}")
        return 0.0

def analyze_tank_capacity_plan(excel_path: str) -> pd.DataFrame:
    """
    Tank Capacity Plan Excel 파일을 분석합니다.
    
    Args:
        excel_path: Excel 파일 경로
        
    Returns:
        pd.DataFrame: 정리된 탱크 데이터
    """
    # Excel 파일 읽기
    df = pd.read_excel(excel_path)
    
    print("=" * 80)
    print("Tank Capacity Plan 분석")
    print("=" * 80)
    print(f"\n원본 데이터 형태: {df.shape}")
    print(f"컬럼: {df.columns.tolist()}\n")
    
    # 컬럼명 정리
    df_clean = df.copy()
    df_clean.columns = df_clean.columns.str.replace('\n', '_').str.strip()
    
    # LCG 파싱
    if 'LCG_(m)' in df_clean.columns:
        df_clean['LCG_m'] = df_clean['LCG_(m)'].apply(parse_lcg_value)
    elif 'LCG\n(m)' in df_clean.columns:
        df_clean['LCG_m'] = df_clean['LCG\n(m)'].apply(parse_lcg_value)
    
    # TCG 파싱
    if 'TCG_(m)' in df_clean.columns:
        df_clean['TCG_m'] = df_clean['TCG_(m)'].apply(parse_tcg_value)
    elif 'TCG\n(m)' in df_clean.columns:
        df_clean['TCG_m'] = df_clean['TCG\n(m)'].apply(parse_tcg_value)
    
    # VCG 파싱 (이미 숫자일 수 있음)
    if 'VCG_(m)' in df_clean.columns:
        df_clean['VCG_m'] = pd.to_numeric(df_clean['VCG_(m)'], errors='coerce')
    elif 'VCG\n(m)' in df_clean.columns:
        df_clean['VCG_m'] = pd.to_numeric(df_clean['VCG\n(m)'], errors='coerce')
    
    # 컬럼명 매핑
    column_mapping = {
        'REF.CODE': 'Tank_ID',
        'Volume_(m3)': 'Capacity_m3',
        'Volume\n(m3)': 'Capacity_m3',
        'Weight (MT)': 'Weight_t',
        'Max FSM (MT-m)': 'FSM_full_tm',
        'Perm': 'Permeability',
        'Load (%)': 'Percent_Fill',
    }
    
    for old_col, new_col in column_mapping.items():
        if old_col in df_clean.columns:
            df_clean[new_col] = df_clean[old_col]
    
    # SG 계산 (Tank Name에서 추출)
    def extract_sg(tank_name: str) -> float:
        """Tank Name에서 SG 추출"""
        if pd.isna(tank_name):
            return None
        match = re.search(r'SpGr\s*([\d.]+)', str(tank_name))
        if match:
            return float(match.group(1))
        return None
    
    df_clean['SG_Master'] = df_clean['Tank Name'].apply(extract_sg)
    
    # 표준 컬럼 선택
    standard_columns = [
        'Tank_ID',
        'Tank Name',
        'Capacity_m3',
        'SG_Master',
        'LCG_m',
        'VCG_m',
        'TCG_m',
        'FSM_full_tm',
        'Weight_t',
        'Percent_Fill',
        'Permeability',
        'Location',
    ]
    
    # 존재하는 컬럼만 선택
    available_columns = [col for col in standard_columns if col in df_clean.columns]
    df_result = df_clean[available_columns].copy()
    
    # 데이터 타입 정리
    numeric_columns = ['Capacity_m3', 'SG_Master', 'LCG_m', 'VCG_m', 'TCG_m', 
                      'FSM_full_tm', 'Weight_t', 'Percent_Fill', 'Permeability']
    for col in numeric_columns:
        if col in df_result.columns:
            df_result[col] = pd.to_numeric(df_result[col], errors='coerce')
    
    print("\n정리된 데이터:")
    print(df_result.to_string())
    
    print("\n데이터 통계:")
    print(df_result.describe())
    
    return df_result

def compare_with_existing_data(cleaned_df: pd.DataFrame, 
                               master_tanks_path: Optional[str] = None):
    """
    기존 코드베이스의 탱크 데이터와 비교합니다.
    
    Args:
        cleaned_df: 정리된 탱크 데이터
        master_tanks_path: 기존 master_tanks.csv 파일 경로
    """
    if master_tanks_path and Path(master_tanks_path).exists():
        print("\n" + "=" * 80)
        print("기존 master_tanks.csv와 비교")
        print("=" * 80)
        
        existing_df = pd.read_csv(master_tanks_path)
        print(f"\n기존 데이터: {existing_df.shape}")
        print(f"새 데이터: {cleaned_df.shape}")
        
        # Tank_ID로 비교
        if 'Tank_ID' in cleaned_df.columns and 'Tank_ID' in existing_df.columns:
            common_tanks = set(cleaned_df['Tank_ID']) & set(existing_df['Tank_ID'])
            new_tanks = set(cleaned_df['Tank_ID']) - set(existing_df['Tank_ID'])
            missing_tanks = set(existing_df['Tank_ID']) - set(cleaned_df['Tank_ID'])
            
            print(f"\n공통 탱크: {len(common_tanks)}개")
            print(f"새로운 탱크: {len(new_tanks)}개")
            if new_tanks:
                print(f"  {sorted(new_tanks)}")
            print(f"누락된 탱크: {len(missing_tanks)}개")
            if missing_tanks:
                print(f"  {sorted(missing_tanks)}")
            
            # 공통 탱크의 값 비교
            if common_tanks:
                print("\n공통 탱크 값 비교:")
                for tank_id in sorted(common_tanks)[:5]:  # 처음 5개만
                    new_row = cleaned_df[cleaned_df['Tank_ID'] == tank_id].iloc[0]
                    existing_row = existing_df[existing_df['Tank_ID'] == tank_id].iloc[0]
                    
                    print(f"\n  {tank_id}:")
                    for col in ['Capacity_m3', 'LCG_m', 'VCG_m', 'TCG_m', 'FSM_full_tm']:
                        if col in new_row.index and col in existing_row.index:
                            new_val = new_row[col]
                            existing_val = existing_row[col]
                            if pd.notna(new_val) and pd.notna(existing_val):
                                diff = abs(new_val - existing_val)
                                status = "✓" if diff < 0.01 else "⚠"
                                print(f"    {col}: {new_val} vs {existing_val} (차이: {diff:.3f}) {status}")

def save_to_csv(cleaned_df: pd.DataFrame, output_path: str = "master_tanks_from_capacity_plan.csv"):
    """
    정리된 데이터를 CSV로 저장합니다.
    
    Args:
        cleaned_df: 정리된 탱크 데이터
        output_path: 출력 파일 경로
    """
    cleaned_df.to_csv(output_path, index=False)
    print(f"\n정리된 데이터가 {output_path}에 저장되었습니다.")

def main():
    """메인 실행 함수"""
    excel_path = "Tank Capacity_Plan.xlsx"
    
    if not Path(excel_path).exists():
        print(f"[Error] 파일을 찾을 수 없습니다: {excel_path}")
        return
    
    # Excel 파일 분석
    cleaned_df = analyze_tank_capacity_plan(excel_path)
    
    # 기존 데이터와 비교
    master_tanks_path = "bushra_stability/data/master_tanks.csv"
    if Path(master_tanks_path).exists():
        compare_with_existing_data(cleaned_df, master_tanks_path)
    
    # CSV로 저장
    save_to_csv(cleaned_df, "master_tanks_from_capacity_plan.csv")
    
    print("\n" + "=" * 80)
    print("분석 완료!")
    print("=" * 80)

if __name__ == "__main__":
    main()

