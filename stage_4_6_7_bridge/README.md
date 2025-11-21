# Stage 4/6/7 Excel-Python Bridge 작업 파일

이 폴더는 **LCT BUSHRA AGI TR** 프로젝트의 Stage 4/6/7 Trim 값 설정 및 Python ↔ Excel ↔ Stability JSON 브리지 작업에 사용된 모든 파일을 포함합니다.

## 작업 목적

RORO 시트에서 Stage 4/6/7의 Trim 값을 읽어 JSON 설정 파일에 입력하고, Stage_Tanks 시트를 채운 후 브리지 함수를 실행하여 완전한 데이터 루프를 구축하는 작업입니다.

## 파일 설명

### 📄 설정 및 데이터 파일

| 파일명 | 설명 |
|--------|------|
| `stage_config_sample_4_7.json` | Stage 4/6/7 설정 파일<br>- Trim 초기값/목표값<br>- 각 Stage별 탱크 목록 및 Percent_Fill |
| `bushra_stability_verification.json` | Excel → JSON 변환 검증 결과 |
| `Stage_Tanks_template.xlsx` | Stage_Tanks 시트 템플릿<br>- Stage별 탱크 선택<br>- Percent_Fill, SG, UseForBallast 입력 |
| `bushra_stability_export.xlsx` | JSON → Excel 변환 최종 출력<br>- Tank_Coordinates<br>- Stage_Tank_Plan<br>- Stage_Tank_Sums<br>- Stage_Ballast |

### 🐍 Python 스크립트

| 파일명 | 용도 | 실행 순서 |
|--------|------|----------|
| `create_stage_tanks_sheet.py` | Stage_Tanks 시트 생성 (템플릿) | 1 |
| `fill_stage_tanks.py` | Stage_Tanks 시트에 탱크 데이터 채우기 | 2 |
| `update_stage_config_with_tanks.py` | Stage_Tanks 데이터를 JSON에 반영 | 3 |
| `add_stage_tanks_to_excel.py` | 원본 Excel에 Stage_Tanks 시트 추가 | (선택) |
| `run_bridge_tests.py` | 브리지 테스트 실행 (JSON → Excel) | 4 |
| `run_bridge_verification.py` | Excel → JSON 검증 | 5 |

### 📚 문서

| 파일명 | 내용 |
|--------|------|
| `FINAL_BRIDGE_EXECUTION_SUMMARY.md` | 최종 작업 완료 상세 요약 |
| `BRIDGE_EXECUTION_SUMMARY.md` | 초기 작업 요약 |

## Stage 4/6/7 설정 값

### Trim 값

| Stage | 초기 Trim (cm) | 목표 Trim (cm) | ΔTrim (cm) |
|-------|---------------|---------------|------------|
| Stage 4 | -181.89 | -121.0 | +60.89 |
| Stage 6 | -150.0 | -96.5 | +53.5 |
| Stage 7 | -120.0 | -84.34 | +35.66 |

### Ballast 계산 결과

| Stage | 필요 Ballast (t) | 탱크 무게 합계 (t) | FSM 합계 (t·m) |
|-------|-----------------|-------------------|---------------|
| Stage 4 | 182.19 | 272.83 | 134.20 |
| Stage 6 | 160.08 | 361.35 | 453.69 |
| Stage 7 | 106.70 | 301.25 | 486.96 |

### 탱크 구성

**Stage 4:**
- VOID3.P (80%, SG 1.025)
- VOID3.S (80%, SG 1.025)
- VOIDDB2.C (60%, SG 1.025)

**Stage 6:**
- VOID3.P (70%, SG 1.025)
- VOID3.S (70%, SG 1.025)
- FWCARGO1.P (50%, SG 1.0)
- FWCARGO1.S (50%, SG 1.0)

**Stage 7:**
- VOID3.P (60%, SG 1.025)
- VOID3.S (60%, SG 1.025)
- FWCARGO2.P (40%, SG 1.0)
- FWCARGO2.S (40%, SG 1.0)

## 작업 흐름

```
1. Excel RORO 시트에서 Stage 4 Trim 값 읽기
   ↓
2. stage_config_sample_4_7.json 생성 (Trim 값 입력)
   ↓
3. Stage_Tanks 시트 생성 및 채우기
   ↓
4. JSON에 탱크 데이터 반영
   ↓
5. export_tank_summaries_to_excel() 실행
   ↓
6. bushra_stability_export.xlsx 생성 완료
```

## 사용 방법

### 1. 설정 파일 수정 후 Excel 재생성

```bash
# 1. stage_config_sample_4_7.json 수정
# 2. 브리지 실행
python run_bridge_tests.py
```

### 2. Stage_Tanks 시트 수정 후 JSON 업데이트

```bash
# 1. Stage_Tanks_template.xlsx에서 탱크 선택 수정
# 2. JSON 업데이트
python update_stage_config_with_tanks.py
# 3. Excel 재생성
python run_bridge_tests.py
```

### 3. 원본 Excel에 Stage_Tanks 시트 추가

```bash
python add_stage_tanks_to_excel.py
```

## 외부 의존성

이 폴더의 스크립트는 다음 파일들을 참조합니다:

- **메인 브리지 코드**: `../bushra_excel_bridge_v1.py`
- **Master tanks 데이터**: `../bushra_stability/data/master_tanks.json`
- **원본 Excel 파일**: `../LCT_BUSHRA_AGI_TR.xlsx`

## 주의사항

1. **Stage 6, 7의 초기 Trim 값**은 추정값입니다. 실제 프로젝트 값과 다르면 `stage_config_sample_4_7.json`에서 수정하세요.

2. **탱크 선택 및 Percent_Fill**은 예시입니다. 실제 운용 시 프로젝트 요구사항에 맞게 조정이 필요합니다.

3. **Excel 파일이 열려있으면** 스크립트 실행이 실패할 수 있습니다. 실행 전 Excel 파일을 닫아주세요.

## 관련 문서

- 상세 작업 요약: `FINAL_BRIDGE_EXECUTION_SUMMARY.md`
- 브리지 함수 설명: `../bushra_excel_bridge_v1.py` (docstring 참고)

---

**작업 완료일**: 2025-01-XX  
**브리지 상태**: ✅ 정상 작동  
**데이터 완성도**: ✅ 완료
