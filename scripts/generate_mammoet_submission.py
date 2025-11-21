# -*- coding: utf-8 -*-
"""
LCT BUSHRA — Mammoet 제출 자료 통합 생성 스크립트
Excel 업데이트 → 스케치 생성 → PDF 보고서 생성
"""

import os
import sys
from pathlib import Path

# 스크립트 디렉토리를 경로에 추가
script_dir = Path(__file__).parent
sys.path.insert(0, str(script_dir))

from generate_vessel_sketch import main as generate_sketches
from generate_height_report_pdf import main as generate_pdf


def main():
    """통합 실행 함수"""
    print("=" * 80)
    print("LCT BUSHRA — Mammoet Submission Package Generator")
    print("=" * 80)

    # 경로 설정
    script_dir = Path(__file__).parent
    output_dir = script_dir.parent / "output"

    # 출력 디렉토리 생성
    output_dir.mkdir(parents=True, exist_ok=True)

    excel_path = output_dir / "LCT_BUSHRA_GateAB_v4_HYBRID_generated.xlsx"

    # 1. Excel 파일 확인
    if not excel_path.exists():
        print(f"\n⚠️  Error: Excel file not found: {excel_path}")
        print("Please run build_bushra_v4_standalone.py first to generate the Excel file.")
        return 1

    print(f"\n✓ Excel file found: {excel_path}")

    # 2. 선박 측면도 스케치 생성
    print("\n" + "-" * 80)
    print("Step 1: Generating vessel elevation sketches...")
    print("-" * 80)
    try:
        generate_sketches()
        print("✓ Vessel sketches generated successfully")
    except Exception as e:
        print(f"⚠️  Error generating sketches: {e}")
        print("Continuing with PDF generation...")

    # 3. PDF 보고서 생성
    print("\n" + "-" * 80)
    print("Step 2: Generating PDF report...")
    print("-" * 80)
    try:
        generate_pdf()
        print("✓ PDF report generated successfully")
    except Exception as e:
        print(f"⚠️  Error generating PDF: {e}")
        return 1

    # 4. 출력 파일 목록
    print("\n" + "=" * 80)
    print("Submission Package Generated Successfully!")
    print("=" * 80)
    print("\nOutput files:")
    print(f"  1. Excel: {excel_path}")

    sketch_files = [
        output_dir / "vessel_sketch_stage_1.png",
        output_dir / "vessel_sketch_stage_2.png",
    ]
    for sketch_file in sketch_files:
        if sketch_file.exists():
            print(f"  2. Sketch: {sketch_file}")

    pdf_file = output_dir / "LCT_BUSHRA_Height_Report.pdf"
    if pdf_file.exists():
        print(f"  3. PDF Report: {pdf_file}")

    print("\n" + "-" * 80)
    print("Next Steps:")
    print("-" * 80)
    print("1. Verify KminusZ (K-Z) measurement in Calc!D10")
    print("2. Update tide data in December_Tide_2025 sheet (744 rows)")
    print("3. Review Stage-by-Stage heights in RoRo_Height_Report sheet")
    print("4. Send Excel + PDF to Mammoet (Yulia Frolova) for DWG update")
    print("5. Deadline: 11/06 (as per #msg-39)")
    print("=" * 80)

    return 0


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)

