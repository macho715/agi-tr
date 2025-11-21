"""
Command-line interface for BUSHRA Stability Calculation.

Provides CLI commands to calculate displacement from Excel workbooks
and output results in JSON or CSV format.
"""
import json
import sys
from pathlib import Path
from typing import Optional
import argparse
import csv

from .excel_reader import read_weight_items_from_excel
from .csv_reader import csv_to_weight_items
from .displacement import calculate_displacement, DisplacementResult
from .stability import calculate_stability, StabilityResult
from .imo_check import check_imo_a749
from .reporting import export_stability_json, export_stability_excel, export_stability_pdf
from .site_config import SiteRequirements, validate_stability_for_site, generate_site_checklist

# Optional imports
try:
    from .hydrostatic import HydroEngine
    HYDROSTATIC_AVAILABLE = True
except ImportError:
    HYDROSTATIC_AVAILABLE = False
    HydroEngine = None


def format_result_json(result: DisplacementResult) -> str:
    """Format displacement result as JSON string."""
    return json.dumps(
        {
            "total_weight": result.total_weight,
            "lcg": result.lcg,
            "vcg": result.vcg,
            "tcg": result.tcg,
            "total_fsm": result.total_fsm,
        },
        indent=2,
    )


def format_result_csv(result: DisplacementResult, output_path: Path) -> None:
    """Write displacement result to CSV file."""
    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Parameter", "Value", "Unit"])
        writer.writerow(["Total Weight", f"{result.total_weight:.4f}", "t"])
        writer.writerow(["LCG", f"{result.lcg:.6f}", "m"])
        writer.writerow(["VCG", f"{result.vcg:.6f}", "m"])
        writer.writerow(["TCG", f"{result.tcg:.6f}", "m"])
        writer.writerow(["Total FSM", f"{result.total_fsm:.2f}", "t·m"])


