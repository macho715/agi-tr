# Stage 4/6/7 Trim 값 채우기 및 브리지 실행 완료 요약

## 완료된 작업

### 1. Excel RORO 시트에서 Stage 4 Trim 값 읽기 ✅
- **파일**: `LCT_BUSHRA_AGI_TR.xlsx`
- **시트**: `RORO_Stage_Scenarios`
- **결과**:
  - Stage 4: Row 18, Trim_cm = **-181.89 cm**
  - Stage 6, 7: Excel 파일에 없음 (null로 설정, 나중에 입력 가능)

### 2. stage_config_sample_4_7.json 생성 ✅
- **파일**: `stage_config_sample_4_7.json`
- **내용**:
  - Vessel 메타데이터 (Lpp_m=60.302, LCF_m_from_midship=0.433, MTC_tm_per_cm=34.61 등)
  - Stage 4: trim_initial_cm = -181.89 cm
  - Stage 6, 7: trim_initial_cm = null (나중에 입력 필요)
  - 모든 Stage에 ballast 설정 포함 (pump_rate_tph=5.0, x_ballast_m_mid=12.0)

### 3. Stage_Tanks 시트 생성 ✅
- **템플릿 파일**: `Stage_Tanks_template.xlsx`
  - Stage_Tanks 시트: 샘플 행 포함 (Stage 5A-2, CL.P, 80%, TRUE)
  - Tank_Master_Ref 시트: 31개 탱크 전체 레퍼런스
- **원본 Excel에 추가**: `LCT_BUSHRA_AGI_TR.xlsx`에 Stage_Tanks 시트 추가됨

### 4. 브리지 코드 실행 ✅

#### 4.1 export_tank_summaries_to_excel() 실행
- **입력**: `stage_config_sample_4_7.json` + `master_tanks.json`
- **출력**: `bushra_stability_export.xlsx`
- **생성된 시트**:
  - `Tank_Coordinates`: 탱크 좌표 테이블
  - `Stage_Tank_Sums`: Stage 4/6/7 요약 (현재 tanks 배열이 비어있어 0 값)

#### 4.2 stage_workbook_to_stability_json() 실행
- **입력**: `LCT_BUSHRA_AGI_TR.xlsx` (원본 워크북)
- **출력**: `bushra_stability_verification.json`
- **결과**: 정상 실행 완료

## 생성된 파일

1. `stage_config_sample_4_7.json` - Stage 4/6/7 설정 파일
2. `Stage_Tanks_template.xlsx` - Stage_Tanks 템플릿 (2개 시트)
3. `bushra_stability_export.xlsx` - JSON → Excel 변환 결과
4. `bushra_stability_verification.json` - Excel → JSON 검증 결과
5. `LCT_BUSHRA_AGI_TR.xlsx` - 원본 파일에 Stage_Tanks 시트 추가됨

## 다음 단계 (사용자 작업 필요)

1. **Stage 6, 7 Trim 값 입력**
   - Excel RORO 시트에 Stage 6, 7 추가 또는
   - `stage_config_sample_4_7.json`에서 직접 trim_initial_cm 값 입력

2. **Stage 4/6/7 목표 Trim 값 설정**
   - `stage_config_sample_4_7.json`에서 각 Stage의 `trim_target_cm` 값 입력

3. **Stage_Tanks 시트 채우기**
   - `Stage_Tanks_template.xlsx` 또는 `LCT_BUSHRA_AGI_TR.xlsx`의 Stage_Tanks 시트에서
   - 각 Stage별로 사용할 탱크 선택
   - Percent_Fill, SG, UseForBallast 값 입력
   - UseForBallast=TRUE로 설정할 탱크 선택

4. **브리지 재실행**
   - Stage_Tanks 데이터를 채운 후
   - `export_tank_summaries_to_excel()` 재실행하여 완전한 Excel 파일 생성

## 참고 사항

- Stage 5A-1/2/3은 이미 trim 타깃(-121 / -96.50 / -84.34 cm)이 설정되어 있음
- 모든 숫자 값 (Lpp_m, LCF, MTC 등)은 현재 코드/워크북 기준으로 설정됨
- 실제 최종 보고서 값과 다르면 `stage_config_sample_4_7.json`에서 바로 조정 가능

