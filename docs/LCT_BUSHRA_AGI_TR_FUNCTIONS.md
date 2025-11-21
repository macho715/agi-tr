# LCT_BUSHRA_AGI_TR.xlsx 함수 목록 (시트별)

**생성 일시**: 2025-11-13T04:31:24.920105
**원본 파일**: LCT_BUSHRA_AGI_TR.xlsx

## 개요

- **총 시트 수**: 4개
- **총 수식 수**: 7495개
- **고유 함수 종류**: 11개

## 시트별 함수 목록

### Calc

**시트 정보**: 20행 × 7열, 수식 0개

*수식이 없는 시트입니다.*

### December_Tide_2025

**시트 정보**: 745행 × 2열, 수식 0개

*수식이 없는 시트입니다.*

### Hourly_FWD_AFT_Heights

**시트 정보**: 745행 × 14열, 수식 7440개

#### AND (사용 744회)

**셀 위치 및 수식**:

- **H2**: `=IF($E2="","", IF(AND($E2>=INDEX(Calc!$E:$E, MATCH("min_fwd_draft_m", Calc!$C:$C, 0)), $E2<=INDEX...`
- **H3**: `=IF($E3="","", IF(AND($E3>=INDEX(Calc!$E:$E, MATCH("min_fwd_draft_m", Calc!$C:$C, 0)), $E3<=INDEX...`
- **H4**: `=IF($E4="","", IF(AND($E4>=INDEX(Calc!$E:$E, MATCH("min_fwd_draft_m", Calc!$C:$C, 0)), $E4<=INDEX...`
- **H5**: `=IF($E5="","", IF(AND($E5>=INDEX(Calc!$E:$E, MATCH("min_fwd_draft_m", Calc!$C:$C, 0)), $E5<=INDEX...`
- **H6**: `=IF($E6="","", IF(AND($E6>=INDEX(Calc!$E:$E, MATCH("min_fwd_draft_m", Calc!$C:$C, 0)), $E6<=INDEX...`
- **H7**: `=IF($E7="","", IF(AND($E7>=INDEX(Calc!$E:$E, MATCH("min_fwd_draft_m", Calc!$C:$C, 0)), $E7<=INDEX...`
- **H8**: `=IF($E8="","", IF(AND($E8>=INDEX(Calc!$E:$E, MATCH("min_fwd_draft_m", Calc!$C:$C, 0)), $E8<=INDEX...`
- **H9**: `=IF($E9="","", IF(AND($E9>=INDEX(Calc!$E:$E, MATCH("min_fwd_draft_m", Calc!$C:$C, 0)), $E9<=INDEX...`
- **H10**: `=IF($E10="","", IF(AND($E10>=INDEX(Calc!$E:$E, MATCH("min_fwd_draft_m", Calc!$C:$C, 0)), $E10<=IN...`
- **H11**: `=IF($E11="","", IF(AND($E11>=INDEX(Calc!$E:$E, MATCH("min_fwd_draft_m", Calc!$C:$C, 0)), $E11<=IN...`
- **H12**: `=IF($E12="","", IF(AND($E12>=INDEX(Calc!$E:$E, MATCH("min_fwd_draft_m", Calc!$C:$C, 0)), $E12<=IN...`
- **H13**: `=IF($E13="","", IF(AND($E13>=INDEX(Calc!$E:$E, MATCH("min_fwd_draft_m", Calc!$C:$C, 0)), $E13<=IN...`
- **H14**: `=IF($E14="","", IF(AND($E14>=INDEX(Calc!$E:$E, MATCH("min_fwd_draft_m", Calc!$C:$C, 0)), $E14<=IN...`
- **H15**: `=IF($E15="","", IF(AND($E15>=INDEX(Calc!$E:$E, MATCH("min_fwd_draft_m", Calc!$C:$C, 0)), $E15<=IN...`
- **H16**: `=IF($E16="","", IF(AND($E16>=INDEX(Calc!$E:$E, MATCH("min_fwd_draft_m", Calc!$C:$C, 0)), $E16<=IN...`
- **H17**: `=IF($E17="","", IF(AND($E17>=INDEX(Calc!$E:$E, MATCH("min_fwd_draft_m", Calc!$C:$C, 0)), $E17<=IN...`
- **H18**: `=IF($E18="","", IF(AND($E18>=INDEX(Calc!$E:$E, MATCH("min_fwd_draft_m", Calc!$C:$C, 0)), $E18<=IN...`
- **H19**: `=IF($E19="","", IF(AND($E19>=INDEX(Calc!$E:$E, MATCH("min_fwd_draft_m", Calc!$C:$C, 0)), $E19<=IN...`
- **H20**: `=IF($E20="","", IF(AND($E20>=INDEX(Calc!$E:$E, MATCH("min_fwd_draft_m", Calc!$C:$C, 0)), $E20<=IN...`
- **H21**: `=IF($E21="","", IF(AND($E21>=INDEX(Calc!$E:$E, MATCH("min_fwd_draft_m", Calc!$C:$C, 0)), $E21<=IN...`
- *... 외 724개 셀에서 사용됨*

#### ATAN (사용 744회)

**셀 위치 및 수식**:

- **G2**: `=IF($E2="","", DEGREES(ATAN((INDEX(Calc!$E:$E, MATCH("KminusZ_m", Calc!$C:$C, 0)) - $E2 + $B2) / ...`
- **G3**: `=IF($E3="","", DEGREES(ATAN((INDEX(Calc!$E:$E, MATCH("KminusZ_m", Calc!$C:$C, 0)) - $E3 + $B3) / ...`
- **G4**: `=IF($E4="","", DEGREES(ATAN((INDEX(Calc!$E:$E, MATCH("KminusZ_m", Calc!$C:$C, 0)) - $E4 + $B4) / ...`
- **G5**: `=IF($E5="","", DEGREES(ATAN((INDEX(Calc!$E:$E, MATCH("KminusZ_m", Calc!$C:$C, 0)) - $E5 + $B5) / ...`
- **G6**: `=IF($E6="","", DEGREES(ATAN((INDEX(Calc!$E:$E, MATCH("KminusZ_m", Calc!$C:$C, 0)) - $E6 + $B6) / ...`
- **G7**: `=IF($E7="","", DEGREES(ATAN((INDEX(Calc!$E:$E, MATCH("KminusZ_m", Calc!$C:$C, 0)) - $E7 + $B7) / ...`
- **G8**: `=IF($E8="","", DEGREES(ATAN((INDEX(Calc!$E:$E, MATCH("KminusZ_m", Calc!$C:$C, 0)) - $E8 + $B8) / ...`
- **G9**: `=IF($E9="","", DEGREES(ATAN((INDEX(Calc!$E:$E, MATCH("KminusZ_m", Calc!$C:$C, 0)) - $E9 + $B9) / ...`
- **G10**: `=IF($E10="","", DEGREES(ATAN((INDEX(Calc!$E:$E, MATCH("KminusZ_m", Calc!$C:$C, 0)) - $E10 + $B10)...`
- **G11**: `=IF($E11="","", DEGREES(ATAN((INDEX(Calc!$E:$E, MATCH("KminusZ_m", Calc!$C:$C, 0)) - $E11 + $B11)...`
- **G12**: `=IF($E12="","", DEGREES(ATAN((INDEX(Calc!$E:$E, MATCH("KminusZ_m", Calc!$C:$C, 0)) - $E12 + $B12)...`
- **G13**: `=IF($E13="","", DEGREES(ATAN((INDEX(Calc!$E:$E, MATCH("KminusZ_m", Calc!$C:$C, 0)) - $E13 + $B13)...`
- **G14**: `=IF($E14="","", DEGREES(ATAN((INDEX(Calc!$E:$E, MATCH("KminusZ_m", Calc!$C:$C, 0)) - $E14 + $B14)...`
- **G15**: `=IF($E15="","", DEGREES(ATAN((INDEX(Calc!$E:$E, MATCH("KminusZ_m", Calc!$C:$C, 0)) - $E15 + $B15)...`
- **G16**: `=IF($E16="","", DEGREES(ATAN((INDEX(Calc!$E:$E, MATCH("KminusZ_m", Calc!$C:$C, 0)) - $E16 + $B16)...`
- **G17**: `=IF($E17="","", DEGREES(ATAN((INDEX(Calc!$E:$E, MATCH("KminusZ_m", Calc!$C:$C, 0)) - $E17 + $B17)...`
- **G18**: `=IF($E18="","", DEGREES(ATAN((INDEX(Calc!$E:$E, MATCH("KminusZ_m", Calc!$C:$C, 0)) - $E18 + $B18)...`
- **G19**: `=IF($E19="","", DEGREES(ATAN((INDEX(Calc!$E:$E, MATCH("KminusZ_m", Calc!$C:$C, 0)) - $E19 + $B19)...`
- **G20**: `=IF($E20="","", DEGREES(ATAN((INDEX(Calc!$E:$E, MATCH("KminusZ_m", Calc!$C:$C, 0)) - $E20 + $B20)...`
- **G21**: `=IF($E21="","", DEGREES(ATAN((INDEX(Calc!$E:$E, MATCH("KminusZ_m", Calc!$C:$C, 0)) - $E21 + $B21)...`
- *... 외 724개 셀에서 사용됨*

#### DEGREES (사용 744회)

**셀 위치 및 수식**:

