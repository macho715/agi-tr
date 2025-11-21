"""
Streamlit web interface for BUSHRA Stability Calculation.

Provides an interactive UI for calculating vessel stability from Excel workbooks.
"""
import streamlit as st
from pathlib import Path
import pandas as pd
import json
import tempfile
import os
import sys

# Handle both relative and absolute imports
try:
    from .excel_reader import read_weight_items_from_excel
    from .csv_reader import csv_to_weight_items
    from .displacement import calculate_displacement, WeightItem, DisplacementResult
    from .stability import calculate_stability, StabilityResult
    from .imo_check import check_imo_a749
    from .reporting import export_stability_json, export_stability_excel, export_stability_pdf
    # Optional imports
    try:
        from .hydrostatic import HydroEngine
        HYDROSTATIC_AVAILABLE = True
    except ImportError:
        HYDROSTATIC_AVAILABLE = False
        HydroEngine = None
except ImportError:
    # Fallback for direct execution
    from excel_reader import read_weight_items_from_excel
    from csv_reader import csv_to_weight_items
    from displacement import calculate_displacement, WeightItem, DisplacementResult
    from stability import calculate_stability, StabilityResult
    from imo_check import check_imo_a749
    from reporting import export_stability_json, export_stability_excel, export_stability_pdf
    # Optional imports
    try:
        from hydrostatic import HydroEngine
        HYDROSTATIC_AVAILABLE = True
    except ImportError:
        HYDROSTATIC_AVAILABLE = False
        HydroEngine = None


def format_result_table(result: DisplacementResult) -> pd.DataFrame:
    """Format displacement result as a pandas DataFrame for display."""
    return pd.DataFrame(
        {
            "Parameter": ["Total Weight", "LCG", "VCG", "TCG", "Total FSM"],
            "Value": [
                f"{result.total_weight:.4f}",
                f"{result.lcg:.6f}",
                f"{result.vcg:.6f}",
                f"{result.tcg:.6f}",
                f"{result.total_fsm:.2f}",
            ],
            "Unit": ["t", "m", "m", "m", "t·m"],
        }
    )


def format_items_table(items: list[WeightItem]) -> pd.DataFrame:
    """Format weight items as a pandas DataFrame for display."""
    data = []
    for item in items:
        data.append(
            {
                "Name": item.name,
                "Group": item.group or "",
                "Weight (t)": f"{item.weight:.4f}" if item.weight else "",
                "LCG (m)": f"{item.lcg:.3f}" if item.lcg is not None else "",
                "VCG (m)": f"{item.vcg:.3f}" if item.vcg is not None else "",
                "TCG (m)": f"{item.tcg:.3f}" if item.tcg is not None else "",
                "FSM (t·m)": f"{item.fsm:.2f}" if item.fsm else "",
            }
        )
    return pd.DataFrame(data)


