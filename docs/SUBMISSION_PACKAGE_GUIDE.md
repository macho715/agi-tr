# LCT BUSHRA - Submission Package Guide

**Document:** Submission Package Structure & Guidelines  
**Version:** 1.0  
**Date:** 2025-11-06  
**Project:** HVDC Transformer Transportation  
**Purpose:** Harbor Master / Port Authority Submission  

---

## Quick Start

### Prerequisites
```bash
# Ensure you have run patch3.py first
cd C:\Users\SAMSUNG\Downloads\KZ_measurement_note\scripts
python patch3.py

# This generates: LCT_BUSHRA_Package_RORO_FIXED.xlsx
```

### Generate Submission Package
```bash
# Install dependencies (if not already installed)
pip install openpyxl matplotlib

# Run package generator
python generate_submission_package.py
```

### Output Structure
```
SUBMISSION_PACKAGE/
├── 01_PDF_Report/
│   └── LCT_BUSHRA_FWD_AFT_Report.pdf     ← Primary submission document
├── 02_Working_Excel/
│   └── LCT_BUSHRA_Calculator_LOCKED.xlsx  ← Reference calculator
├── 03_Supporting_Documents/
│   ├── KZ_Measurement_Record_TEMPLATE.txt
│   ├── Tide_Data_Source_Declaration_TEMPLATE.txt
│   └── Submission_Checklist.txt
└── README.txt                             ← Package instructions
```

---

## 1. PDF Report (Primary Submission)

### 1.1 Document Overview

**Filename:** `LCT_BUSHRA_FWD_AFT_Report.pdf`  
**Pages:** 1-2 (depending on data range)  
**Format:** A4 Landscape (11.69" × 8.27")  
**Purpose:** Official submission to Harbor Master for RORO operation approval

### 1.2 Content Structure

#### Page 1 (Mandatory)

**Header Section:**
- Vessel name and IMO number
- Project name and route
- Preparation date and responsible party
- Approval signature blocks

**Critical Parameters Box:**
```
┌─────────────────────────────────────────┐
│ K–Z Distance: [X.XX] m (site measured)  │
│ Linkspan Length: 12.0 m                 │
│ Maximum Ramp Angle: 6.0° (HM limit)     │
│ Vessel Molded Depth: 3.65 m (LCT Bushra actual depth, corrected from 4.85m) │
│ Length Between Perpendiculars: 64.0 m   │
└─────────────────────────────────────────┘
```

**Hourly Schedule Table (First 24 hours):**

| Column | Description | Example |
|--------|-------------|---------|
| Time (GST) | Date and time in Gulf Standard Time | 12-01 00:00 |
| Tide (m) | Tidal height above Chart Datum | 2.06 |
| Dfwd_req (m) | Required forward draft (even-keel) | 8.06 |
| Trim (m) | Applied trim (if any) | 0.00 or -0.50 |
| Dfwd_adj (m) | Adjusted forward draft | 8.06 |
| Daft_adj (m) | Adjusted aft draft | 8.06 |
| Ramp∠ (deg) | Calculated ramp angle | 4.2 |
| Status | OK / CHECK indicator | OK |
| Notes | Operational notes | Even-keel |

**Color Coding:**
- 🟢 Green: Status = "OK" (safe for operations)
- 🟡 Yellow: Status = "CHECK" (requires verification)

#### Page 2 (If needed)

**Continued Schedule (Hours 25-48):**
- Same table structure as Page 1
- Covers additional operational hours

**Approval Section:**
```
Prepared by: _________________
Signature: __________  Date: __________

Reviewed by (Chief Officer): _________________
Signature: __________  Date: __________

Harbor Master Approval:
Signature: __________  Date: __________
```

### 1.3 Usage Guidelines

**For Harbor Master Submission:**
1. Print in color for clear status indication
2. Obtain all required signatures before submission
3. Attach supporting documents (K-Z record, tide source)
4. Submit via official port authority channels

**For Internal Use:**
- Review with Chief Officer before submission
- Verify all calculations against stability booklet
- Cross-check with actual tide predictions
- Confirm all "OK" status for planned operation window

---

## 2. Working Excel (Reference Calculator)

### 2.1 Document Overview

**Filename:** `LCT_BUSHRA_Calculator_LOCKED.xlsx`  
**Protection:** Sheet-level protection with password  
**Password:** `BUSHRA2025`  
**Purpose:** Reference calculator for real-time adjustments and what-if scenarios

