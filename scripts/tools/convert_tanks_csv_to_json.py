#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
master_tanks.csv를 master_tanks.json으로 변환

이 스크립트는:
1. master_tanks.csv 파일을 읽어서
2. JSON 형식으로 변환
3. bushra_stability/data/master_tanks.json으로 저장
"""

import pandas as pd
import json
from pathlib import Path
import sys

# 프로젝트 루트를 경로에 추가
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

def convert_csv_to_json(csv_path: str = None, json_path: str = None):
    """
    CSV 파일을 JSON 파일로 변환합니다.
    
    Args:
        csv_path: 입력 CSV 파일 경로 (기본값: bushra_stability/data/master_tanks.csv)
        json_path: 출력 JSON 파일 경로 (기본값: bushra_stability/data/master_tanks.json)
    """
    # 프로젝트 루트 경로
    project_root = Path(__file__).parent.parent.parent
    
    # 기본 경로 설정
    if csv_path is None:
        csv_path = project_root / "bushra_stability" / "data" / "master_tanks.csv"
    else:
        csv_path = Path(csv_path)
        if not csv_path.is_absolute():
            csv_path = project_root / csv_path
    
    if json_path is None:
        json_path = project_root / "bushra_stability" / "data" / "master_tanks.json"
    else:
        json_path = Path(json_path)
        if not json_path.is_absolute():
            json_path = project_root / json_path
    
    # CSV 파일 읽기
    print("=" * 80)
    print("master_tanks.csv → master_tanks.json 변환")
    print("=" * 80)
    print(f"입력 파일: {csv_path}")
    print(f"출력 파일: {json_path}")
    
    if not csv_path.exists():
        print(f"❌ CSV 파일을 찾을 수 없습니다: {csv_path}")
        return None
    
    # CSV 읽기
    df = pd.read_csv(csv_path)
    print(f"\n✅ CSV 파일 읽기 성공: {len(df)}개 탱크")
    
    # DataFrame을 딕셔너리 리스트로 변환
    # NaN 값을 None으로 변환
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
    
    print(f"\n✅ JSON 파일 생성 완료: {json_path}")
    print(f"   파일 크기: {json_path.stat().st_size} bytes")
    
    # 데이터 검증
    print("\n📊 데이터 검증:")
    print(f"   - 총 탱크 수: {len(tanks_data)}")
    print(f"   - Tank_ID 목록: {[t['Tank_ID'] for t in tanks_data[:5]]}... (처음 5개)")
    
    # 샘플 데이터 출력
    if tanks_data:
        print("\n📋 샘플 데이터 (첫 번째 탱크):")
        sample = tanks_data[0]
        for key, value in sample.items():
            print(f"   {key}: {value}")
    
    return json_data

def verify_json_file(json_path: str):
    """
    JSON 파일이 올바른 형식인지 검증합니다.
    
    Args:
        json_path: JSON 파일 경로
    """
    print("\n" + "=" * 80)
    print("master_tanks.json 형식 검증")
    print("=" * 80)
    
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            json_data = json.load(f)
        
        print(f"\n✅ JSON 파일 읽기 성공")
        
        # 메타데이터 확인
        if "metadata" in json_data:
            metadata = json_data["metadata"]
            print(f"   - 소스: {metadata.get('source', 'N/A')}")
            print(f"   - 총 탱크 수: {metadata.get('total_tanks', 'N/A')}")
            print(f"   - 형식 버전: {metadata.get('format_version', 'N/A')}")
        
        # 탱크 데이터 확인
        if "tanks" in json_data:
            tanks = json_data["tanks"]
            print(f"   - 탱크 배열 길이: {len(tanks)}")
            
            if tanks:
                # 첫 번째 탱크의 필수 필드 확인
                first_tank = tanks[0]
                required_fields = ['Tank_ID', 'Capacity_m3', 'SG_Master', 'LCG_m', 'VCG_m', 'TCG_m', 'FSM_full_tm']
                missing_fields = [field for field in required_fields if field not in first_tank]
                
                if missing_fields:
                    print(f"   ⚠️  누락된 필수 필드: {missing_fields}")
                else:
                    print(f"   ✅ 모든 필수 필드 존재: {required_fields}")
        
        return True
        
    except json.JSONDecodeError as e:
        print(f"\n❌ JSON 파싱 오류: {e}")
        return False
    except Exception as e:
        print(f"\n❌ 검증 실패: {e}")
        return False

def main():
    """메인 실행 함수"""
    # 프로젝트 루트 경로
    project_root = Path(__file__).parent.parent.parent
    csv_path = project_root / "bushra_stability" / "data" / "master_tanks.csv"
    json_path = project_root / "bushra_stability" / "data" / "master_tanks.json"
    
    if not csv_path.exists():
        print(f"❌ CSV 파일을 찾을 수 없습니다: {csv_path}")
        print(f"\n다음 명령어로 CSV 파일을 먼저 생성하세요:")
        print(f"   python scripts/tools/create_master_tanks_from_excel.py")
        return
    
    # CSV → JSON 변환
    json_data = convert_csv_to_json(str(csv_path), str(json_path))
    
    if json_data:
        # 형식 검증
        if verify_json_file(str(json_path)):
            print("\n" + "=" * 80)
            print("✅ master_tanks.json 생성 및 검증 완료!")
            print("=" * 80)
            print(f"\nJSON 파일 위치: {json_path}")
            print(f"\n사용 방법:")
            print(f"  import json")
            print(f"  with open('bushra_stability/data/master_tanks.json', 'r', encoding='utf-8') as f:")
            print(f"      data = json.load(f)")
            print(f"      tanks = data['tanks']")
        else:
            print("\n" + "=" * 80)
            print("❌ 검증 실패 - 파일을 확인해주세요")
            print("=" * 80)

if __name__ == "__main__":
    main()

