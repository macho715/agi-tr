#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tank Capacity Plan.xlsx를 기준으로 표준 master_tanks.csv 생성

이 스크립트는:
1. Tank Capacity_Plan.xlsx 파일을 읽어서 파싱
2. 표준 형식의 master_tanks.csv 파일 생성
3. bushra_stability/data/ 디렉토리에 저장
"""

import pandas as pd
import re
import sys
import json
from pathlib import Path

# 프로젝트 루트를 경로에 추가
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from scripts.tools.analyze_tank_capacity_plan import parse_lcg_value, parse_tcg_value

def create_standard_master_tanks(excel_path: str = None,
                                 output_dir: str = None,
                                 output_file: str = "master_tanks.csv"):
    """
    Excel 파일을 기준으로 표준 master_tanks.csv 파일을 생성합니다.
    
    Args:
        excel_path: Excel 파일 경로 (기본값: 프로젝트 루트의 Tank Capacity_Plan.xlsx)
        output_dir: 출력 디렉토리 (기본값: bushra_stability/data)
        output_file: 출력 파일명
    """
    # 프로젝트 루트 경로 (이미 상단에서 정의됨)
    project_root = Path(__file__).parent.parent.parent
    
    # 기본 경로 설정
    if excel_path is None:
        excel_path = project_root / "Tank Capacity_Plan.xlsx"
    else:
        excel_path = Path(excel_path)
        if not excel_path.is_absolute():
            excel_path = project_root / excel_path
    
    if output_dir is None:
        output_dir = project_root / "bushra_stability" / "data"
    else:
        output_dir = Path(output_dir)
        if not output_dir.is_absolute():
            output_dir = project_root / output_dir
    
    # 출력 디렉토리 생성
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    # Excel 파일 분석
    print("=" * 80)
    print("Tank Capacity Plan.xlsx → master_tanks.csv 변환")
    print("=" * 80)
    print(f"입력 파일: {excel_path}")
    print(f"출력 디렉토리: {output_path}")
    
    df = pd.read_excel(excel_path)
    
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
    
    # VCG 파싱
    if 'VCG_(m)' in df_clean.columns:
        df_clean['VCG_m'] = pd.to_numeric(df_clean['VCG_(m)'], errors='coerce')
    elif 'VCG\n(m)' in df_clean.columns:
        df_clean['VCG_m'] = pd.to_numeric(df_clean['VCG\n(m)'], errors='coerce')
    
    # 컬럼 매핑
    column_mapping = {
        'REF.CODE': 'Tank_ID',
        'Volume_(m3)': 'Capacity_m3',
        'Volume\n(m3)': 'Capacity_m3',
        'Weight (MT)': 'Weight_t',
        'Max FSM (MT-m)': 'FSM_full_tm',
        'Perm': 'Permeability',
        'Load (%)': 'Percent_Fill',
        'Tank Name': 'Content',
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
    
    # 표준 컬럼 선택 (필수 컬럼만)
    standard_columns = [
        'Tank_ID',
        'Capacity_m3',
        'SG_Master',
        'LCG_m',
        'VCG_m',
        'TCG_m',
        'FSM_full_tm',
    ]
    
    # 선택적 컬럼 추가
    optional_columns = ['Content', 'Location']
    for col in optional_columns:
        if col in df_clean.columns:
            standard_columns.append(col)
    
    # 존재하는 컬럼만 선택
    available_columns = [col for col in standard_columns if col in df_clean.columns]
    df_result = df_clean[available_columns].copy()
    
    # 데이터 타입 정리
    numeric_columns = ['Capacity_m3', 'SG_Master', 'LCG_m', 'VCG_m', 'TCG_m', 'FSM_full_tm']
    for col in numeric_columns:
        if col in df_result.columns:
            df_result[col] = pd.to_numeric(df_result[col], errors='coerce')
    
    # 정렬 (Tank_ID 기준)
    if 'Tank_ID' in df_result.columns:
        df_result = df_result.sort_values('Tank_ID').reset_index(drop=True)
    
    # CSV 저장
    output_file_path = output_path / output_file
    df_result.to_csv(output_file_path, index=False)
    
    print(f"\n✅ master_tanks.csv 생성 완료!")
    print(f"   경로: {output_file_path}")
    print(f"   총 탱크 수: {len(df_result)}")
    print(f"   컬럼: {df_result.columns.tolist()}")
    
    # JSON 저장
    json_file_path = output_path / output_file.replace('.csv', '.json')
    save_to_json(df_result, json_file_path)
    
    print(f"\n✅ master_tanks.json 생성 완료!")
    print(f"   경로: {json_file_path}")
    
    # 데이터 검증
    print("\n📊 데이터 검증:")
    print(f"   - Tank_ID: {df_result['Tank_ID'].nunique()}개 (고유값)")
    print(f"   - Capacity_m3: {df_result['Capacity_m3'].min():.2f} ~ {df_result['Capacity_m3'].max():.2f} m³")
    print(f"   - SG_Master: {df_result['SG_Master'].min():.3f} ~ {df_result['SG_Master'].max():.3f}")
    print(f"   - LCG_m: {df_result['LCG_m'].min():.3f} ~ {df_result['LCG_m'].max():.3f} m")
    print(f"   - VCG_m: {df_result['VCG_m'].min():.3f} ~ {df_result['VCG_m'].max():.3f} m")
    print(f"   - TCG_m: {df_result['TCG_m'].min():.3f} ~ {df_result['TCG_m'].max():.3f} m")
    print(f"   - FSM_full_tm: {df_result['FSM_full_tm'].min():.2f} ~ {df_result['FSM_full_tm'].max():.2f} t·m")
    
    # 누락 데이터 확인
    missing_data = df_result.isnull().sum()
    if missing_data.any():
        print("\n⚠️  누락 데이터:")
        for col, count in missing_data.items():
            if count > 0:
                print(f"   - {col}: {count}개")
    else:
        print("\n✅ 누락 데이터 없음")
    
    # 샘플 데이터 출력
    print("\n📋 샘플 데이터 (처음 5개):")
    print(df_result.head().to_string(index=False))
    
    return df_result

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
            "format_version": "1.0",
            "description": "LCT BUSHRA 탱크 마스터 데이터"
        },
        "tanks": tanks_data
    }
    
    # JSON 파일 저장
    json_path.parent.mkdir(parents=True, exist_ok=True)
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(json_data, f, ensure_ascii=False, indent=2)
    
    print(f"   파일 크기: {json_path.stat().st_size} bytes")

def verify_master_tanks_format(csv_path: str):
    """
    생성된 master_tanks.csv 파일이 올바른 형식인지 검증합니다.
    
    Args:
        csv_path: CSV 파일 경로
    """
    # 프로젝트 루트를 경로에 추가
    project_root = Path(__file__).parent.parent.parent
    sys.path.insert(0, str(project_root / "bushra_stability" / "src"))
    
    try:
        from csv_reader import read_master_tanks
    except ImportError:
        # 직접 읽기
        import pandas as pd
        def read_master_tanks(path):
            return pd.read_csv(path)
    
    print("\n" + "=" * 80)
    print("master_tanks.csv 형식 검증")
    print("=" * 80)
    
    try:
        df = read_master_tanks(Path(csv_path))
        print(f"\n✅ 파일 읽기 성공: {len(df)}개 탱크")
        
        # 필수 컬럼 확인
        required_columns = ['Tank_ID', 'Capacity_m3', 'SG_Master', 'LCG_m', 'VCG_m', 'TCG_m', 'FSM_full_tm']
        missing_columns = [col for col in required_columns if col not in df.columns]
        
        if missing_columns:
            print(f"\n❌ 누락된 필수 컬럼: {missing_columns}")
            return False
        else:
            print(f"\n✅ 모든 필수 컬럼 존재: {required_columns}")
        
        # 데이터 타입 확인
        print("\n📊 데이터 타입:")
        for col in required_columns:
            dtype = df[col].dtype
            null_count = df[col].isnull().sum()
            print(f"   - {col}: {dtype} (누락: {null_count}개)")
        
        return True
        
    except Exception as e:
        print(f"\n❌ 검증 실패: {e}")
        return False

def main():
    """메인 실행 함수"""
    # 프로젝트 루트 경로
    project_root = Path(__file__).parent.parent.parent
    excel_path = project_root / "Tank Capacity_Plan.xlsx"
    
    if not excel_path.exists():
        print(f"❌ 파일을 찾을 수 없습니다: {excel_path}")
        return
    
    # 표준 master_tanks.csv 생성
    df_result = create_standard_master_tanks(
        excel_path=str(excel_path),
        output_dir=str(project_root / "bushra_stability" / "data"),
        output_file="master_tanks.csv"
    )
    
    # 형식 검증
    csv_path = project_root / "bushra_stability" / "data" / "master_tanks.csv"
    if verify_master_tanks_format(str(csv_path)):
        print("\n" + "=" * 80)
        print("✅ master_tanks.csv 생성 및 검증 완료!")
        print("=" * 80)
        print(f"\n다음 단계:")
        print(f"  1. bushra_stability 코드에서 이 파일을 사용할 수 있습니다")
        print(f"  2. tank_mapping.csv 파일도 필요합니다")
        print(f"  3. condition_*.csv 파일로 탱크 채움 상태를 지정할 수 있습니다")
    else:
        print("\n" + "=" * 80)
        print("❌ 검증 실패 - 파일을 확인해주세요")
        print("=" * 80)

if __name__ == "__main__":
    main()