### 2.2 Protection Scheme

| Sheet | Protected | Editable Cells | Purpose |
|-------|-----------|----------------|---------|
| Calc | Yes | Yellow cells (D4-D16) | Update constants if needed |
| December_Tide_2025 | No | Column B (tide data) | Paste official tide values |
| Hourly_FWD_AFT_Heights | Yes | Column D (Trim input) | Apply trim adjustments |
| RORO_Stage_Scenarios | Yes | Columns B-C (W, x inputs) | Enter cargo details |
| README | No | N/A | Reference only |

### 2.3 Unprotecting Sheets

**If modifications needed:**
```excel
1. Right-click sheet tab
2. Select "Unprotect Sheet"
3. Enter password: BUSHRA2025
4. Make changes
5. Re-protect sheet (recommended)
```

**Caution:** Unprotecting formulas risks accidental changes. Only authorized personnel should unprotect sheets.

### 2.4 Real-Time Use During Operations

**Scenario: Tide deviates from prediction**
1. Open locked Excel file
2. Navigate to December_Tide_2025 sheet
3. Update tide value for current hour
4. Review Hourly_FWD_AFT_Heights sheet
5. Check Status column for "OK" confirmation
6. Proceed if status is acceptable

**Scenario: Need to apply trim adjustment**
1. Open Hourly_FWD_AFT_Heights sheet
2. Locate current hour row
3. Enter desired trim in Column D (yellow cell)
4. Verify FWD_Height and AFT_Height are acceptable
5. Check ramp angle ≤ 6°
6. Document trim reason in Notes column

---

## 3. Supporting Documents

### 3.1 K-Z Measurement Record

**Filename:** `KZ_Measurement_Record_TEMPLATE.txt`  
**Status:** Template - **MUST BE COMPLETED**  
**Purpose:** Document on-site measurement of K-Z distance

#### Required Information:

**Measurement Details:**
- Date and time of measurement (GST)
- Weather conditions
- Tide level at measurement time
- Surveyor name and credentials

**Measurements:**
- Jetty deck elevation above CD
- Linkspan contact point elevation
- Calculated K-Z distance
- Verification measurement (repeat reading)

**Photo Documentation (Minimum 3):**
1. Wide view of measurement setup
2. Close-up of contact point
3. Measuring equipment with reading visible

**Signatures:**
- Surveyor
- Chief Officer
- Harbor Master (if present)

#### Critical Notes:

⚠️ **Accuracy Requirement:** Measurement accuracy ±50mm  
⚠️ **Verification:** Repeat measurement must agree within 50mm  
⚠️ **Documentation:** Photos must clearly show measurement method  
⚠️ **Update:** Immediately update Calc!D6 in Excel after measurement

### 3.2 Tide Data Source Declaration

**Filename:** `Tide_Data_Source_Declaration_TEMPLATE.txt`  
**Status:** Template - **MUST BE COMPLETED**  
**Purpose:** Declare official source of tide predictions

#### Required Information:

**Source Details:**
- Official source name (AD Ports / ADNOC / Other)
- Document reference number
- Publication date
- Validity period
- Datum (Chart Datum or other)

**Data Characteristics:**
- Temporal resolution (hourly/other)
- Predicted vs. Observed
- Any corrections applied

**Verification:**
- Cross-check source
- Verifier name and signature

**Attachment:**
- Copy of original tide table (PDF/Excel)

#### Acceptable Sources:

✅ **Primary Sources:**
- Abu Dhabi Ports Authority (AD Ports)
- ADNOC Marine & Offshore Services
- UAE National Hydrographic Office

❌ **Unacceptable Sources:**
- Third-party websites (unless approved)
- Unofficial apps or software
- Outdated publications (>1 year old)

### 3.3 Submission Checklist

**Filename:** `Submission_Checklist.txt`  
**Purpose:** Master verification checklist for complete submission

#### Checklist Sections:

**1. Required Documents**
- [ ] PDF Report (LCT_BUSHRA_FWD_AFT_Report.pdf)
- [ ] Working Excel (optional reference)
- [ ] K-Z Measurement Record (completed)
- [ ] Tide Data Source Declaration (completed)
- [ ] Vessel documentation (Stability Booklet, etc.)

**2. Technical Verification**
- [ ] K-Z distance measured on site
- [ ] Linkspan specifications confirmed (12m)
- [ ] Max ramp angle ≤ 6° in all scenarios
- [ ] All "Status" cells show "OK" for operation window
- [ ] No "EXCESSIVE" trim warnings (or explained)
- [ ] Ballast operations feasible

