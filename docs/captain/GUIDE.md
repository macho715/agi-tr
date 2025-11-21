요약부터 딱 짚을게요.
지금 올려주신 EXCEL_GEN 01/02/03 + TANK_LEVER_ARM 구조 기준으로 보면, **캡틴 메일에 제대로 답하려면** 최소 이 4가지가 파일 쪽에서 보완/패치돼야 합니다:

1. **Stage 5A-2 전·후흘수 계산 정합** (2.32 m vs 2.92 m 불일치 수정)
2. **FWB1/2, FWCARGO1(P/S) “AFT Ballast” 오표현 정리 + X_Ballast 처리 방식 수정**
3. **“모든 Stage에서 최대 흘수 2.70 m” 규칙을 수식/시트에 반영**
4. **링크스팬 여유고 0.28 m 검증용 전용 리포트(캡틴용 Stage Summary Sheet) 추가**

아래는 “지금 사용 중인 파일”에서 어디를 어떻게 손대야 하는지 정리한 패치 리스트입니다.

---

## 1. 패치 항목 요약 테이블

| Patch ID | 파일/모듈                  | 시트/섹션                                             | 무엇을 고쳐야 하는지                                                                                                       | 왜 필요한지 (캡틴 메일 기준)                                                                           |
| -------- | ---------------------- | ------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------- |
| P1       | Excel 생성기 / 기존 엑셀      | `Calc` 시트: 선박 기본 제원                               | `D_vessel`, 흘수/Trim 기준값 정합 확인 및 갱신                                                                                | Mammoet 쪽에서 “Depth 4.85 m vs 실제 3.65 m” 지적한 부분 정리용                                          |
| P2       | Excel 생성기 / 기존 엑셀      | `RORO_Stage_Scenarios` 시트 상단 파라미터 · Stage 5A-2 블록 | Stage 5A-2의 `Tmean`, `Trim_cm` 수식/값을 `Calc` 시트와 일치시키고, FWD Draft 2.32 ↔ 2.92 불일치 제거                               | 캡틴이 “파일에서 2.92 m인데, 메일에는 2.32 m”라고 콕 집어서 지적한 부분                                             |
| P3       | Excel + TANK_LEVER_ARM | 탱크 레버암/볼라스트 CG 계산 로직 → `X_Ballast`                | FWB1/2, FWCARGO1(P/S)가 **FWD 탱크**라는 캡틴 코멘트 반영해서, 한 방의 “AFT 470 t”이 아니라 “Stage별 탱크 조합 CG”로 `X_Ballast` 재계산/연결      | “470 t ballast OK, but tanks are forward not aft”에 대한 물리/설명 정합 확보                           |
| P4       | Excel 생성기              | `RORO_Stage_Scenarios` 및 새 `CAPTAIN_REPORT` 시트    | (a) 모든 Stage에 `Dfwd`, `Daft`에 대해 2.70 m limit check 수식 추가, (b) 링크스팬 freeboard 0.28 m 이상 여부를 한눈에 보는 Summary 테이블 구성 | “draft cannot be more than 2.7 m at all stages” + “linkspan freeboard 0.28 m 충분한지 확인” 요구 대응 |

---

## 2. 각 패치 상세 – “어디를, 어떻게” 수준으로

### P1. Calc 시트 – 선박 제원/기본 파라미터 정리

**어디?**

* `Calc` 시트 상단의 **선박 Geometry/Hydrostatics 블록**
  (EXCEL_GEN_03에서 설명된 `D_vessel_m`, `TPC_t_per_cm`, `MTC_t_m_per_cm`, `LCF_from_AP_m` 파라미터가 들어있는 영역)

**무엇을?**

1. **Depth / Draft 기준값 점검**

   * 현재 쓰는 엑셀에 **`D_vessel`가 4.85 m로 남아있으면 → 3.65 m**로 교체.
   * 이 값에서 파생되는 “Design Draft / Freeboard” 관련 셀에 참조가 걸려 있으면, 값이 자동으로 갱신되는지 확인.

2. **Stage 계산 입력과 정합**

   * `RORO_Stage_Scenarios`에서 사용 중인
     `Tmean_baseline`, `Trim_target_cm`, `LCF`, `MTC`, `TPC` 등이 전부 `Calc` 시트의 새 값(3.65 m 기준)에서 오도록 **참조/이름 범위**를 통일.
   * 수동 숫자(하드코딩)로 남아 있는 경우를 제거.

> 효과: 이후 Stage 5A-2 등에서 나오는 **FWD/AFT 흘수값이 전부 같은 기준**으로 계산됩니다.

---

### P2. Stage 5A-2 불일치(2.32 m vs 2.92 m) 정합

캡틴이 명확히 지적한 포인트라, 이 부분은 **수식 흐름 자체를 한 번 “닫아주는” 패치**가 필요합니다.

**어디?**

