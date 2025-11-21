# Mammoet 제출 패키지 - 빠른 실행 가이드

## 🚀 실행 방법

### Step 1: RORO 계산기 생성 (patch3.py)
```bash
cd C:\Users\SAMSUNG\Downloads\KZ_measurement_note\scripts
python patch3.py
```
→ 생성: `LCT_BUSHRA_Package_RORO_FIXED.xlsx`

### Step 2: Mammoet 제출 패키지 생성
```bash
python generate_mammoet_package.py
```

### Step 3: 생성된 패키지 확인
```
MAMMOET_PACKAGE/
├── 01_PDF_Report/
│   └── LCT_BUSHRA_FWD_AFT_Report_for_Mammoet.pdf  ← 주요 문서
├── 02_Working_Excel/
│   └── LCT_BUSHRA_FWD_AFT_Calculator_COMPLETE.xlsx
├── 03_Supporting_Evidence/
│   ├── KZ_Measurement_Evidence.txt
│   └── Tide_Data_Source.txt
└── README_MAMMOET.txt
```

---

## 📧 이메일 템플릿 (Mammoet 제출용)

### 기본 이메일

```
To: [Mammoet Operations Coordinator]
Cc: [Aries Marine Superintendent], [Samsung Project Manager]
Subject: LCT BUSHRA FWD/AFT Draft Calculation - HVDC Transformer Transport

Dear Mammoet Team,

Please find attached the FWD/AFT draft calculations for LCT BUSHRA 
RORO operations at Mina Zayed Port for the HVDC Transformer 
Transportation project.

KEY INFORMATION:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
• K-Z Distance (site measured):  [X.XX] m
• Linkspan Length:               12.0 m
• Maximum Ramp Angle Limit:      6.0°
• Tide Data Source:              [AD Ports / ADNOC]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

RECOMMENDED OPERATION WINDOWS:
Window 1: [Date] [Start Time] - [End Time] ([X] hours continuous)
  • Average Tide: [X.XX] m
  • Average Ramp Angle: [X.X]° (within limit)
  • Status: All hours show OK for RORO operations

Window 2: [Date] [Start Time] - [End Time] ([X] hours continuous)
  • Average Tide: [X.XX] m
  • Average Ramp Angle: [X.X]° (within limit)
  • Status: All hours show OK for RORO operations

ATTACHMENTS:
1. LCT_BUSHRA_FWD_AFT_Report_for_Mammoet.pdf (Primary document)
2. LCT_BUSHRA_FWD_AFT_Calculator_COMPLETE.xlsx (Reference, optional)
3. KZ_measurement_photo.jpg (Site measurement evidence)
4. Tide_table_source.pdf (Official data source)

The PDF report provides detailed hourly schedules with tide levels, 
draft requirements, and ramp angles. All calculations are based on 
site-measured K-Z distance and official tide predictions.

The Excel workbook is provided for your reference and can be used 
for real-time adjustments during operations (sheet protection 
password: MAMMOET2025).

For Intact Stability and MSRA preparation (Aries Marine):
The attached data provides the necessary FWD/AFT draft information 
for your stability calculations and risk assessments.

Please review and let us know if you require any clarifications or 
additional information.

Best regards,

[Your Name]
[Position]
Samsung C&T Engineering & Construction
Logistics Department

Mobile: [Phone]
Email: [Email]
```

---

## 📧 한국어 이메일 템플릿