**3. Operational Approval**
- [ ] Chief Officer review completed
- [ ] Samsung C&T approval obtained
- [ ] Harbor Master preliminary review

**4. Submission Method**
- [ ] Email to [port authority email]
- [ ] Physical copy delivered (if required)
- [ ] Online portal submission (if applicable)

---

## 4. Submission Workflow

### 4.1 Timeline

```
T-7 days:  Site survey and K-Z measurement
T-5 days:  Obtain official tide data
T-3 days:  Complete Excel calculations
T-2 days:  Generate PDF report and gather documents
T-1 day:   Internal review and approvals
T-0 day:   Submit to Harbor Master
```

### 4.2 Step-by-Step Process

#### Phase 1: Pre-Submission (T-7 to T-3)

**Step 1.1: Site Survey (T-7)**
```
□ Coordinate with port authority for berth access
□ Assemble measurement team (surveyor, chief officer, Samsung rep)
□ Conduct K-Z measurement following template procedure
□ Take photos (minimum 3, preferably 5-7)
□ Complete KZ_Measurement_Record_TEMPLATE.txt
□ Obtain all required signatures
```

**Step 1.2: Tide Data Acquisition (T-5)**
```
□ Request official tide predictions from AD Ports/ADNOC
□ Verify data covers full operational period (December 2025)
□ Check data format (Excel preferred for easy import)
□ Complete Tide_Data_Source_Declaration_TEMPLATE.txt
□ Attach copy of original tide table
```

**Step 1.3: Excel Update (T-3)**
```
□ Open LCT_BUSHRA_Package_RORO_FIXED.xlsx
□ Update Calc!D6 with measured K-Z value
□ Paste tide data into December_Tide_2025 sheet (B2:B745)
□ Review Hourly_FWD_AFT_Heights sheet
   - Identify "OK" operation windows
   - Note any "CHECK" status hours
   - Plan operations around favorable tides
□ (Optional) Fill RORO_Stage_Scenarios sheet
   - Enter cargo weights (W_stage_t)
   - Enter cargo positions (x_stage_m)
   - Review Trim_Check column
   - Note ballast requirements
□ Save updated file
```

#### Phase 2: Document Generation (T-2)

**Step 2.1: Generate Package**
```bash
cd C:\Users\SAMSUNG\Downloads\KZ_measurement_note\scripts
python generate_submission_package.py
```

**Step 2.2: Review PDF Report**
```
□ Verify K-Z value matches measurement record
□ Check all tables for #DIV/0! or #REF! errors
□ Confirm "OK" status for planned operation dates/times
□ Review ramp angles (all should be ≤ 6°)
□ Verify tide values match official source
```

**Step 2.3: Assemble Supporting Documents**
```
□ KZ_Measurement_Record_TEMPLATE.txt (completed, signed)
□ Photos of K-Z measurement (3+ images)
□ Tide_Data_Source_Declaration_TEMPLATE.txt (completed, signed)
□ Copy of official tide table
□ Vessel Stability Booklet (if required)
□ Certificate of Class (if required)
```

#### Phase 3: Internal Review (T-1)

**Step 3.1: Chief Officer Review**
```
□ Review PDF report for accuracy
□ Verify calculations against vessel's stability booklet
□ Confirm operational feasibility
□ Check ballast operation timeline
□ Sign approval section of PDF
```

**Step 3.2: Samsung C&T Review**
```
□ Verify project requirements met
□ Confirm schedule alignment with cargo operations
□ Review risk assessment
□ Obtain management approval
```

**Step 3.3: Final Verification**
```
□ Complete Submission_Checklist.txt
□ Verify all signatures obtained
□ Check all documents are legible
□ Prepare cover letter (if required)
```

#### Phase 4: Submission (T-0)

**Step 4.1: Package Assembly**
```
Primary Package:
├── Cover Letter (if required)
├── LCT_BUSHRA_FWD_AFT_Report.pdf (with signatures)
├── KZ_Measurement_Record (with photos)
└── Tide_Data_Source_Declaration (with original tide table)

Optional Reference:
└── LCT_BUSHRA_Calculator_LOCKED.xlsx
```

**Step 4.2: Submission Channels**