- **G2**: `=IF($E2="","", DEGREES(ATAN((INDEX(Calc!$E:$E, MATCH("KminusZ_m", Calc!$C:$C, 0)) - $E2 + $B2) / ...`
- **G3**: `=IF($E3="","", DEGREES(ATAN((INDEX(Calc!$E:$E, MATCH("KminusZ_m", Calc!$C:$C, 0)) - $E3 + $B3) / ...`
- **G4**: `=IF($E4="","", DEGREES(ATAN((INDEX(Calc!$E:$E, MATCH("KminusZ_m", Calc!$C:$C, 0)) - $E4 + $B4) / ...`
- **G5**: `=IF($E5="","", DEGREES(ATAN((INDEX(Calc!$E:$E, MATCH("KminusZ_m", Calc!$C:$C, 0)) - $E5 + $B5) / ...`
- **G6**: `=IF($E6="","", DEGREES(ATAN((INDEX(Calc!$E:$E, MATCH("KminusZ_m", Calc!$C:$C, 0)) - $E6 + $B6) / ...`
- **G7**: `=IF($E7="","", DEGREES(ATAN((INDEX(Calc!$E:$E, MATCH("KminusZ_m", Calc!$C:$C, 0)) - $E7 + $B7) / ...`
- **G8**: `=IF($E8="","", DEGREES(ATAN((INDEX(Calc!$E:$E, MATCH("KminusZ_m", Calc!$C:$C, 0)) - $E8 + $B8) / ...`
- **G9**: `=IF($E9="","", DEGREES(ATAN((INDEX(Calc!$E:$E, MATCH("KminusZ_m", Calc!$C:$C, 0)) - $E9 + $B9) / ...`
- **G10**: `=IF($E10="","", DEGREES(ATAN((INDEX(Calc!$E:$E, MATCH("KminusZ_m", Calc!$C:$C, 0)) - $E10 + $B10)...`
- **G11**: `=IF($E11="","", DEGREES(ATAN((INDEX(Calc!$E:$E, MATCH("KminusZ_m", Calc!$C:$C, 0)) - $E11 + $B11)...`
- **G12**: `=IF($E12="","", DEGREES(ATAN((INDEX(Calc!$E:$E, MATCH("KminusZ_m", Calc!$C:$C, 0)) - $E12 + $B12)...`
- **G13**: `=IF($E13="","", DEGREES(ATAN((INDEX(Calc!$E:$E, MATCH("KminusZ_m", Calc!$C:$C, 0)) - $E13 + $B13)...`
- **G14**: `=IF($E14="","", DEGREES(ATAN((INDEX(Calc!$E:$E, MATCH("KminusZ_m", Calc!$C:$C, 0)) - $E14 + $B14)...`
- **G15**: `=IF($E15="","", DEGREES(ATAN((INDEX(Calc!$E:$E, MATCH("KminusZ_m", Calc!$C:$C, 0)) - $E15 + $B15)...`
- **G16**: `=IF($E16="","", DEGREES(ATAN((INDEX(Calc!$E:$E, MATCH("KminusZ_m", Calc!$C:$C, 0)) - $E16 + $B16)...`
- **G17**: `=IF($E17="","", DEGREES(ATAN((INDEX(Calc!$E:$E, MATCH("KminusZ_m", Calc!$C:$C, 0)) - $E17 + $B17)...`
- **G18**: `=IF($E18="","", DEGREES(ATAN((INDEX(Calc!$E:$E, MATCH("KminusZ_m", Calc!$C:$C, 0)) - $E18 + $B18)...`
- **G19**: `=IF($E19="","", DEGREES(ATAN((INDEX(Calc!$E:$E, MATCH("KminusZ_m", Calc!$C:$C, 0)) - $E19 + $B19)...`
- **G20**: `=IF($E20="","", DEGREES(ATAN((INDEX(Calc!$E:$E, MATCH("KminusZ_m", Calc!$C:$C, 0)) - $E20 + $B20)...`
- **G21**: `=IF($E21="","", DEGREES(ATAN((INDEX(Calc!$E:$E, MATCH("KminusZ_m", Calc!$C:$C, 0)) - $E21 + $B21)...`
- *... 외 724개 셀에서 사용됨*

#### IF (사용 7440회)

**셀 위치 및 수식**:

- **A2**: `=IF(December_Tide_2025!A2="","",December_Tide_2025!A2)`
- **B2**: `=IF(December_Tide_2025!B2="","",December_Tide_2025!B2)`
- **C2**: `=IF($A2="","", INDEX(Calc!$E:$E, MATCH("KminusZ_m", Calc!$C:$C, 0)) + $B2 - INDEX(Calc!$E:$E, MAT...`
- **E2**: `=IF($C2="","", IF($D2="", $C2, $C2 - $D2/2))`
- **F2**: `=IF($C2="","", IF($D2="", $C2, $C2 + $D2/2))`
- **G2**: `=IF($E2="","", DEGREES(ATAN((INDEX(Calc!$E:$E, MATCH("KminusZ_m", Calc!$C:$C, 0)) - $E2 + $B2) / ...`
- **H2**: `=IF($E2="","", IF(AND($E2>=INDEX(Calc!$E:$E, MATCH("min_fwd_draft_m", Calc!$C:$C, 0)), $E2<=INDEX...`
- **I2**: `=IF($E2="","", INDEX(Calc!$E:$E, MATCH("D_vessel_m", Calc!$C:$C, 0)) - $E2 + $B2)`
- **J2**: `=IF($F2="","", INDEX(Calc!$E:$E, MATCH("D_vessel_m", Calc!$C:$C, 0)) - $F2 + $B2)`
- **K2**: `=IF(D2=0, "Even Keel", "")`
- **A3**: `=IF(December_Tide_2025!A3="","",December_Tide_2025!A3)`
- **B3**: `=IF(December_Tide_2025!B3="","",December_Tide_2025!B3)`
- **C3**: `=IF($A3="","", INDEX(Calc!$E:$E, MATCH("KminusZ_m", Calc!$C:$C, 0)) + $B3 - INDEX(Calc!$E:$E, MAT...`
- **E3**: `=IF($C3="","", IF($D3="", $C3, $C3 - $D3/2))`
- **F3**: `=IF($C3="","", IF($D3="", $C3, $C3 + $D3/2))`
- **G3**: `=IF($E3="","", DEGREES(ATAN((INDEX(Calc!$E:$E, MATCH("KminusZ_m", Calc!$C:$C, 0)) - $E3 + $B3) / ...`
- **H3**: `=IF($E3="","", IF(AND($E3>=INDEX(Calc!$E:$E, MATCH("min_fwd_draft_m", Calc!$C:$C, 0)), $E3<=INDEX...`
- **I3**: `=IF($E3="","", INDEX(Calc!$E:$E, MATCH("D_vessel_m", Calc!$C:$C, 0)) - $E3 + $B3)`
- **J3**: `=IF($F3="","", INDEX(Calc!$E:$E, MATCH("D_vessel_m", Calc!$C:$C, 0)) - $F3 + $B3)`
- **K3**: `=IF(D3=0, "Even Keel", "")`
- *... 외 7420개 셀에서 사용됨*

#### INDEX (사용 3720회)