```
수신: [Mammoet 운영 담당자]
참조: [Aries Marine], [Samsung 프로젝트 매니저]
제목: LCT BUSHRA 선수/선미 흘수 계산서 - HVDC 변압기 운송

Mammoet 팀 귀하,

HVDC 변압기 운송 프로젝트를 위한 Mina Zayed Port에서의 
LCT BUSHRA RORO 작업 관련 선수/선미 흘수 계산서를 첨부합니다.

주요 정보:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
• K-Z 거리 (현장 실측):       [X.XX] m
• 링크스팬 길이:              12.0 m
• 최대 램프 각도 제한:        6.0°
• 조수 데이터 출처:           [AD Ports / ADNOC]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

권장 작업 시간대:
구간 1: [날짜] [시작시간] - [종료시간] (연속 [X]시간)
  • 평균 조수: [X.XX] m
  • 평균 램프 각도: [X.X]° (제한 범위 내)
  • 상태: 모든 시간대 RORO 작업 가능 (OK)

구간 2: [날짜] [시작시간] - [종료시간] (연속 [X]시간)
  • 평균 조수: [X.XX] m
  • 평균 램프 각도: [X.X]° (제한 범위 내)
  • 상태: 모든 시간대 RORO 작업 가능 (OK)

첨부 파일:
1. LCT_BUSHRA_FWD_AFT_Report_for_Mammoet.pdf (주요 문서)
2. LCT_BUSHRA_FWD_AFT_Calculator_COMPLETE.xlsx (참고용)
3. KZ_measurement_photo.jpg (현장 측정 사진)
4. Tide_table_source.pdf (공식 조수표 출처)

PDF 보고서는 조수 높이, 흘수 요구사항, 램프 각도가 포함된 시간별 
상세 스케줄을 제공합니다. 모든 계산은 현장 측정된 K-Z 거리와 
공식 조수 예측을 기반으로 합니다.

Excel 워크북은 참고용으로 제공되며 운영 중 실시간 조정에 사용 
가능합니다 (시트 보호 비밀번호: MAMMOET2025).

Aries Marine의 Intact Stability 및 MSRA 작성을 위해:
첨부된 데이터는 복원성 계산 및 위험 평가에 필요한 선수/선미 
흘수 정보를 제공합니다.

검토 후 추가 정보나 설명이 필요하시면 연락 주시기 바랍니다.

감사합니다.

[이름]
[직책]
삼성물산 건설부문
물류팀

휴대폰: [번호]
이메일: [이메일]
```

---

## ⚠️ 제출 전 체크리스트

### 필수 확인 사항

```
□ K-Z 거리 현장 측정 완료
  └── 측정값: ______ m
  └── Excel Calc!D6 업데이트 완료
  └── 측정 사진 촬영 (최소 1장)

□ 공식 조수 데이터 확보
  └── 출처: □ AD Ports  □ ADNOC
  └── Excel December_Tide_2025 시트에 붙여넣기 완료
  └── 출처 스크린샷/PDF 준비

□ 패키지 재생성
  └── python generate_mammoet_package.py 실행
  └── PDF 확인 (K-Z 값 정확한지 확인)
  └── 운영 가능 시간대 확인

□ 첨부 파일 준비
  └── PDF Report
  └── Excel Calculator (선택사항)
  └── K-Z 측정 사진
  └── 조수표 출처 문서

□ 이메일 작성
  └── 권장 작업 시간대 기재
  └── K-Z 측정값 명시
  └── 연락처 정보 기재
```

---

## 📊 PDF 보고서 주요 내용

### Page 1: 요약 + 권장 시간대

```
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ CRITICAL PARAMETERS (Site Measured)        ┃
┣━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┫
┃ K–Z Distance:        [X.XX] m              ┃
┃ Linkspan Length:     12.0 m                ┃
┃ Max Ramp Angle:      6.0°                  ┃
┃ Vessel Depth:        3.65 m (LCT Bushra actual depth, corrected from 4.85m) ┃
┃ Draft Range:         1.5 - 3.5 m           ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛

RECOMMENDED OPERATION WINDOWS (≥2h continuous)

Window 1: [Start] → [End]
  Duration: [X] hours
  Avg Tide: [X.XX]m
  Avg Ramp Angle: [X.X]°

DETAILED HOURLY SCHEDULE
┌──────┬──────┬──────┬─────────┬─────────┬──────┬──────┬────────┬─────────┐
│ Date │ Time │ Tide │ Dfwd_req│ Daft_req│ Trim │ Ramp∠│ Status │ Remark  │
│      │ GST  │  m   │    m    │    m    │  m   │ deg  │        │         │
├──────┼──────┼──────┼─────────┼─────────┼──────┼──────┼────────┼─────────┤
│12-01 │00:00 │ 2.06 │  8.06   │  8.06   │  -   │ 4.2  │   OK   │OK RORO  │
└──────┴──────┴──────┴─────────┴─────────┴──────┴──────┴────────┴─────────┘
... (계속)
```