def main():
    """Main Streamlit application."""
    st.set_page_config(
        page_title="BUSHRA Stability Calculation",
        page_icon="⚓",
        layout="wide",
    )
    
    st.title("⚓ BUSHRA Stability Calculation")
    st.markdown(
        "Calculate vessel displacement and stability parameters from Excel workbooks."
    )
    
    # File upload
    st.sidebar.header("Input")
    
    input_mode = st.sidebar.radio(
        "Input Mode",
        ["Excel Workbook", "CSV Files"],
        help="Choose input format"
    )
    
    if input_mode == "Excel Workbook":
        uploaded_file = st.sidebar.file_uploader(
            "Upload Excel Workbook",
            type=["xls", "xlsx"],
            help="Upload the BUSHRA Stability Calculation Excel workbook",
        )
        sheet_name = st.sidebar.text_input(
            "Sheet Name", value="Volum", help="Name of the sheet to read from"
        )
        hydro_file = None
        kn_file = None
    else:
        uploaded_file = None
        sheet_name = None
        st.sidebar.subheader("CSV Files")
        master_file = st.sidebar.file_uploader(
            "Master Tanks CSV",
            type=["csv"],
            help="Master tanks data file"
        )
        mapping_file = st.sidebar.file_uploader(
            "Tank Mapping CSV",
            type=["csv"],
            help="Tank mapping file"
        )
        condition_file = st.sidebar.file_uploader(
            "Condition CSV",
            type=["csv"],
            help="Condition file"
        )
    
    # Stability calculation options
    st.sidebar.header("Stability Options")
    enable_stability = st.sidebar.checkbox(
        "Enable Stability Calculation",
        help="Calculate GZ curves and trim (requires hydrostatic data)"
    )
    
    if enable_stability:
        hydro_file = st.sidebar.file_uploader(
            "Hydrostatics CSV",
            type=["csv"],
            help="Hydrostatic data file"
        )
        kn_file = st.sidebar.file_uploader(
            "KN Table CSV",
            type=["csv"],
            help="KN table file"
        )
        enable_imo = st.sidebar.checkbox(
            "IMO A.749 Check",
            help="Perform IMO stability criteria check"
        )
    else:
        enable_imo = False
    
    # Process input
    items = None
    tmp_files = []
    
    if input_mode == "Excel Workbook" and uploaded_file is not None:
        # Save uploaded file to temporary location
        with tempfile.NamedTemporaryFile(delete=False, suffix=".xls") as tmp_file:
            tmp_file.write(uploaded_file.getvalue())
            tmp_path = Path(tmp_file.name)
            tmp_files.append(tmp_path)
        
        try:
            # Read items from Excel
            with st.spinner("Reading Excel workbook..."):
                items = read_weight_items_from_excel(tmp_path, sheet_name=sheet_name)
        except Exception as e:
            st.error(f"Error reading Excel file: {e}")
            items = None
    
    elif input_mode == "CSV Files" and all([master_file, mapping_file, condition_file]):
        # Save CSV files to temporary location
        for file, suffix in [(master_file, "_master.csv"), (mapping_file, "_mapping.csv"), (condition_file, "_condition.csv")]:
            with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp_file:
                tmp_file.write(file.getvalue())
                tmp_files.append(Path(tmp_file.name))
        
        master_path, mapping_path, condition_path = tmp_files
        
        try:
            # Read items from CSV
            with st.spinner("Reading CSV files..."):
                items = csv_to_weight_items(master_path, mapping_path, condition_path)
        except Exception as e:
            st.error(f"Error reading CSV files: {e}")
            items = None
    
    if items is not None:
        try:
            # Calculate displacement or stability
            if enable_stability and HYDROSTATIC_AVAILABLE and hydro_file and kn_file:
                # Save hydrostatic files
                with tempfile.NamedTemporaryFile(delete=False, suffix="_hydro.csv") as tmp_hydro:
                    tmp_hydro.write(hydro_file.getvalue())
                    tmp_files.append(Path(tmp_hydro.name))
                with tempfile.NamedTemporaryFile(delete=False, suffix="_kn.csv") as tmp_kn:
                    tmp_kn.write(kn_file.getvalue())
                    tmp_files.append(Path(tmp_kn.name))
                
                # Calculate stability
                with st.spinner("Calculating stability..."):
                    hydro = HydroEngine(tmp_files[-2], tmp_files[-1])
                    result = calculate_stability(items, hydro)
                    
                    # IMO check if requested
                    imo_check = None
                    if enable_imo:
                        heel_angles = list(result.gz_curve.keys())
                        gz_values = list(result.gz_curve.values())
                        imo_check = check_imo_a749(heel_angles, gz_values, result.gm)
            else:
                # Basic displacement only
                with st.spinner("Calculating displacement..."):
                    result = calculate_displacement(items)
                imo_check = None
            
            if not items:
                st.error("No weight items found.")
                return
            
            # Display results
            if isinstance(result, StabilityResult):
                st.header("📊 Stability Results")
                
                # Key metrics
                col1, col2, col3, col4, col5 = st.columns(5)
                
                with col1:
                    st.metric("Displacement", f"{result.total_weight:.2f} t")
                
                with col2:
                    st.metric("GM", f"{result.gm:.3f} m")
                
                with col3:
                    st.metric("KG Corrected", f"{result.kg_corrected:.3f} m")
                
                with col4:
                    st.metric("Trim", f"{result.trim:.3f} m")
                
                with col5:
                    st.metric("Draft Mean", f"{result.draft_mean:.3f} m")
                
                # Additional metrics
                col6, col7, col8, col9, col10 = st.columns(5)
                
                with col6:
                    st.metric("LCG", f"{result.lcg:.3f} m")
                
                with col7:
                    st.metric("VCG", f"{result.vcg:.3f} m")
                
                with col8:
                    st.metric("KMT", f"{result.kmt:.3f} m")
                
                with col9:
                    st.metric("Draft Fwd", f"{result.draft_fwd:.3f} m")
                
                with col10:
                    st.metric("Draft Aft", f"{result.draft_aft:.3f} m")
                
                # GZ Curve
                st.header("📈 GZ Curve")
                heels = list(result.gz_curve.keys())
                gz_values = list(result.gz_curve.values())
                kn_values = [result.kn_curve.get(h, 0) for h in heels]
                
                curve_df = pd.DataFrame({
                    "Heel (deg)": heels,
                    "KN (m)": kn_values,
                    "GZ (m)": gz_values,
                })
                st.line_chart(curve_df.set_index("Heel (deg)"))
                st.dataframe(curve_df, use_container_width=True, hide_index=True)
                
                # Trim Iteration History
                if result.trim_history and len(result.trim_history) > 0:
                    st.header("🔄 Trim Iteration History")
                    trim_hist_df = pd.DataFrame(result.trim_history)
                    st.dataframe(trim_hist_df, use_container_width=True, hide_index=True)
                    
                    # Show convergence status
                    converged = any(
                        abs(hist.get("new_trim", 0) - hist.get("trim", 0)) < 0.001 
                        for hist in result.trim_history
                    )
                    if converged:
                        st.success(f"✅ Trim converged after {len(result.trim_history)} iterations")
                    else:
                        st.warning(f"⚠️ Trim iteration completed ({len(result.trim_history)} iterations)")
                
                # IMO Check
                if imo_check:
                    st.header("✅ IMO A.749 Check")
                    imo_data = []
                    for key, value in imo_check.items():
                        if isinstance(value, dict) and "Pass" in value:
                            imo_data.append({
                                "Criterion": key,
                                "Value": value.get("Value", ""),
                                "Required": value.get("Required", ""),
                                "Status": "✅ PASS" if value["Pass"] else "❌ FAIL",
                            })
                    
                    if imo_data:
                        imo_df = pd.DataFrame(imo_data)
                        st.dataframe(imo_df, use_container_width=True, hide_index=True)
                        
                        overall_pass = imo_check.get("Overall_Pass", False)
                        if overall_pass:
                            st.success("✅ All IMO A.749 criteria PASSED")
                        else:
                            st.error("❌ Some IMO A.749 criteria FAILED")
            else:
                st.header("📊 Displacement Results")
                
                col1, col2, col3, col4, col5 = st.columns(5)
                
                with col1:
                    st.metric("Total Weight", f"{result.total_weight:.2f} t")
                
                with col2:
                    st.metric("LCG", f"{result.lcg:.3f} m")
                
                with col3:
                    st.metric("VCG", f"{result.vcg:.3f} m")
                
                with col4:
                    st.metric("TCG", f"{result.tcg:.3f} m")
                
                with col5:
                    st.metric("Total FSM", f"{result.total_fsm:.2f} t·m")
            
            # Detailed results table
            st.subheader("Detailed Results")
            if isinstance(result, StabilityResult):
                result_df = pd.DataFrame({
                    "Parameter": [
                        "Displacement (t)", "LCG (m)", "VCG (m)", "TCG (m)",
                        "Total FSM (t·m)", "KG Corrected (m)", "KMT (m)", "GM (m)",
                        "Trim (m)", "Draft Mean (m)", "Draft Forward (m)", "Draft Aft (m)",
                    ],
                    "Value": [
                        result.total_weight, result.lcg, result.vcg, result.tcg,
                        result.total_fsm, result.kg_corrected, result.kmt, result.gm,
                        result.trim, result.draft_mean, result.draft_fwd, result.draft_aft,
                    ],
                })
            else:
                result_df = format_result_table(result)
            st.dataframe(result_df, use_container_width=True, hide_index=True)
            
            # Weight items table
            st.header("📋 Weight Items")
            items_df = format_items_table(items)
            st.dataframe(items_df, use_container_width=True, hide_index=True)
            
            # Export options
            st.header("💾 Export Results")
            
            if isinstance(result, StabilityResult):
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    json_data = export_stability_json(result, imo_check)
                    st.download_button(
                        label="Download JSON",
                        data=json_data,
                        file_name="stability_result.json",
                        mime="application/json",
                    )
                
                with col2:
                    # Excel export
                    try:
                        with tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx") as tmp_xlsx:
                            tmp_xlsx_path = Path(tmp_xlsx.name)
                        export_stability_excel(result, items, imo_check, tmp_xlsx_path)
                        with open(tmp_xlsx_path, "rb") as f:
                            st.download_button(
                                label="Download Excel",
                                data=f.read(),
                                file_name="stability_report.xlsx",
                                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                            )
                        os.unlink(tmp_xlsx_path)
                    except ImportError:
                        st.warning("xlsxwriter not available for Excel export")
                
                with col3:
                    # PDF export
                    try:
                        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_pdf:
                            tmp_pdf_path = Path(tmp_pdf.name)
                        export_stability_pdf(result, "BUSHRA", imo_check, tmp_pdf_path)
                        with open(tmp_pdf_path, "rb") as f:
                            st.download_button(
                                label="Download PDF",
                                data=f.read(),
                                file_name="stability_report.pdf",
                                mime="application/pdf",
                            )
                        os.unlink(tmp_pdf_path)
                    except ImportError:
                        st.warning("matplotlib not available for PDF export")
                
                with col4:
                    # CSV export (curve data)
                    curve_csv = curve_df.to_csv(index=False)
                    st.download_button(
                        label="Download GZ Curve CSV",
                        data=curve_csv,
                        file_name="gz_curve.csv",
                        mime="text/csv",
                    )
            else:
                col1, col2 = st.columns(2)
                
                with col1:
                    json_data = json.dumps(
                        {
                            "total_weight": result.total_weight,
                            "lcg": result.lcg,
                            "vcg": result.vcg,
                            "tcg": result.tcg,
                            "total_fsm": result.total_fsm,
                        },
                        indent=2,
                    )
                    st.download_button(
                        label="Download JSON",
                        data=json_data,
                        file_name="displacement_result.json",
                        mime="application/json",
                    )
                
                with col2:
                    csv_data = result_df.to_csv(index=False)
                    st.download_button(
                        label="Download CSV",
                        data=csv_data,
                        file_name="displacement_result.csv",
                        mime="text/csv",
                    )
            
            # Clean up temporary files
            for tmp_file in tmp_files:
                if tmp_file.exists():
                    os.unlink(tmp_file)
            
        except Exception as e:
            st.error(f"Error processing file: {e}")
            import traceback
            st.code(traceback.format_exc())
            for tmp_file in tmp_files:
                if tmp_file.exists():
                    os.unlink(tmp_file)
    
    if items is None:
        st.info("👈 Please upload an Excel workbook to begin.")
        
        # Show example usage
        with st.expander("📖 How to Use"):
            st.markdown(
                """
                ### Excel Mode
                1. **Upload Excel File**: Click "Browse files" and select your BUSHRA Stability Calculation workbook
                2. **Select Sheet**: Enter the sheet name (default: "Volum")
                3. **View Results**: The displacement calculation results will be displayed automatically
                4. **Stability Calculation** (optional): Enable stability calculation and upload hydrostatic/KN CSV files
                5. **Export**: Download results as JSON, CSV, Excel, or PDF
                
                ### CSV Mode
                1. **Upload CSV Files**: Upload master_tanks.csv, tank_mapping.csv, and condition CSV files
                2. **Stability Calculation** (optional): Enable and upload hydrostatic/KN CSV files
                3. **View Results**: Results will be displayed automatically
                4. **Export**: Download results in various formats
                
                ### Supported Formats
                - **Excel**: Sheet with weight items (Weight, LCG, VCG, TCG, FSM)
                - **CSV**: Master tanks, mapping, and condition files
                - **Hydrostatic CSV**: Displacement, Trim, Draft, LCB, KMT, MTC columns
                - **KN CSV**: Displacement, Trim, Heel_0, Heel_10, ..., Heel_60 columns
                """
            )


if __name__ == "__main__":
    main()

