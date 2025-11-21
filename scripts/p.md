1. Line 690 다음에 두 함수 추가:

def extend_roro_captain_req(ws):
    """RORO 시트에 Captain Req 컬럼 추가 (Col T부터)"""
    styles = get_styles()
    
    captain_cols = ["GM(m)", "Fwd Draft(m)", "vs 2.70m", "De-ballast Qty(t)", "Timing", 
                    "Freeboard(m)", "Prop Imm(%)", "Time(h)"]
    start_col = 20  # Col T
    
    # Row 14에 헤더 설정 (기존 헤더 행과 동일)
    for i, h in enumerate(captain_cols):
        col = start_col + i
        cell = ws.cell(row=14, column=col)
        cell.value = h
        cell.font = styles["header_font"]
        cell.fill = styles["header_fill"]
        cell.alignment = styles["center_align"]
        cell.border = Border(
            left=styles["thin_border"],
            right=styles["thin_border"],
            top=styles["thin_border"],
            bottom=styles["thin_border"]
        )
    
    # Row 15부터 각 Stage 행에 수식 생성 (10개 Stage)
    for row in range(15, 25):
        row_str = str(row)
        
        # Col U (21): Fwd Draft(m) - Col O의 Dfwd_m 참조
        ws.cell(row=row, column=21).value = f'=IF(O{row_str}="", "", O{row_str})'
        ws.cell(row=row, column=21).number_format = "0.00"
        ws.cell(row=row, column=21).font = styles["normal_font"]
        
        # Col V (22): vs 2.70m - Col U와 2.70 비교
        ws.cell(row=row, column=22).value = f'=IF(U{row_str}="", "", IF(U{row_str}<=2.70,"OK","NG"))'
        ws.cell(row=row, column=22).font = styles["normal_font"]
        
        # Col W (23): De-ballast Qty(t) - Col J의 Ballast_t_calc 참조
        ws.cell(row=row, column=23).value = f'=IF(J{row_str}="", "", J{row_str})'
        ws.cell(row=row, column=23).number_format = "0.00"
        ws.cell(row=row, column=23).font = styles["normal_font"]
        
        # Col Y (25): Freeboard(m) - Col Q의 FWD_Height_m 참조
        ws.cell(row=row, column=25).value = f'=IF(Q{row_str}="", "", Q{row_str})'
        ws.cell(row=row, column=25).number_format = "0.00"
        ws.cell(row=row, column=25).font = styles["normal_font"]
        
        # Col AA (27): Time(h) - Col K의 Ballast_time_h_calc 참조
        ws.cell(row=row, column=27).value = f'=IF(K{row_str}="", "", K{row_str})'
        ws.cell(row=row, column=27).number_format = "0.00"
        ws.cell(row=row, column=27).font = styles["normal_font"]
    
    # 컬럼 너비 설정
    ws.column_dimensions['T'].width = 12
    ws.column_dimensions['U'].width = 12
    ws.column_dimensions['V'].width = 12
    ws.column_dimensions['W'].width = 15
    ws.column_dimensions['X'].width = 12
    ws.column_dimensions['Y'].width = 13
    ws.column_dimensions['Z'].width = 12
    ws.column_dimensions['AA'].width = 12
    
    print("  [OK] Captain Req columns added to RORO_Stage_Scenarios sheet")


def create_captain_req_sheet(wb):
    """Captain_Req 시트 생성"""
    ws = wb.create_sheet("Captain_Req")
    styles = get_styles()
    
    # Row 1: 헤더
    headers = ["Stage", "GM(m)", "Fwd Draft(m)", "vs 2.70m", "De-ballast Qty(t)", 
               "Timing", "Critical Trim(m aft)", "GM", "Freeboard(m)", "vs Prev 0.46m", 
               "Prop Imm(%)", "Emergency OK", "Vent Rate(t/h)", "Time(h)", "Notes"]
    
    for col, h in enumerate(headers, 1):
        cell = ws.cell(row=1, column=col, value=h)
        cell.font = styles["header_font"]
        cell.fill = styles["header_fill"]
        cell.alignment = styles["center_align"]
        cell.border = Border(
            left=styles["thin_border"],
            right=styles["thin_border"],
            top=styles["thin_border"],
            bottom=styles["thin_border"]
        )
        ws.column_dimensions[get_column_letter(col)].width = 14
    
    # Row 2-5: 샘플 데이터
    data = [
        ("0", 2.85, 2.10, "OK", 0, "-", 0.20, 2.85, 1.55, "-", 100, "OK", "-", "-", "Empty baseline"),
        ("1", 1.68, 2.92, "NG", 160, "After 1st TR", -0.53, 1.68, 0.73, "-", 92, "OK", 45, 3.56, "De-ballast start"),
        ("Critical", 1.88, 2.68, "OK", 0, "-", 0.60, 1.88, 0.42, -0.04, 96, "OK", "-", "-", "TR1 stow + TR2 ramp"),
        ("Final", 1.85, 2.65, "OK", 50, "Fine tune", 0.70, 1.85, 1.00, "-", 97, "OK", "-", "-", "Optimized")
    ]
    
    for r, row_data in enumerate(data, 2):
        for c, val in enumerate(row_data, 1):
            cell = ws.cell(row=r, column=c, value=val)
            cell.font = styles["normal_font"]
            if c in [2, 3, 8, 9, 11]:  # 숫자 열
                cell.number_format = '0.00'
    
    # Row 2-10: 수식 생성 (샘플 데이터 이후에도 수식 적용)
    for r in range(2, 11):
        row_str = str(r)
        # Col D (4): vs 2.70m
        ws.cell(row=r, column=4).value = f'=IF(C{r}<=2.70,"OK","NG")'
        # Col J (10): vs Prev 0.46m
        ws.cell(row=r, column=10).value = f'=IF(C{r}-0.46<0, C{r}-0.46, "-")'
        # Col N (14): Time(h) = De-ballast Qty / Vent Rate
        ws.cell(row=r, column=14).value = f'=IF(E{r}>0, IF(M{r}>0, E{r}/M{r}, "-"), "-")'
    
    print("  [OK] Captain_Req sheet created")




 Line 656 수정:

            # Table range: A14:AA24 (header row + 10 data rows, 27 columns - T~AA 추가)
        table = Table(displayName="Stages", ref=f"A{header_row}:AA{first_data_row + len(stages) - 1}") 

 Line 729 다음에 추가:
            create_roro_sheet(wb)
    # RORO 시트에 Captain Req 컬럼 추가
    roro_ws = wb["RORO_Stage_Scenarios"]
    extend_roro_captain_req(roro_ws)
    # Captain_Req 시트 생성
    create_captain_req_sheet(wb)