### Page 2: 추가 시간대 (필요 시)

```
DETAILED HOURLY SCHEDULE (Continuation)

... (25-48시간 테이블)

CONTACT INFORMATION
Prepared by: Samsung Logistics Team
Mammoet Coordinator: [To be filled]
Aries Marine: [To be filled]
```

---

## 💾 Excel 워크북 사용법

### 기본 정보

- **파일명**: `LCT_BUSHRA_FWD_AFT_Calculator_COMPLETE.xlsx`
- **보호**: 수식 잠금 (실수 방지)
- **비밀번호**: `MAMMOET2025`

### 편집 가능한 영역 (노란색 셀)

```
Calc 시트:
  D6 → K-Z 거리 (현장 측정값 입력)

December_Tide_2025 시트:
  B2:B745 → 조수 데이터 (공식 조수표에서 붙여넣기)

Hourly_FWD_AFT_Heights 시트:
  D열 → Trim 입력 (선택사항, 필요 시)

RORO_Stage_Scenarios 시트:
  B열 → 화물 중량 (W_stage_t)
  C열 → 화물 위치 (x_stage_m)
```

### 실시간 사용 시나리오

**상황: 실제 조수가 예측과 다를 때**
```
1. Excel 파일 열기
2. December_Tide_2025 시트로 이동
3. 해당 시간의 조수 값 수정
4. Hourly_FWD_AFT_Heights 시트 확인
5. Status 컬럼에서 "OK" 확인
6. 작업 진행 여부 결정
```

---

## 🎯 Mammoet이 이 데이터로 하는 작업

### 1. RORO 작업 스케줄링
- 최적 작업 시간대 선정
- 조수에 따른 작업 계획
- 램프 각도 검증

### 2. 링크스팬 포지셔닝
- K-Z 거리 기반 설치 높이 계산
- 선박 접안 시 램프 각도 확인
- 안전 마진 검증

### 3. Aries Marine 전달 (Intact Stability)
- FWD/AFT 흘수 데이터 제공
- 복원성 계산 입력
- MSRA (Marine Spread Risk Assessment) 작성

---

## 📞 문의처

### Samsung C&T
- 프로젝트 매니저: [이름, 이메일, 전화]
- 물류 코디네이터: [이름, 이메일, 전화]

### LCT BUSHRA
- 선장: [이름, 전화, VHF 채널]
- 일등항해사: [이름, 전화]

### Mammoet
- 운영 코디네이터: [이름, 이메일, 전화]
- 프로젝트 엔지니어: [이름, 이메일, 전화]

### Aries Marine
- Marine Superintendent: [이름, 이메일, 전화]

---

## 🔄 업데이트 프로세스

### 데이터 변경 시

```
1. 원본 Excel 파일 업데이트
   (LCT_BUSHRA_Package_RORO_FIXED.xlsx)

2. 스크립트 재실행
   python generate_mammoet_package.py

3. 새로운 PDF 확인
   → K-Z 값 변경 반영 확인
   → 권장 시간대 변경 확인

4. Mammoet에 업데이트 통보
   Subject: [UPDATED] LCT BUSHRA FWD/AFT Calculation
```

---

## ✅ 성공적인 제출 사례

```
✓ K-Z 거리: 3.25m (현장 실측)
✓ 조수 출처: AD Ports 공식 조수표
✓ 권장 시간대: 12월 5일 08:00-14:00 (6시간 연속)
✓ 최대 램프 각도: 5.2° (6° 제한 내)
✓ 첨부 완료: PDF + Excel + 사진 3장 + 조수표

→ Mammoet 확인 완료
→ Aries Marine으로 전달
→ Intact Stability 계산 진행
→ RORO 작업 승인
```

---

**모든 준비 완료!** 이제 실행하고 Mammoet에 제출하세요. 🚀