**Email Submission:**
```
To: [Harbor Master email]
Cc: [Port Authority, Samsung team]
Subject: RORO Operation Request - LCT BUSHRA - December 2025

Attach:
- LCT_BUSHRA_FWD_AFT_Report.pdf
- KZ_Measurement_Record.pdf (scanned)
- Tide_Data_Source_Declaration.pdf (scanned)
- Photos.zip (K-Z measurement photos)

Email body:
[Professional request with operation details]
```

**Physical Submission (if required):**
```
- Print PDF report in color
- Include original signed documents
- Bind in folder with cover page
- Deliver to port authority office
- Obtain receipt/acknowledgment
```

**Online Portal (if applicable):**
```
- Log into port authority system
- Upload required documents
- Fill online forms
- Submit for review
- Note confirmation number
```

### 4.3 Post-Submission

**Follow-Up Actions:**
```
□ Confirm receipt of submission
□ Note expected review timeline
□ Prepare for any clarification requests
□ Keep team informed of approval status
□ Plan contingency if revisions needed
```

**If Revisions Requested:**
```
1. Review Harbor Master comments carefully
2. Update Excel calculations if needed
3. Regenerate PDF report
4. Resubmit with cover letter explaining changes
5. Highlight what was modified
```

---

## 5. Common Issues & Resolutions

### 5.1 Excel-Related Issues

**Issue:** Formulas showing #DIV/0!  
**Cause:** TPC or MTC value is 0 or empty in Calc sheet  
**Resolution:** Verify Calc!D13 (MTC = 33.95) and Calc!D15 (TPC = 7.5)

**Issue:** K-Z value seems incorrect  
**Cause:** Measurement error or wrong datum reference  
**Resolution:** Re-measure K-Z with surveyor present; verify Chart Datum

**Issue:** All hours show "CHECK" status  
**Cause:** K-Z value not updated or extreme tide conditions  
**Resolution:** Ensure Calc!D6 updated with actual measurement

**Issue:** Tide data not displaying in tables  
**Cause:** Incorrect paste location or wrong format  
**Resolution:** Paste tide values into December_Tide_2025!B2:B745 (values only, not formulas)

### 5.2 PDF Generation Issues

**Issue:** PDF report is blank or shows errors  
**Cause:** Excel file not found or data missing  
**Resolution:** Ensure LCT_BUSHRA_Package_RORO_FIXED.xlsx is in same directory as script

**Issue:** Tables in PDF are cut off  
**Cause:** Data exceeds page boundaries  
**Resolution:** Script automatically paginates; check if matplotlib is updated

**Issue:** Colors not showing correctly  
**Cause:** PDF viewer doesn't support color  
**Resolution:** Open with Adobe Reader or update PDF viewer

### 5.3 Submission-Related Issues

**Issue:** Harbor Master requests additional information  
**Cause:** Missing supporting documents or unclear calculations  
**Resolution:** Provide requested documents; consider adding explanatory notes

**Issue:** K-Z measurement challenged  
**Cause:** Measurement method not clear or results questioned  
**Resolution:** Provide detailed measurement record with photos; offer to re-measure with HM present

**Issue:** Tide source not acceptable  
**Cause:** Source not official or data outdated  
**Resolution:** Obtain data from AD Ports or ADNOC directly; resubmit with proper declaration

---

## 6. Quality Assurance

### 6.1 Pre-Submission Verification Checklist

**Excel Workbook:**
- [ ] Calc!D6 (K-Z) = actual measured value (not 3.0 default)
- [ ] December_Tide_2025!B2:B745 populated with official data
- [ ] No #DIV/0!, #REF!, or #VALUE! errors anywhere
- [ ] Hourly_FWD_AFT_Heights shows "OK" for operation window
- [ ] RORO_Stage_Scenarios (if used) shows no "EXCESSIVE" trim

**PDF Report:**
- [ ] K-Z value matches measurement record
- [ ] All tables complete and readable
- [ ] Color coding clear (green = OK, yellow = CHECK)
- [ ] Signatures sections present
- [ ] Footer disclaimer present

**Supporting Documents:**
- [ ] K-Z measurement record complete with all fields filled
- [ ] Minimum 3 photos attached (clear and high-resolution)
- [ ] Tide data source declaration complete and signed
- [ ] Original tide table attached
- [ ] All signatures obtained

**Overall Package:**
- [ ] All files present in correct folders
- [ ] File names correct and consistent
- [ ] README.txt reviewed
- [ ] Submission checklist complete
- [ ] Cover letter prepared (if needed)