**셀 위치 및 수식**:

- **C2**: `=IF($A2="","", INDEX(Calc!$E:$E, MATCH("KminusZ_m", Calc!$C:$C, 0)) + $B2 - INDEX(Calc!$E:$E, MAT...`
- **G2**: `=IF($E2="","", DEGREES(ATAN((INDEX(Calc!$E:$E, MATCH("KminusZ_m", Calc!$C:$C, 0)) - $E2 + $B2) / ...`
- **H2**: `=IF($E2="","", IF(AND($E2>=INDEX(Calc!$E:$E, MATCH("min_fwd_draft_m", Calc!$C:$C, 0)), $E2<=INDEX...`
- **I2**: `=IF($E2="","", INDEX(Calc!$E:$E, MATCH("D_vessel_m", Calc!$C:$C, 0)) - $E2 + $B2)`
- **J2**: `=IF($F2="","", INDEX(Calc!$E:$E, MATCH("D_vessel_m", Calc!$C:$C, 0)) - $F2 + $B2)`
- **C3**: `=IF($A3="","", INDEX(Calc!$E:$E, MATCH("KminusZ_m", Calc!$C:$C, 0)) + $B3 - INDEX(Calc!$E:$E, MAT...`
- **G3**: `=IF($E3="","", DEGREES(ATAN((INDEX(Calc!$E:$E, MATCH("KminusZ_m", Calc!$C:$C, 0)) - $E3 + $B3) / ...`
- **H3**: `=IF($E3="","", IF(AND($E3>=INDEX(Calc!$E:$E, MATCH("min_fwd_draft_m", Calc!$C:$C, 0)), $E3<=INDEX...`
- **I3**: `=IF($E3="","", INDEX(Calc!$E:$E, MATCH("D_vessel_m", Calc!$C:$C, 0)) - $E3 + $B3)`
- **J3**: `=IF($F3="","", INDEX(Calc!$E:$E, MATCH("D_vessel_m", Calc!$C:$C, 0)) - $F3 + $B3)`
- **C4**: `=IF($A4="","", INDEX(Calc!$E:$E, MATCH("KminusZ_m", Calc!$C:$C, 0)) + $B4 - INDEX(Calc!$E:$E, MAT...`
- **G4**: `=IF($E4="","", DEGREES(ATAN((INDEX(Calc!$E:$E, MATCH("KminusZ_m", Calc!$C:$C, 0)) - $E4 + $B4) / ...`
- **H4**: `=IF($E4="","", IF(AND($E4>=INDEX(Calc!$E:$E, MATCH("min_fwd_draft_m", Calc!$C:$C, 0)), $E4<=INDEX...`
- **I4**: `=IF($E4="","", INDEX(Calc!$E:$E, MATCH("D_vessel_m", Calc!$C:$C, 0)) - $E4 + $B4)`
- **J4**: `=IF($F4="","", INDEX(Calc!$E:$E, MATCH("D_vessel_m", Calc!$C:$C, 0)) - $F4 + $B4)`
- **C5**: `=IF($A5="","", INDEX(Calc!$E:$E, MATCH("KminusZ_m", Calc!$C:$C, 0)) + $B5 - INDEX(Calc!$E:$E, MAT...`
- **G5**: `=IF($E5="","", DEGREES(ATAN((INDEX(Calc!$E:$E, MATCH("KminusZ_m", Calc!$C:$C, 0)) - $E5 + $B5) / ...`
- **H5**: `=IF($E5="","", IF(AND($E5>=INDEX(Calc!$E:$E, MATCH("min_fwd_draft_m", Calc!$C:$C, 0)), $E5<=INDEX...`
- **I5**: `=IF($E5="","", INDEX(Calc!$E:$E, MATCH("D_vessel_m", Calc!$C:$C, 0)) - $E5 + $B5)`
- **J5**: `=IF($F5="","", INDEX(Calc!$E:$E, MATCH("D_vessel_m", Calc!$C:$C, 0)) - $F5 + $B5)`
- *... 외 3700개 셀에서 사용됨*

#### MATCH (사용 3720회)

**셀 위치 및 수식**:

- **C2**: `=IF($A2="","", INDEX(Calc!$E:$E, MATCH("KminusZ_m", Calc!$C:$C, 0)) + $B2 - INDEX(Calc!$E:$E, MAT...`
- **G2**: `=IF($E2="","", DEGREES(ATAN((INDEX(Calc!$E:$E, MATCH("KminusZ_m", Calc!$C:$C, 0)) - $E2 + $B2) / ...`
- **H2**: `=IF($E2="","", IF(AND($E2>=INDEX(Calc!$E:$E, MATCH("min_fwd_draft_m", Calc!$C:$C, 0)), $E2<=INDEX...`
- **I2**: `=IF($E2="","", INDEX(Calc!$E:$E, MATCH("D_vessel_m", Calc!$C:$C, 0)) - $E2 + $B2)`
- **J2**: `=IF($F2="","", INDEX(Calc!$E:$E, MATCH("D_vessel_m", Calc!$C:$C, 0)) - $F2 + $B2)`
- **C3**: `=IF($A3="","", INDEX(Calc!$E:$E, MATCH("KminusZ_m", Calc!$C:$C, 0)) + $B3 - INDEX(Calc!$E:$E, MAT...`
- **G3**: `=IF($E3="","", DEGREES(ATAN((INDEX(Calc!$E:$E, MATCH("KminusZ_m", Calc!$C:$C, 0)) - $E3 + $B3) / ...`
- **H3**: `=IF($E3="","", IF(AND($E3>=INDEX(Calc!$E:$E, MATCH("min_fwd_draft_m", Calc!$C:$C, 0)), $E3<=INDEX...`
- **I3**: `=IF($E3="","", INDEX(Calc!$E:$E, MATCH("D_vessel_m", Calc!$C:$C, 0)) - $E3 + $B3)`
- **J3**: `=IF($F3="","", INDEX(Calc!$E:$E, MATCH("D_vessel_m", Calc!$C:$C, 0)) - $F3 + $B3)`
- **C4**: `=IF($A4="","", INDEX(Calc!$E:$E, MATCH("KminusZ_m", Calc!$C:$C, 0)) + $B4 - INDEX(Calc!$E:$E, MAT...`
- **G4**: `=IF($E4="","", DEGREES(ATAN((INDEX(Calc!$E:$E, MATCH("KminusZ_m", Calc!$C:$C, 0)) - $E4 + $B4) / ...`
- **H4**: `=IF($E4="","", IF(AND($E4>=INDEX(Calc!$E:$E, MATCH("min_fwd_draft_m", Calc!$C:$C, 0)), $E4<=INDEX...`
- **I4**: `=IF($E4="","", INDEX(Calc!$E:$E, MATCH("D_vessel_m", Calc!$C:$C, 0)) - $E4 + $B4)`
- **J4**: `=IF($F4="","", INDEX(Calc!$E:$E, MATCH("D_vessel_m", Calc!$C:$C, 0)) - $F4 + $B4)`
- **C5**: `=IF($A5="","", INDEX(Calc!$E:$E, MATCH("KminusZ_m", Calc!$C:$C, 0)) + $B5 - INDEX(Calc!$E:$E, MAT...`
- **G5**: `=IF($E5="","", DEGREES(ATAN((INDEX(Calc!$E:$E, MATCH("KminusZ_m", Calc!$C:$C, 0)) - $E5 + $B5) / ...`
- **H5**: `=IF($E5="","", IF(AND($E5>=INDEX(Calc!$E:$E, MATCH("min_fwd_draft_m", Calc!$C:$C, 0)), $E5<=INDEX...`
- **I5**: `=IF($E5="","", INDEX(Calc!$E:$E, MATCH("D_vessel_m", Calc!$C:$C, 0)) - $E5 + $B5)`
- **J5**: `=IF($F5="","", INDEX(Calc!$E:$E, MATCH("D_vessel_m", Calc!$C:$C, 0)) - $F5 + $B5)`
- *... 외 3700개 셀에서 사용됨*

#### RADIANS (사용 744회)

**셀 위치 및 수식**:

- **C2**: `=IF($A2="","", INDEX(Calc!$E:$E, MATCH("KminusZ_m", Calc!$C:$C, 0)) + $B2 - INDEX(Calc!$E:$E, MAT...`
- **C3**: `=IF($A3="","", INDEX(Calc!$E:$E, MATCH("KminusZ_m", Calc!$C:$C, 0)) + $B3 - INDEX(Calc!$E:$E, MAT...`
- **C4**: `=IF($A4="","", INDEX(Calc!$E:$E, MATCH("KminusZ_m", Calc!$C:$C, 0)) + $B4 - INDEX(Calc!$E:$E, MAT...`
- **C5**: `=IF($A5="","", INDEX(Calc!$E:$E, MATCH("KminusZ_m", Calc!$C:$C, 0)) + $B5 - INDEX(Calc!$E:$E, MAT...`
- **C6**: `=IF($A6="","", INDEX(Calc!$E:$E, MATCH("KminusZ_m", Calc!$C:$C, 0)) + $B6 - INDEX(Calc!$E:$E, MAT...`
- **C7**: `=IF($A7="","", INDEX(Calc!$E:$E, MATCH("KminusZ_m", Calc!$C:$C, 0)) + $B7 - INDEX(Calc!$E:$E, MAT...`
- **C8**: `=IF($A8="","", INDEX(Calc!$E:$E, MATCH("KminusZ_m", Calc!$C:$C, 0)) + $B8 - INDEX(Calc!$E:$E, MAT...`
- **C9**: `=IF($A9="","", INDEX(Calc!$E:$E, MATCH("KminusZ_m", Calc!$C:$C, 0)) + $B9 - INDEX(Calc!$E:$E, MAT...`
- **C10**: `=IF($A10="","", INDEX(Calc!$E:$E, MATCH("KminusZ_m", Calc!$C:$C, 0)) + $B10 - INDEX(Calc!$E:$E, M...`
- **C11**: `=IF($A11="","", INDEX(Calc!$E:$E, MATCH("KminusZ_m", Calc!$C:$C, 0)) + $B11 - INDEX(Calc!$E:$E, M...`
- **C12**: `=IF($A12="","", INDEX(Calc!$E:$E, MATCH("KminusZ_m", Calc!$C:$C, 0)) + $B12 - INDEX(Calc!$E:$E, M...`
- **C13**: `=IF($A13="","", INDEX(Calc!$E:$E, MATCH("KminusZ_m", Calc!$C:$C, 0)) + $B13 - INDEX(Calc!$E:$E, M...`
- **C14**: `=IF($A14="","", INDEX(Calc!$E:$E, MATCH("KminusZ_m", Calc!$C:$C, 0)) + $B14 - INDEX(Calc!$E:$E, M...`
- **C15**: `=IF($A15="","", INDEX(Calc!$E:$E, MATCH("KminusZ_m", Calc!$C:$C, 0)) + $B15 - INDEX(Calc!$E:$E, M...`
- **C16**: `=IF($A16="","", INDEX(Calc!$E:$E, MATCH("KminusZ_m", Calc!$C:$C, 0)) + $B16 - INDEX(Calc!$E:$E, M...`
- **C17**: `=IF($A17="","", INDEX(Calc!$E:$E, MATCH("KminusZ_m", Calc!$C:$C, 0)) + $B17 - INDEX(Calc!$E:$E, M...`
- **C18**: `=IF($A18="","", INDEX(Calc!$E:$E, MATCH("KminusZ_m", Calc!$C:$C, 0)) + $B18 - INDEX(Calc!$E:$E, M...`
- **C19**: `=IF($A19="","", INDEX(Calc!$E:$E, MATCH("KminusZ_m", Calc!$C:$C, 0)) + $B19 - INDEX(Calc!$E:$E, M...`
- **C20**: `=IF($A20="","", INDEX(Calc!$E:$E, MATCH("KminusZ_m", Calc!$C:$C, 0)) + $B20 - INDEX(Calc!$E:$E, M...`
- **C21**: `=IF($A21="","", INDEX(Calc!$E:$E, MATCH("KminusZ_m", Calc!$C:$C, 0)) + $B21 - INDEX(Calc!$E:$E, M...`
- *... 외 724개 셀에서 사용됨*

