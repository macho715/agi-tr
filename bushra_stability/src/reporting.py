"""
Report generation module for stability calculations.

Provides Excel and PDF report generation with GZ curves and IMO checks.
"""
from pathlib import Path
from typing import Dict, Any, List, Optional
import json

import pandas as pd
import numpy as np

try:
    import matplotlib.pyplot as plt
    from matplotlib.backends.backend_pdf import PdfPages
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False

try:
    import xlsxwriter
    XLSXWRITER_AVAILABLE = True
except ImportError:
    XLSXWRITER_AVAILABLE = False

from .stability import StabilityResult


def export_stability_json(
    result: StabilityResult,
    imo_check: Optional[Dict[str, Any]] = None,
    output_path: Optional[Path] = None
) -> str:
    """
    Export stability result as JSON.
    
    Args:
        result: StabilityResult object
        imo_check: Optional IMO check results
        output_path: Optional output file path (if None, returns JSON string)
        
    Returns:
        JSON string or writes to file
    """
    data = {
        "displacement": result.total_weight,
        "lcg": result.lcg,
        "vcg": result.vcg,
        "tcg": result.tcg,
        "total_fsm": result.total_fsm,
        "kg_corrected": result.kg_corrected,
        "kmt": result.kmt,
        "gm": result.gm,
        "trim": result.trim,
        "draft_mean": result.draft_mean,
        "draft_fwd": result.draft_fwd,
        "draft_aft": result.draft_aft,
        "lcb": result.lcb,
        "mtc": result.mtc,
        "kn_curve": result.kn_curve,
        "gz_curve": result.gz_curve,
    }
    
    if result.trim_history:
        data["trim_history"] = result.trim_history
    
    if imo_check:
        data["imo_check"] = imo_check
    
    json_str = json.dumps(data, indent=2, ensure_ascii=False)
    
    if output_path:
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(json_str)
        return str(output_path)
    
    return json_str


def export_stability_excel(
    result: StabilityResult,
    items: List[Any],  # WeightItem or DataFrame rows
    imo_check: Optional[Dict[str, Any]] = None,
    output_path: Path
) -> str:
    """
    Export stability result as Excel workbook.
    
    Args:
        result: StabilityResult object
        items: List of weight items or DataFrame
        imo_check: Optional IMO check results
        output_path: Output file path
        
    Returns:
        Path to created Excel file
        
    Raises:
        ImportError: If xlsxwriter is not available
    """
    if not XLSXWRITER_AVAILABLE:
        raise ImportError("xlsxwriter is required for Excel export")
    
    with pd.ExcelWriter(output_path, engine="xlsxwriter") as writer:
        # Summary sheet
        summary_data = {
            "Parameter": [
                "Displacement (t)",
                "LCG (m)",
                "VCG (m)",
                "TCG (m)",
                "Total FSM (t·m)",
                "KG Corrected (m)",
                "KMT (m)",
                "GM (m)",
                "Trim (m)",
                "Draft Mean (m)",
                "Draft Forward (m)",
                "Draft Aft (m)",
                "LCB (m)",
                "MTC (t·m/cm)",
            ],
            "Value": [
                result.total_weight,
                result.lcg,
                result.vcg,
                result.tcg,
                result.total_fsm,
                result.kg_corrected,
                result.kmt,
                result.gm,
                result.trim,
                result.draft_mean,
                result.draft_fwd,
                result.draft_aft,
                result.lcb,
                result.mtc,
            ],
        }
        
        if imo_check:
            summary_data["Parameter"].extend([
                "IMO Area 0-30 (m·rad)",
                "IMO Area 0-40 (m·rad)",
                "IMO Area 30-40 (m·rad)",
                "IMO GZ@30° (m)",
                "IMO GZmax (m)",
                "IMO Angle@GZmax (deg)",
                "IMO Overall Pass",
            ])
            summary_data["Value"].extend([
                imo_check.get("Area_0_30_mrad", 0),
                imo_check.get("Area_0_40_mrad", 0),
                imo_check.get("Area_30_40_mrad", 0),
                imo_check.get("GZ_30deg_m", 0),
                imo_check.get("GZmax_m", 0),
                imo_check.get("Angle_at_GZmax_deg", 0),
                imo_check.get("Overall_Pass", False),
            ])
        
        pd.DataFrame(summary_data).to_excel(
            writer, sheet_name="Summary", index=False
        )
        
        # GZ Curve sheet
        curve_data = {
            "Heel (deg)": list(result.gz_curve.keys()),
            "KN (m)": [result.kn_curve.get(h, 0) for h in result.gz_curve.keys()],
            "GZ (m)": list(result.gz_curve.values()),
        }
        curve_df = pd.DataFrame(curve_data)
        curve_df.to_excel(writer, sheet_name="GZ_Curve", index=False)
        
        # Add chart
        workbook = writer.book
        worksheet = writer.sheets["GZ_Curve"]
        chart = workbook.add_chart({"type": "line"})
        chart.add_series({
            "name": "GZ (m)",
            "categories": ["GZ_Curve", 1, 0, len(curve_df), 0],
            "values": ["GZ_Curve", 1, 2, len(curve_df), 2],
        })
        chart.set_title({"name": "GZ Curve"})
        chart.set_x_axis({"name": "Heel (deg)"})
        chart.set_y_axis({"name": "GZ (m)"})
        worksheet.insert_chart("E2", chart)
        
        # Trim Iteration sheet (if trim_history available)
        if result.trim_history and len(result.trim_history) > 0:
            trim_df = pd.DataFrame(result.trim_history)
            trim_df.to_excel(writer, sheet_name="Trim_Iteration", index=False)
        
        # Items sheet (if items provided)
        if items:
            if isinstance(items, pd.DataFrame):
                items_df = items
            else:
                # Convert WeightItem list to DataFrame
                items_data = []
                for item in items:
                    items_data.append({
                        "Name": item.name,
                        "Group": item.group or "",
                        "Weight (t)": item.weight,
                        "LCG (m)": item.lcg,
                        "VCG (m)": item.vcg,
                        "TCG (m)": item.tcg,
                        "FSM (t·m)": item.fsm,
                    })
                items_df = pd.DataFrame(items_data)
            
            items_df.to_excel(writer, sheet_name="Weight_Items", index=False)
    
    return str(output_path)


