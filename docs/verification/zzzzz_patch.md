# zzzzz.md 가이드 패치 검증 보고서

## 📋 검증 일시
2025-11-19

## ✅ 1. 구조·수식 검증 결과

### 1.1 파라미터 영역 ✅
- **A6**: `Trim_target_cm` (헤더) ✅
- **B6**: `-96.5` (목표 Trim_cm 값) ✅
- **B8**: `=INDEX(Calc!$E:$E, MATCH("MTC_t_m_per_cm", Calc!$C:$C, 0))` ✅
- **B11**: `=Calc!$E$31` (pump_rate_effective_tph) ✅

→ 이후 수식에서 전부 `$B$6`, `$B$8`, `$B$11`만 참조하므로 OK.

### 1.2 H열 ΔTM_cm_tm ✅
**수식**: `=IF($A{row}="","",(E{row} - $B$6) * $B$8)`

- 의미: (현재 Trim_cm - 목표 Trim_target_cm) × MTC = 필요한 Trim 모멘트
- E = B6인 Stage (Trim이 딱 목표값인 Stage)는 **H=0**이 떠야 정상 ✅

### 1.3 J열 Ballast_t_calc / K열 시간 ✅
**J 수식**: `=IF(OR($A{row}="",$I{row}="", $I{row}=0),"",ROUND(H{row} / $I{row}, 2))`
**K 수식**: `=IF(OR(J{row}="", $B$11="", $B$11=0, ISERROR($B$11)), "", ROUND(J{row} / $B$11, 2))`

- H/I → 이론 Ballast톤, 그걸 pump_rate로 나눈 시간 구조라 일관성 OK ✅

### 1.4 보라색 블록(AM~AP) ✅
- **AM (39)**: `=IF($A{row}="","",ABS(H{row}))` ✅ → ΔTM 크기만
- **AN (40)**: `=IF($A{row}="","",IF(OR($I{row}="",$I{row}=0),0,ROUND(H{row}/$I{row},2)))` ✅ → J와 동일 개념
- **AO (41)**: `=IF($A{row}="","",AN{row} - $L{row})` ✅ → 필요한 ballast − 실제 ballast(L열)
- **AP (42)**: `=IF($A{row}="","",IF($B$11=0,0,AO{row}/$B$11))` ✅ → Gap 톤 / 펌프레이트

→ 여기서 **AP는 부호를 그대로 유지**하므로
- AP>0 → "추가 Ballast 필요 → ballast 시간"
- AP<0 → "De-ballast 필요 → |AP| 시간만큼 빼야 함"

## 🔍 2. Excel에서 바로 해볼 수 있는 Sanity Check 3개

### 2.1 Trim = Target Stage 체크
**방법**: 어느 Stage든 E열(Trim_cm)에 **-96.5를 임시로 직접 입력**해 보기

**기대값**:
- H열 ≈ 0.00
- J, AM, AN, AO, AP 전부 0 또는 BLANK 근처

→ 이렇게 나오면 **Target 기준 ΔTM 로직이 맞게 물린 것** ✅

### 2.2 Stage 5A-2 감도 체크 (대략 수치)
**Stage 5A-2**: Trim_cm ≈ -96.5 (목표값과 동일), Target = -96.50

**예상 계산**:
- ΔTrim ≈ 0 cm
- H ≈ 0 × 33.99 ≈ **0.00** (t·m·cm 단위 모멘트)
- Lever_arm 21.62 → J/AN ≈ **0.00 t**

**해석**:
- H=0 → "목표 Trim 달성"
- AO = AN - L (L는 실제 Ballast) → "현재 Ballast와 필요한 Ballast 차이"
- AP = AO/45 → "추가/감소 시간"

→ 부호 방향이 이렇게 해석 가능한지만 봐주면 된다 ✅

### 2.3 Pump rate 변경 테스트
**방법**: B11을 45 → 90으로 바꿔 보기

**기대값**:
- J/AN/AO는 그대로
- K, AP 값이 **정확히 1/2로 줄어야** 정상 (펌프 2배 → 시간 반) ✅

## 🎯 3. 권장 마지막 미세 튜닝

### 3.1 운영용 시트
- AP를 "De-ballast/ballast 구분까지 보고 싶다" → 지금처럼 `AO/$B$11` (부호 유지) 그대로 두는 게 좋음 ✅

### 3.2 보고서용 그래프
- "시간은 항상 양수로만" 보고 싶다 → 다른 시트에서 `=ABS(Time_Add_h)`로 한 번 더 래핑해서 쓰는 방식 추천 ✅

## 📊 4. 한 줄 정리

> **지금 패치 내용 그대로면 `zzzzz.md` 가이드 요구사항(Trim_target 파라미터 + ΔTM·Ballast Fix 체인)과 완전히 일치하고,**
> **간단한 2~3개 Stage만 수동으로 건드려 보면 부호·크기 모두 직관에 맞게 움직이는 상태**라고 보면 된다.

## ✅ 5. 검증 완료 항목

- [x] 파라미터 영역 (A6, B6, B8, B11) 설정 완료
- [x] H열 ΔTM_cm_tm 수식 적용 완료
- [x] J열 Ballast_t_calc 수식 적용 완료
- [x] K열 Ballast_time_h_calc 수식 적용 완료
- [x] AM열 ΔTM_needed_cm·tm 수식 적용 완료
- [x] AN열 Ballast_req_t 수식 적용 완료
- [x] AO열 Ballast_gap_t 수식 적용 완료
- [x] AP열 Time_Add_h 수식 적용 완료
- [x] 모든 수식이 `$B$6`, `$B$8`, `$B$11` 참조 구조 일관성 확인

## 🚀 다음 단계

이제 이 H/J/AM~AP 블록이 살아났으니,
다음 단계는 **"옵션1/2/3 비교 시나리오"를 이 수치들로 바로 보고서 테이블/그래프에 뽑는 쪽**으로 이어가면 된다.

