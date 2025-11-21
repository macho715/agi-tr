# 탱크 데이터 관리 도구

이 디렉토리에는 탱크 데이터 분석 및 변환 도구가 포함되어 있습니다.

## 파일 설명

### `create_master_tanks_from_excel.py`
- **목적**: `Tank Capacity_Plan.xlsx` 파일을 표준 `master_tanks.csv` 형식으로 변환
- **사용법**:
  ```bash
  python scripts/tools/create_master_tanks_from_excel.py
  ```
- **출력**: `bushra_stability/data/master_tanks.csv`

### `compare_tank_data.py`
- **목적**: Excel 기준 master_tanks.csv와 scripts/special의 탱크 데이터 비교
- **사용법**:
  ```bash
  python scripts/tools/compare_tank_data.py
  ```

### 탱크 데이터 변환 스크립트 (루트에서 이동)
- **`convert_tank_coordinates_to_json.py`**: 탱크 좌표를 JSON으로 변환
- **`convert_tank_csv_to_json.py`**: 탱크 CSV를 JSON으로 변환
- **`convert_tank_data_to_json.py`**: 탱크 데이터를 JSON으로 변환
- **`convert_tank_excel_to_json.py`**: 탱크 Excel을 JSON으로 변환
- **`convert_tank_to_json_final.py`**: 탱크 데이터 최종 JSON 변환

**참고**: 이 스크립트들은 이전 버전의 변환 도구입니다. 최신 버전은 `convert_tanks_csv_to_json.py`를 사용하세요.

## 데이터 소스

- **원본**: `Tank Capacity_Plan.xlsx` (프로젝트 루트)
- **출력**: `bushra_stability/data/master_tanks.csv`

## 주의사항

- `Tank Capacity_Plan.xlsx`가 정확한 데이터 소스입니다
- master_tanks.csv 파일을 수정하려면 원본 Excel 파일을 수정하고 스크립트를 재실행하세요