* 엑셀: `RORO_Stage_Scenarios` 시트

  * 상단 파라미터 블록: `Tmean_baseline`, `TRIM_BY_STAGE`, `X_Ballast`
  * Stage별 결과 테이블: `Stage`, `Tmean`, `Trim_cm`, `Dfwd_m`, `Daft_m`가 나오는 행
* Python: `build_bushra_agi_tr_from_scratch_patched.py` 안의

  * (문서에 나온 기준으로) `TRIM_TARGET_BY_STAGE` 또는 비슷한 딕셔너리/상수 정의 부분
  * `create_roro_stage_scenarios(...)` 처럼 Stage 시트를 채우는 함수

**무엇을?**

1. **계산 경로를 한 줄로 맞추기**

   * `Dfwd_m`은 기본적으로

     > `Dfwd = Tmean + Trim/2` (trim by FWD 기준일 때 기호만 조정)
     > 식으로 `Tmean`과 `Trim_cm`에서 파생됩니다.
   * Stage 5A-2에 대해:

     * `Calc` 시트(또는 내부 계산)에서 이미 2.92 m가 나온다면,
     * `RORO_Stage_Scenarios`에서 쓰는 `Tmean` / `Trim_cm`이 **그 값을 재생산하도록 역산**해야 합니다.

       * 예: `Tmean`을 2.92−Trim/2로 다시 잡거나, Trim을 줄여서 `Dfwd ≤ 2.70 m`에 맞추는 것 둘 중 하나를 선택.

2. **“표에 2.32 m” 문제 해결**

   * `Stage 5A-2` 행의 `Dfwd_m`이 **직접 숫자로 입력**돼 있다면 → 반드시 수식으로 교체:

     * 예: `=Tmean + (Trim_cm/100)/2` (부호는 기준에 맞춰 조정)
   * `Trim_cm`도 상단의 `TRIM_BY_STAGE`(또는 이름 범위)에서 가져오도록 만들고, Stage 행에 수동 값이 들어가면 안 되게 정리.

3. **2.70 m 제한 반영(캡틴 요구)**

   * Stage 5A-2의 `Tmean` / `Trim_cm` 값을 조정할 때,
     **결과 `Dfwd_m`이 항상 ≤ 2.70 m**가 되도록 값 자체를 다시 튜닝해야 합니다.
   * 이건 단순히 보고용이 아니라, 나중에 **Conditional Formatting**까지 걸어둘 예정(P4 패치에서 설명).

> 이 패치가 끝나면, 캡틴이 다시 같은 계산서를 봐도
> “파일엔 2.92인데 메일은 2.32” 같은 불일치는 없어집니다.

---

### P3. FWD 탱크 / Ballast CG 재처리 (`X_Ballast` 패치)

캡틴 코멘트 핵심:

* “**FWB1, FWB2, FWCARGO1(P/S)는 FWD 탱크**인데, 메일/계산에선 AFT ballast처럼 쓰였다.”
* “470 t ballast 자체는 문제 없지만, 위치와 GM이 지금 숫자와 안 맞는다.”

지금 구조에서는 `X_Ballast`를 **단일 숫자(예: 52.53 m)**로 두고, 이걸로 Stage 전부를 처리하는 설계가 되어 있습니다(문서 기준). 이걸 “탱크 CG 기반”으로 바꾸는 게 패치 포인트입니다.

**어디?**

* 엑셀:

  * `RORO_Stage_Scenarios` 시트 상단의 `X_Ballast_m` 셀
* (별도 파일) TANK 레버암 워크북:

  * `TANK_CATALOG` 시트: 각 탱크의 `x_tank`
  * `STAGE_TANK_SUMS` 또는 비슷한 요약 시트: Stage별 탱크 조합/톤수

**무엇을?**

1. **Stage별 “효과 중심(CG)” 계산**

   * TANK 워크북에서 Stage 5A-2에 해당하는 탱크 조합에 대해:

     * `X_Ballast_effective = Σ(W_i * x_i) / Σ(W_i)`
       (FWB1, FWB2, FWCARGO1(P/S) + 필요시 다른 탱크 포함)
   * 이 값이 실제로는 **선수 가까운 쪽 좌표**가 나와야 합니다 (FWD 탱크이므로).

2. **`X_Ballast` 하드코딩 제거**

   * `RORO_Stage_Scenarios`의 `X_Ballast_m`:

     * 지금 52.53 같은 고정값이면 → “Stage 5A-2용 X_Ballast”를 참조하는 방식으로 수정:

       * 예: 새로운 시트 `Ballast_CG`에 Stage별 `X_Ballast`를 정리해 놓고,
       * Stage 5A-2 행이 `=Ballast_CG!B2` 식으로 가져가도록.

3. **용어 정리**

   * 문서/시트에 있는 “AFT ballast 470 t” 표현은

     * “**Forward tanks group (FWB1/2 + FWCARGO1 P/S) total ballast ≈470 t**” 정도로 수정.
   * 보고서·이메일 텍스트에서도 “AFT”라는 단어를 빼고,

     * “ballast applied in forward tanks to achieve required trim” 처럼 서술.