#### TAN (사용 744회)

**셀 위치 및 수식**:

- **C2**: `=IF($A2="","", INDEX(Calc!$E:$E, MATCH("KminusZ_m", Calc!$C:$C, 0)) + $B2 - INDEX(Calc!$E:$E, MAT...`
- **C3**: `=IF($A3="","", INDEX(Calc!$E:$E, MATCH("KminusZ_m", Calc!$C:$C, 0)) + $B3 - INDEX(Calc!$E:$E, MAT...`
- **C4**: `=IF($A4="","", INDEX(Calc!$E:$E, MATCH("KminusZ_m", Calc!$C:$C, 0)) + $B4 - INDEX(Calc!$E:$E, MAT...`
- **C5**: `=IF($A5="","", INDEX(Calc!$E:$E, MATCH("KminusZ_m", Calc!$C:$C, 0)) + $B5 - INDEX(Calc!$E:$E, MAT...`
- **C6**: `=IF($A6="","", INDEX(Calc!$E:$E, MATCH("KminusZ_m", Calc!$C:$C, 0)) + $B6 - INDEX(Calc!$E:$E, MAT...`
- **C7**: `=IF($A7="","", INDEX(Calc!$E:$E, MATCH("KminusZ_m", Calc!$C:$C, 0)) + $B7 - INDEX(Calc!$E:$E, MAT...`
- **C8**: `=IF($A8="","", INDEX(Calc!$E:$E, MATCH("KminusZ_m", Calc!$C:$C, 0)) + $B8 - INDEX(Calc!$E:$E, MAT...`
- **C9**: `=IF($A9="","", INDEX(Calc!$E:$E, MATCH("KminusZ_m", Calc!$C:$C, 0)) + $B9 - INDEX(Calc!$E:$E, MAT...`
- **C10**: `=IF($A10="","", INDEX(Calc!$E:$E, MATCH("KminusZ_m", Calc!$C:$C, 0)) + $B10 - INDEX(Calc!$E:$E, M...`
- **C11**: `=IF($A11="","", INDEX(Calc!$E:$E, MATCH("KminusZ_m", Calc!$C:$C, 0)) + $B11 - INDEX(Calc!$E:$E, M...`
- **C12**: `=IF($A12="","", INDEX(Calc!$E:$E, MATCH("KminusZ_m", Calc!$C:$C, 0)) + $B12 - INDEX(Calc!$E:$E, M...`
- **C13**: `=IF($A13="","", INDEX(Calc!$E:$E, MATCH("KminusZ_m", Calc!$C:$C, 0)) + $B13 - INDEX(Calc!$E:$E, M...`
- **C14**: `=IF($A14="","", INDEX(Calc!$E:$E, MATCH("KminusZ_m", Calc!$C:$C, 0)) + $B14 - INDEX(Calc!$E:$E, M...`
- **C15**: `=IF($A15="","", INDEX(Calc!$E:$E, MATCH("KminusZ_m", Calc!$C:$C, 0)) + $B15 - INDEX(Calc!$E:$E, M...`
- **C16**: `=IF($A16="","", INDEX(Calc!$E:$E, MATCH("KminusZ_m", Calc!$C:$C, 0)) + $B16 - INDEX(Calc!$E:$E, M...`
- **C17**: `=IF($A17="","", INDEX(Calc!$E:$E, MATCH("KminusZ_m", Calc!$C:$C, 0)) + $B17 - INDEX(Calc!$E:$E, M...`
- **C18**: `=IF($A18="","", INDEX(Calc!$E:$E, MATCH("KminusZ_m", Calc!$C:$C, 0)) + $B18 - INDEX(Calc!$E:$E, M...`
- **C19**: `=IF($A19="","", INDEX(Calc!$E:$E, MATCH("KminusZ_m", Calc!$C:$C, 0)) + $B19 - INDEX(Calc!$E:$E, M...`
- **C20**: `=IF($A20="","", INDEX(Calc!$E:$E, MATCH("KminusZ_m", Calc!$C:$C, 0)) + $B20 - INDEX(Calc!$E:$E, M...`
- **C21**: `=IF($A21="","", INDEX(Calc!$E:$E, MATCH("KminusZ_m", Calc!$C:$C, 0)) + $B21 - INDEX(Calc!$E:$E, M...`
- *... 외 724개 셀에서 사용됨*