### 6.2 Calculation Spot-Check

**Manual Verification (Sample Hour):**
```
Select one representative hour and verify manually:

Example: 2025-12-01 12:00
□ Tide from official table: ______ m
□ Dfwd_req = K-Z + Tide - L_ramp × tan(θ_max)
  Calculated: ______ m
  Excel: ______ m
  Match? Yes □ No □

□ Ramp_Angle = arctan((K-Z - Dfwd + Tide) / L_ramp)
  Calculated: ______ deg
  Excel: ______ deg  
  Match? Yes □ No □

□ Angle ≤ 6°? Yes □ No □
□ Status = "OK"? Yes □ No □
```

If spot-check fails, review formulas in Excel before submission.

---

## 7. Contact & Support

### 7.1 Project Team

**Samsung C&T Logistics:**
- Coordinator: [Name, Email, Phone]
- Marine Operations: [Name, Email, Phone]
- Project Manager: [Name, Email, Phone]

**Vessel:**
- Master: [Name, Phone]
- Chief Officer: [Name, Phone]

**Port Authority:**
- Harbor Master: Mina Zayed Port, [Email, Phone]
- Port Operations: [Email, Phone]

**Technical Support:**
- MACHO-GPT System: [Contact details]
- Calculation Verification: [Technical team contact]

### 7.2 Emergency Contacts

**During Operations:**
- Samsung 24/7 Hotline: [Phone]
- Port Emergency: [Phone]
- Vessel VHF: Channel [__]

---

## 8. Document Control

**Version History:**

| Version | Date | Changes | Author |
|---------|------|---------|--------|
| 1.0 | 2025-11-06 | Initial submission package guide | MACHO-GPT |

**Review Schedule:**
- Next review: 2025-12-01 (post-operation debrief)
- Review frequency: After each project or annually

**Distribution:**
- Samsung C&T Logistics Team
- Vessel Master and Chief Officer
- Harbor Master (as part of submission)

---

## Appendix: Sample Email Templates

### A.1 Initial Submission Email

```
Subject: RORO Operation Request - LCT BUSHRA - December 2025

Dear Harbor Master,

Samsung C&T Engineering & Construction hereby requests approval for 
RORO (Roll-On/Roll-Off) operations for the vessel LCT BUSHRA at 
Mina Zayed Port during December 2025.

Operation Details:
- Vessel: LCT BUSHRA (IMO: [XXXXXXX])
- Operation: Loading HVDC transformer equipment
- Planned Period: December [XX-XX], 2025
- Berth: [Berth Number]

Attached Documents:
1. LCT_BUSHRA_FWD_AFT_Report.pdf (Official calculation report)
2. KZ_Measurement_Record.pdf (Site measurement documentation)
3. Tide_Data_Source_Declaration.pdf (Official tide data reference)
4. Photos.zip (K-Z measurement evidence)

Key Safety Confirmations:
- K-Z distance measured on-site: [X.XX] m
- Maximum ramp angle in all scenarios: [X.X]° (within 6° limit)
- All planned operation hours show "OK" status
- Tide data from official source: [AD Ports / ADNOC]

We respectfully request your review and approval for these operations.
Should you require any additional information or clarifications, please 
do not hesitate to contact us.

Best regards,
[Name]
[Position]
Samsung C&T Engineering & Construction
Email: [email]
Phone: [phone]
```

### A.2 Revision Resubmission Email

```
Subject: Re: RORO Operation Request - LCT BUSHRA - REVISED

Dear Harbor Master,

Thank you for your review of our initial submission and your feedback.

We have addressed your comments as follows:

1. [Comment 1]: [Explanation of how it was addressed]
2. [Comment 2]: [Explanation of how it was addressed]
3. [Comment 3]: [Explanation of how it was addressed]

Attached please find the revised submission package with the following 
updated documents:
- LCT_BUSHRA_FWD_AFT_Report_REVISED.pdf
- [Any other updated documents]

Changes have been highlighted in the revised PDF report for your convenience.

We believe these revisions fully address your concerns and maintain all 
required safety margins. We respectfully request your approval to proceed 
with operations.

Thank you for your attention to this matter.

Best regards,
[Name]
[Position]
Samsung C&T Engineering & Construction
```

---

**END OF DOCUMENT**

For questions about this guide:
- Email: [Support email]
- Phone: [Support phone]
- MACHO-GPT System: [Contact method]