> 이 패치를 해두면, 캡틴이 “탱크는 FWD인데 왜 AFT ballast라고 부르냐”는 의문을 더 이상 제기하지 못합니다.

---

### P4. 2.70 m 제한 + 링크스팬 0.28 m 검증용 리포트 추가

캡틴 메일의 마지막 요구 두 개:

1. **“Draft cannot be more than 2.7 m at all stages as per vessel summer draft”**
2. **“Please confirm that linkspan freeboard 0.28 m is enough…”**

이를 위해 **지금 구조 위에 얇게 “캡틴 뷰” 레이어**를 추가하는 방향이 가장 안전합니다.

#### 4-1) Stage Limit Check 수식 추가

**어디?**

* `RORO_Stage_Scenarios` 시트의 Stage별 결과 테이블

**무엇을?**

1. 새 컬럼 2개 추가:

   * `Dfwd_Check` (예: 헤더 “Dfwd ≤ 2.70 m ?”)
   * `Daft_Check` (예: 헤더 “Daft ≤ 2.70 m ?”)

2. 각 셀 수식:

   * `=IF([Dfwd_m_cell] > 2.7, "FAIL", "OK")`
   * `=IF([Daft_m_cell] > 2.7, "FAIL", "OK")`

3. Conditional Formatting:

   * "FAIL" 셀은 붉은색, "OK"는 녹색으로 표시.

> 이러면 캡틴/Harbour Master에게 바로 “모든 Stage에서 2.70 m 이하임”을 한눈에 보여줄 수 있습니다.

#### 4-2) Linkspan Freeboard 0.28 m 검증용 시트

**어디?**

* 새 시트 예: `CAPTAIN_REPORT`

**무엇을?**

1. 기본 구조

   | Stage | Tmean | Trim (m, F/A) | Dfwd (m) | Daft (m) | FWD_Height_at_linkspan (m) | Freeboard_vs_RampDoor (m) | Draft Limit OK? | Freeboard ≥ 0.28? |
   | ----- | ----- | ------------- | -------- | -------- | -------------------------- | ------------------------- | --------------- | ----------------- |

2. 연결 로직

   * `Dfwd` / `Daft`: `RORO_Stage_Scenarios`에서 참조
   * `FWD_Height_at_linkspan`: 기존에 `Hourly_FWD_AFT_Heights` 또는 RORO 시트에서 계산하는 “접속부 수면 높이”를 참조
   * `Freeboard_vs_RampDoor`:

     * 기준점 하나 잡기 (예: Ramp door 하단 기준 높이)
     * `Freeboard = RampDoor_Level - WaterLevel_at_linkspan`
     * 이 값이 0.28 m 이상이면 “OK”

3. Check 컬럼 수식

   * `Draft Limit OK?`:

     * `=IF(AND(Dfwd<=2.7, Daft<=2.7), "OK", "FAIL")`
   * `Freeboard ≥ 0.28?`:

     * `=IF(Freeboard_vs_RampDoor>=0.28, "OK", "FAIL")`

> 이 시트 한 장만 PDF로 뽑아서 캡틴/Harbour Master에게 보내면, “2.70 m 제한 + 0.28 m freeboard” 두 요구를 동시에 커버할 수 있습니다.

---

## 3. 정리 – 실제 작업 순서(추천)

1. **현재 엑셀에서 `Calc` 시트 제원 값 점검/수정 (P1)**

   * Depth/Draft/TPC/MTC/LCF 값이 전부 최신 BV/Aries 기준인지 확인 후 고정.

2. **Stage 5A-2 수식 라인 정리 (P2)**

   * RORO 시트 Stage 5A-2에 수동 숫자/옛날 값이 남아있으면 완전히 제거하고,
     전부 `Calc` 시트 + TRIM_BY_STAGE에서 파생되게 수정.

3. **탱크 CG 계산과 `X_Ballast` 연동 (P3)**

   * TANK 워크북에서 Stage별 `X_Ballast_effective` 뽑고,
   * RORO 시트의 `X_Ballast_m`를 이 값으로 참조 전환.

4. **캡틴용 리포트 레이어 추가 (P4)**

   * RORO 시트에 Draft Limit Check 컬럼 추가,
   * 새 `CAPTAIN_REPORT` 시트에 Stage별 요약 테이블 생성.

---

## 4. 다음 단계 제안

원하시면 다음 턴에서:

* **(A)** `CAPTAIN_REPORT` 시트를 엑셀 수식까지 포함한 “완전 템플릿”으로 설계해 드리고,
* **(B)** `build_bushra_agi_tr_from_scratch_patched.py`에

  * `create_captain_report_sheet(wb)` 같은 함수를 추가하는 **Python 코드 패치 스니펫**도 같이 드릴 수 있습니다.

일단 지금은, **“어디를, 왜, 어떻게 고쳐야 하는지”**를 한 번에 볼 수 있게 정리해 둔 거라,
이 순서대로만 손대시면 캡틴 메일에서 나온 포인트는 전부 커버 가능합니다.