---

### RORO_Stage_Scenarios

**시트 정보**: 29행 × 16열, 수식 55개

#### ABS (사용 10회)

**셀 위치 및 수식**:

- **L15**: `=IF(G15="","", IF(ABS(G15)<=($F$8/50), "OK", "EXCESSIVE"))`
- **M15**: `=IF(OR(G15="",OR($C$10="", $C$10=0)),"", ROUND(ABS(G15) * 50 * $C$10, 2))`
- **L16**: `=IF(G16="","", IF(ABS(G16)<=($F$8/50), "OK", "EXCESSIVE"))`
- **M16**: `=IF(OR(G16="",OR($C$10="", $C$10=0)),"", ROUND(ABS(G16) * 50 * $C$10, 2))`
- **L17**: `=IF(G17="","", IF(ABS(G17)<=($F$8/50), "OK", "EXCESSIVE"))`
- **M17**: `=IF(OR(G17="",OR($C$10="", $C$10=0)),"", ROUND(ABS(G17) * 50 * $C$10, 2))`
- **L18**: `=IF(G18="","", IF(ABS(G18)<=($F$8/50), "OK", "EXCESSIVE"))`
- **M18**: `=IF(OR(G18="",OR($C$10="", $C$10=0)),"", ROUND(ABS(G18) * 50 * $C$10, 2))`
- **L19**: `=IF(G19="","", IF(ABS(G19)<=($F$8/50), "OK", "EXCESSIVE"))`
- **M19**: `=IF(OR(G19="",OR($C$10="", $C$10=0)),"", ROUND(ABS(G19) * 50 * $C$10, 2))`

#### IF (사용 50회)

**셀 위치 및 수식**:

- **E15**: `=IF(OR(C15="",D15=""),"", C15*(D15-$C$9))`
- **F15**: `=IF(OR(E15="",OR($C$8="", $C$8=0)),"", E15/$C$8)`
- **G15**: `=IF(F15="","",F15/100)`
- **H15**: `=IF(OR($D$5="",G15=""),"", $D$5 - G15/2)`
- **I15**: `=IF(OR($D$5="",G15=""),"", $D$5 + G15/2)`
- **J15**: `=IF(H15="","", $F$9 - H15 + $G$5)`
- **K15**: `=IF(I15="","", $F$9 - I15 + $G$5)`
- **L15**: `=IF(G15="","", IF(ABS(G15)<=($F$8/50), "OK", "EXCESSIVE"))`
- **M15**: `=IF(OR(G15="",OR($C$10="", $C$10=0)),"", ROUND(ABS(G15) * 50 * $C$10, 2))`
- **N15**: `=IF(OR(M15="",OR($C$11="", $C$11=0)),"", ROUND(M15/$C$11, 2))`
- **E16**: `=IF(OR(C16="",D16=""),"", C16*(D16-$C$9))`
- **F16**: `=IF(OR(E16="",OR($C$8="", $C$8=0)),"", E16/$C$8)`
- **G16**: `=IF(F16="","",F16/100)`
- **H16**: `=IF(OR($D$5="",G16=""),"", $D$5 - G16/2)`
- **I16**: `=IF(OR($D$5="",G16=""),"", $D$5 + G16/2)`
- **J16**: `=IF(H16="","", $F$9 - H16 + $G$5)`
- **K16**: `=IF(I16="","", $F$9 - I16 + $G$5)`
- **L16**: `=IF(G16="","", IF(ABS(G16)<=($F$8/50), "OK", "EXCESSIVE"))`
- **M16**: `=IF(OR(G16="",OR($C$10="", $C$10=0)),"", ROUND(ABS(G16) * 50 * $C$10, 2))`
- **N16**: `=IF(OR(M16="",OR($C$11="", $C$11=0)),"", ROUND(M16/$C$11, 2))`
- *... 외 30개 셀에서 사용됨*

#### INDEX (사용 5회)

**셀 위치 및 수식**:

- **C8**: `=INDEX(Calc!$E:$E, MATCH("MTC_t_m_per_cm", Calc!$C:$C, 0))`
- **F8**: `=INDEX(Calc!$E:$E, MATCH("Lpp_m", Calc!$C:$C, 0))`
- **C9**: `=INDEX(Calc!$E:$E, MATCH("LCF_m_from_midship", Calc!$C:$C, 0))`
- **F9**: `=INDEX(Calc!$E:$E, MATCH("D_vessel_m", Calc!$C:$C, 0))`
- **C10**: `=INDEX(Calc!$E:$E, MATCH("TPC_t_per_cm", Calc!$C:$C, 0))`

#### MATCH (사용 5회)

**셀 위치 및 수식**:

- **C8**: `=INDEX(Calc!$E:$E, MATCH("MTC_t_m_per_cm", Calc!$C:$C, 0))`
- **F8**: `=INDEX(Calc!$E:$E, MATCH("Lpp_m", Calc!$C:$C, 0))`
- **C9**: `=INDEX(Calc!$E:$E, MATCH("LCF_m_from_midship", Calc!$C:$C, 0))`
- **F9**: `=INDEX(Calc!$E:$E, MATCH("D_vessel_m", Calc!$C:$C, 0))`
- **C10**: `=INDEX(Calc!$E:$E, MATCH("TPC_t_per_cm", Calc!$C:$C, 0))`

#### OR (사용 30회)

**셀 위치 및 수식**:

- **E15**: `=IF(OR(C15="",D15=""),"", C15*(D15-$C$9))`
- **F15**: `=IF(OR(E15="",OR($C$8="", $C$8=0)),"", E15/$C$8)`
- **H15**: `=IF(OR($D$5="",G15=""),"", $D$5 - G15/2)`
- **I15**: `=IF(OR($D$5="",G15=""),"", $D$5 + G15/2)`
- **M15**: `=IF(OR(G15="",OR($C$10="", $C$10=0)),"", ROUND(ABS(G15) * 50 * $C$10, 2))`
- **N15**: `=IF(OR(M15="",OR($C$11="", $C$11=0)),"", ROUND(M15/$C$11, 2))`
- **E16**: `=IF(OR(C16="",D16=""),"", C16*(D16-$C$9))`
- **F16**: `=IF(OR(E16="",OR($C$8="", $C$8=0)),"", E16/$C$8)`
- **H16**: `=IF(OR($D$5="",G16=""),"", $D$5 - G16/2)`
- **I16**: `=IF(OR($D$5="",G16=""),"", $D$5 + G16/2)`
- **M16**: `=IF(OR(G16="",OR($C$10="", $C$10=0)),"", ROUND(ABS(G16) * 50 * $C$10, 2))`
- **N16**: `=IF(OR(M16="",OR($C$11="", $C$11=0)),"", ROUND(M16/$C$11, 2))`
- **E17**: `=IF(OR(C17="",D17=""),"", C17*(D17-$C$9))`
- **F17**: `=IF(OR(E17="",OR($C$8="", $C$8=0)),"", E17/$C$8)`
- **H17**: `=IF(OR($D$5="",G17=""),"", $D$5 - G17/2)`
- **I17**: `=IF(OR($D$5="",G17=""),"", $D$5 + G17/2)`
- **M17**: `=IF(OR(G17="",OR($C$10="", $C$10=0)),"", ROUND(ABS(G17) * 50 * $C$10, 2))`
- **N17**: `=IF(OR(M17="",OR($C$11="", $C$11=0)),"", ROUND(M17/$C$11, 2))`
- **E18**: `=IF(OR(C18="",D18=""),"", C18*(D18-$C$9))`
- **F18**: `=IF(OR(E18="",OR($C$8="", $C$8=0)),"", E18/$C$8)`
- *... 외 10개 셀에서 사용됨*

#### ROUND (사용 10회)

**셀 위치 및 수식**:

- **M15**: `=IF(OR(G15="",OR($C$10="", $C$10=0)),"", ROUND(ABS(G15) * 50 * $C$10, 2))`
- **N15**: `=IF(OR(M15="",OR($C$11="", $C$11=0)),"", ROUND(M15/$C$11, 2))`
- **M16**: `=IF(OR(G16="",OR($C$10="", $C$10=0)),"", ROUND(ABS(G16) * 50 * $C$10, 2))`
- **N16**: `=IF(OR(M16="",OR($C$11="", $C$11=0)),"", ROUND(M16/$C$11, 2))`
- **M17**: `=IF(OR(G17="",OR($C$10="", $C$10=0)),"", ROUND(ABS(G17) * 50 * $C$10, 2))`
- **N17**: `=IF(OR(M17="",OR($C$11="", $C$11=0)),"", ROUND(M17/$C$11, 2))`
- **M18**: `=IF(OR(G18="",OR($C$10="", $C$10=0)),"", ROUND(ABS(G18) * 50 * $C$10, 2))`
- **N18**: `=IF(OR(M18="",OR($C$11="", $C$11=0)),"", ROUND(M18/$C$11, 2))`
- **M19**: `=IF(OR(G19="",OR($C$10="", $C$10=0)),"", ROUND(ABS(G19) * 50 * $C$10, 2))`
- **N19**: `=IF(OR(M19="",OR($C$11="", $C$11=0)),"", ROUND(M19/$C$11, 2))`

---

## 함수별 전체 사용 현황

전체 워크북에서 각 함수가 사용된 횟수와 시트별 분포입니다.

| 함수명 | 총 사용 횟수 | 사용 시트 수 | 시트별 분포 |
|--------|-------------|-------------|------------|
| IF | 7490 | 2 | Hourly_FWD_AFT_Heights: 7440회, RORO_Stage_Scenarios: 50회 |
| INDEX | 3725 | 2 | Hourly_FWD_AFT_Heights: 3720회, RORO_Stage_Scenarios: 5회 |
| MATCH | 3725 | 2 | Hourly_FWD_AFT_Heights: 3720회, RORO_Stage_Scenarios: 5회 |
| TAN | 744 | 1 | Hourly_FWD_AFT_Heights: 744회 |
| RADIANS | 744 | 1 | Hourly_FWD_AFT_Heights: 744회 |
| DEGREES | 744 | 1 | Hourly_FWD_AFT_Heights: 744회 |
| ATAN | 744 | 1 | Hourly_FWD_AFT_Heights: 744회 |
| AND | 744 | 1 | Hourly_FWD_AFT_Heights: 744회 |
| OR | 30 | 1 | RORO_Stage_Scenarios: 30회 |
| ABS | 10 | 1 | RORO_Stage_Scenarios: 10회 |
| ROUND | 10 | 1 | RORO_Stage_Scenarios: 10회 |

## 참고사항

### 특수 수식 패턴

- **배열 수식**: 없음

### 함수 분류

- **수학/삼각**: ABS, ROUND
- **논리**: AND, IF, OR
- **조회/참조**: INDEX, MATCH
- **기타**: ATAN, DEGREES, RADIANS, TAN

---

*이 문서는 2025-11-13T04:31:24.920105에 자동 생성되었습니다.*