def main(args: Optional[list] = None) -> int:
    """
    Main CLI entry point.
    
    Args:
        args: Command-line arguments (defaults to sys.argv)
        
    Returns:
        Exit code (0 for success, non-zero for error)
    """
    parser = argparse.ArgumentParser(
        description="BUSHRA Stability Calculation - Calculate displacement from Excel workbook"
    )
    parser.add_argument(
        "excel_file",
        type=Path,
        nargs="?",
        help="Path to Excel workbook file (required unless --csv-mode)",
    )
    parser.add_argument(
        "--sheet",
        type=str,
        default="Volum",
        help="Sheet name to read from (default: Volum)",
    )
    parser.add_argument(
        "--output",
        "-o",
        type=Path,
        help="Output file path (if not specified, prints to stdout)",
    )
    parser.add_argument(
        "--format",
        "-f",
        choices=["json", "csv", "xlsx", "pdf"],
        default="json",
        help="Output format (default: json)",
    )
    parser.add_argument(
        "--stability",
        action="store_true",
        help="Calculate full stability (requires --hydro and --kn)",
    )
    parser.add_argument(
        "--hydro",
        type=Path,
        help="Path to hydrostatics CSV file (required for stability)",
    )
    parser.add_argument(
        "--kn",
        type=Path,
        help="Path to KN table CSV file (required for stability)",
    )
    parser.add_argument(
        "--csv-mode",
        action="store_true",
        help="Use CSV input mode (requires --master, --mapping, --condition)",
    )
    parser.add_argument(
        "--master",
        type=Path,
        help="Path to master tanks CSV (for CSV mode)",
    )
    parser.add_argument(
        "--mapping",
        type=Path,
        help="Path to tank mapping CSV (for CSV mode)",
    )
    parser.add_argument(
        "--condition",
        type=Path,
        help="Path to condition CSV (for CSV mode)",
    )
    parser.add_argument(
        "--imo-check",
        action="store_true",
        help="Perform IMO A.749 check (requires --stability)",
    )
    parser.add_argument(
        "--site",
        type=str,
        choices=["DAS", "AGI", "DAS-001", "AGI-002"],
        help="Target site for RORO operation (DAS Island or AGI Site)",
    )
    parser.add_argument(
        "--site-validate",
        action="store_true",
        help="Validate stability against site-specific requirements (requires --site and --stability)",
    )
    parser.add_argument(
        "--site-checklist",
        action="store_true",
        help="Generate site-specific operation checklist (requires --site)",
    )
    
    parsed_args = parser.parse_args(args)
    
    try:
        # Handle site checklist (can be standalone)
        if parsed_args.site_checklist:
            if not parsed_args.site:
                print("Error: --site required for --site-checklist", file=sys.stderr)
                return 1
            site_req = SiteRequirements.from_site_code(parsed_args.site)
            checklist = generate_site_checklist(site_req)
            print(checklist)
            if not parsed_args.stability:  # If only checklist requested, exit
                return 0
        
        # Read items
        if parsed_args.csv_mode:
            if not all([parsed_args.master, parsed_args.mapping, parsed_args.condition]):
                print("Error: CSV mode requires --master, --mapping, and --condition", file=sys.stderr)
                return 1
            items = csv_to_weight_items(
                parsed_args.master,
                parsed_args.mapping,
                parsed_args.condition
            )
        else:
            if not parsed_args.excel_file:
                print("Error: Excel file required (or use --csv-mode)", file=sys.stderr)
                return 1
            items = read_weight_items_from_excel(
                parsed_args.excel_file, sheet_name=parsed_args.sheet
            )
        
        if not items:
            print("Error: No weight items found", file=sys.stderr)
            return 1
        
        # Calculate displacement or stability
        if parsed_args.stability:
            if not HYDROSTATIC_AVAILABLE:
                print("Error: scipy is required for stability calculations", file=sys.stderr)
                return 1
            if not all([parsed_args.hydro, parsed_args.kn]):
                print("Error: --hydro and --kn required for stability calculation", file=sys.stderr)
                return 1
            
            hydro = HydroEngine(parsed_args.hydro, parsed_args.kn)
            result = calculate_stability(items, hydro)
            
            # IMO check if requested
            imo_check = None
            if parsed_args.imo_check:
                heel_angles = list(result.gz_curve.keys())
                gz_values = list(result.gz_curve.values())
                imo_check = check_imo_a749(heel_angles, gz_values, result.gm)
            
            # Site validation if requested
            if parsed_args.site_validate:
                if not parsed_args.site:
                    print("Error: --site required for --site-validate", file=sys.stderr)
                    return 1
                site_req = SiteRequirements.from_site_code(parsed_args.site)
                site_validation = validate_stability_for_site(result, site_req, verbose=True)
                # Add site validation to IMO check or create new dict
                if imo_check is None:
                    imo_check = {}
                imo_check["site_validation"] = site_validation
                imo_check["site_name"] = site_req.site_name
                imo_check["site_type"] = site_req.site_type.value
        else:
            # Basic displacement only
            result = calculate_displacement(items)
            imo_check = None
        
        # Output results
        if parsed_args.output:
            if parsed_args.format == "json":
                if isinstance(result, StabilityResult):
                    export_stability_json(result, imo_check, parsed_args.output)
                else:
                    with open(parsed_args.output, "w", encoding="utf-8") as f:
                        f.write(format_result_json(result))
            elif parsed_args.format == "csv":
                if isinstance(result, StabilityResult):
                    print("Error: CSV format not supported for stability results. Use json, xlsx, or pdf", file=sys.stderr)
                    return 1
                format_result_csv(result, parsed_args.output)
            elif parsed_args.format == "xlsx":
                if not isinstance(result, StabilityResult):
                    print("Error: Excel format requires --stability", file=sys.stderr)
                    return 1
                export_stability_excel(result, items, imo_check, parsed_args.output)
            elif parsed_args.format == "pdf":
                if not isinstance(result, StabilityResult):
                    print("Error: PDF format requires --stability", file=sys.stderr)
                    return 1
                export_stability_pdf(result, "BUSHRA", imo_check, parsed_args.output)
        else:
            # Output to stdout
            if parsed_args.format == "json":
                if isinstance(result, StabilityResult):
                    print(export_stability_json(result, imo_check))
                else:
                    print(format_result_json(result))
            else:
                print("Error: Non-JSON formats require --output option", file=sys.stderr)
                return 1
        
        return 0
        
    except FileNotFoundError as e:
        print(f"Error: File not found: {e}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())