def export_stability_pdf(
    result: StabilityResult,
    vessel_name: str = "BUSHRA",
    imo_check: Optional[Dict[str, Any]] = None,
    output_path: Path
) -> str:
    """
    Export stability result as PDF report.
    
    Args:
        result: StabilityResult object
        vessel_name: Vessel name
        imo_check: Optional IMO check results
        output_path: Output file path
        
    Returns:
        Path to created PDF file
        
    Raises:
        ImportError: If matplotlib is not available
    """
    if not MATPLOTLIB_AVAILABLE:
        raise ImportError("matplotlib is required for PDF export")
    
    with PdfPages(output_path) as pdf:
        # Page 1: Summary
        fig, ax = plt.subplots(figsize=(8.3, 11.7))
        ax.axis("off")
        
        lines = [
            f"{vessel_name} Stability Report",
            "",
            f"Displacement (t): {result.total_weight:.2f}",
            f"LCG (m): {result.lcg:.2f}",
            f"VCG (m): {result.vcg:.2f}",
            f"TCG (m): {result.tcg:.2f}",
            f"Total FSM (t·m): {result.total_fsm:.2f}",
            f"KG Corrected (m): {result.kg_corrected:.2f}",
            f"KMT (m): {result.kmt:.2f}",
            f"GM (m): {result.gm:.2f}",
            f"Trim (+aft) (m): {result.trim:.2f}",
            f"Draft Mean (m): {result.draft_mean:.2f}",
            f"Draft Forward (m): {result.draft_fwd:.2f}",
            f"Draft Aft (m): {result.draft_aft:.2f}",
            "",
        ]
        
        if imo_check:
            lines.extend([
                "IMO A.749 Check:",
                f"  Area 0–30 (m·rad): {imo_check.get('Area_0_30_mrad', 0):.3f}  → {'PASS' if imo_check.get('Area 0-30 (m·rad)', {}).get('Pass', False) else 'FAIL'}",
                f"  Area 0–40 (m·rad): {imo_check.get('Area_0_40_mrad', 0):.3f}  → {'PASS' if imo_check.get('Area 0-40 (m·rad)', {}).get('Pass', False) else 'FAIL'}",
                f"  Area 30–40 (m·rad): {imo_check.get('Area_30_40_mrad', 0):.3f}  → {'PASS' if imo_check.get('Area 30-40 (m·rad)', {}).get('Pass', False) else 'FAIL'}",
                f"  GZ@30° (m): {imo_check.get('GZ_30deg_m', 0):.3f}        → {'PASS' if imo_check.get('GZ at 30° (m)', {}).get('Pass', False) else 'FAIL'}",
                f"  Max GZ (m): {imo_check.get('GZmax_m', 0):.3f} at {imo_check.get('Angle_at_GZmax_deg', 0):.1f}° → {'PASS' if imo_check.get('GZmax (m)', {}).get('Pass', False) else 'FAIL'}",
                f"  Overall: {'PASS' if imo_check.get('Overall_Pass', False) else 'FAIL'}",
            ])
        
        y = 0.95
        for line in lines:
            ax.text(0.08, y, line, fontsize=12, va="top")
            y -= 0.035
        
        pdf.savefig(fig)
        plt.close(fig)
        
        # Page 2: GZ Curve
        fig2, ax2 = plt.subplots(figsize=(8.3, 11.7))
        heels = list(result.gz_curve.keys())
        gz_values = list(result.gz_curve.values())
        ax2.plot(heels, gz_values, marker="o", linewidth=2, markersize=8)
        ax2.set_title("GZ Curve", fontsize=16, fontweight="bold")
        ax2.set_xlabel("Heel (deg)", fontsize=12)
        ax2.set_ylabel("GZ (m)", fontsize=12)
        ax2.grid(True, linestyle="--", alpha=0.4)
        ax2.axhline(y=0, color="k", linestyle="-", linewidth=0.5)
        ax2.axvline(x=0, color="k", linestyle="-", linewidth=0.5)
        pdf.savefig(fig2)
        plt.close(fig2)
        
        # Page 3: Trim Iteration (if available)
        if result.trim_history and len(result.trim_history) > 0:
            fig3, ax3 = plt.subplots(figsize=(8.3, 11.7))
            ax3.axis("off")
            
            lines = [
                "Trim Iteration History",
                "",
            ]
            
            # Add iteration details
            for hist in result.trim_history[:28]:  # Limit to 28 rows per page
                lines.append(
                    f"Iter {hist['iter']}: trim={hist['trim']:.4f} → new={hist['new_trim']:.4f} "
                    f"(LCB={hist['LCB']:.3f}, MTC={hist['MTC']:.2f})"
                )
            
            if len(result.trim_history) > 28:
                lines.append(f"\n... ({len(result.trim_history) - 28} more iterations)")
            
            y = 0.95
            for line in lines:
                ax3.text(0.08, y, line, fontsize=10, va="top", family="monospace")
                y -= 0.025
            
            pdf.savefig(fig3)
            plt.close(fig3)
    
    return str(output_path)

