# -*- coding: utf-8 -*-
# extract_stage_data_from_pdf.py
# Extract Stage W and x values from PDF stowage plan

import os
import re
import pdfplumber
from pathlib import Path

# PDF 파일 경로 (상위 폴더 기준)
PDF_PATH = r"../../RoRo Simulation_stowage plan_20251103 (2).pdf"

def safe_float(value, default=None):
    """Safely convert value to float"""
    if value is None:
        return default
    try:
        return float(value)
    except (TypeError, ValueError):
        return default

def extract_weight_patterns(text):
    """Extract weight values from text using various patterns"""
    weights = []
    
    # Pattern 1: "217t", "217 t", "217 ton"
    pattern1 = r'(\d+\.?\d*)\s*(?:t|ton|tonnes?)\b'
    matches = re.finditer(pattern1, text, re.IGNORECASE)
    for match in matches:
        weights.append(safe_float(match.group(1)))
    
    # Pattern 2: "Weight: 217", "W = 217", "W: 217"
    pattern2 = r'(?:Weight|W)\s*[=:]\s*(\d+\.?\d*)'
    matches = re.finditer(pattern2, text, re.IGNORECASE)
    for match in matches:
        weights.append(safe_float(match.group(1)))
    
    # Pattern 3: "217 kg" -> convert to ton
    pattern3 = r'(\d+\.?\d*)\s*kg\b'
    matches = re.finditer(pattern3, text, re.IGNORECASE)
    for match in matches:
        weights.append(safe_float(match.group(1)) / 1000)
    
    return weights

def extract_position_patterns(text):
    """Extract position values (x from midship) from text"""
    positions = []
    
    # Pattern 1: "x = -5", "x: -5", "x -5"
    pattern1 = r'x\s*[=:]\s*(-?\d+\.?\d*)\s*(?:m|meter)?'
    matches = re.finditer(pattern1, text, re.IGNORECASE)
    for match in matches:
        positions.append(safe_float(match.group(1)))
    
    # Pattern 2: "from midship: -5", "position: -5"
    pattern2 = r'(?:from\s+midship|position|pos)\s*[=:]\s*(-?\d+\.?\d*)\s*(?:m|meter)?'
    matches = re.finditer(pattern2, text, re.IGNORECASE)
    for match in matches:
        positions.append(safe_float(match.group(1)))
    
    # Pattern 3: "FWD -5m", "AFT +5m" (negative for forward, positive for aft)
    pattern3 = r'(?:FWD|Forward)\s*(-?\d+\.?\d*)\s*(?:m|meter)?'
    matches = re.finditer(pattern3, text, re.IGNORECASE)
    for match in matches:
        val = safe_float(match.group(1))
        if val is not None:
            positions.append(-abs(val))  # FWD is negative
    
    pattern4 = r'(?:AFT|Aft)\s*(\+?\d+\.?\d*)\s*(?:m|meter)?'
    matches = re.finditer(pattern4, text, re.IGNORECASE)
    for match in matches:
        val = safe_float(match.group(1))
        if val is not None:
            positions.append(abs(val))  # AFT is positive
    
    return positions

def extract_stage_data(pdf_path):
    """Extract stage data from PDF"""
    if not os.path.exists(pdf_path):
        print(f"✗ ERROR: PDF file not found: {pdf_path}")
        return None
    
    stage_data = {
        "Stage 1": {"W": 217, "x": -5, "source": "known"},
        "Stage 2": {"W": 217, "x": -5, "source": "known"},
        "Stage 3": {"W": None, "x": None, "source": "PDF"},
        "Stage 4": {"W": None, "x": None, "source": "PDF"},
        "Stage 5": {"W": None, "x": None, "source": "PDF"},
    }
    
    print(f"\nProcessing PDF: {pdf_path}")
    print("="*70)
    
    try:
        with pdfplumber.open(pdf_path) as pdf:
            full_text = ""
            
            # Extract text from all pages
            for page_num, page in enumerate(pdf.pages, 1):
                text = page.extract_text()
                if text:
                    full_text += f"\n--- Page {page_num} ---\n{text}\n"
            
            # Search for each stage
            for stage_num in [3, 4, 5]:
                stage_key = f"Stage {stage_num}"
                print(f"\n[{stage_key}] Searching...")
                
                # Find stage section in text
                stage_pattern = rf'Stage\s+{stage_num}[^\n]*'
                stage_matches = list(re.finditer(stage_pattern, full_text, re.IGNORECASE))
                
                if not stage_matches:
                    print(f"  ⚠ Stage {stage_num} not found in text")
                    continue
                
                # Extract context around each match (500 chars before and after)
                for match in stage_matches:
                    start = max(0, match.start() - 500)
                    end = min(len(full_text), match.end() + 500)
                    context = full_text[start:end]
                    
                    print(f"  → Found at position {match.start()}")
                    print(f"  → Context preview: {context[:200]}...")
                    
                    # Extract weights
                    weights = extract_weight_patterns(context)
                    if weights:
                        # Filter reasonable weights (50-500 tons for transformer)
                        reasonable_weights = [w for w in weights if 50 <= w <= 500]
                        if reasonable_weights:
                            stage_data[stage_key]["W"] = reasonable_weights[0]
                            print(f"  ✓ Weight found: {reasonable_weights[0]} t")
                    
                    # Extract positions
                    positions = extract_position_patterns(context)
                    if positions:
                        # Filter reasonable positions (-30 to +30 m from midship)
                        reasonable_positions = [p for p in positions if -30 <= p <= 30]
                        if reasonable_positions:
                            stage_data[stage_key]["x"] = reasonable_positions[0]
                            print(f"  ✓ Position found: {reasonable_positions[0]} m")
            
            # Also try extracting from tables
            print("\n[Tables] Searching for stage data in tables...")
            for page_num, page in enumerate(pdf.pages, 1):
                tables = page.extract_tables()
                for table_idx, table in enumerate(tables):
                    if not table or len(table) < 2:
                        continue
                    
                    # Look for stage headers
                    for row_idx, row in enumerate(table):
                        if not row:
                            continue
                        
                        row_text = " ".join([str(cell) if cell else "" for cell in row])
                        
                        # Check if row contains stage information
                        for stage_num in [3, 4, 5]:
                            if re.search(rf'Stage\s+{stage_num}', row_text, re.IGNORECASE):
                                stage_key = f"Stage {stage_num}"
                                print(f"  → Found {stage_key} in table (Page {page_num}, Table {table_idx+1}, Row {row_idx+1})")
                                
                                # Try to extract W and x from this row
                                row_str = " ".join([str(cell) if cell else "" for cell in row])
                                
                                # Extract weight
                                weights = extract_weight_patterns(row_str)
                                if weights and not stage_data[stage_key]["W"]:
                                    reasonable_weights = [w for w in weights if 50 <= w <= 500]
                                    if reasonable_weights:
                                        stage_data[stage_key]["W"] = reasonable_weights[0]
                                        print(f"    ✓ Weight from table: {reasonable_weights[0]} t")
                                
                                # Extract position
                                positions = extract_position_patterns(row_str)
                                if positions and not stage_data[stage_key]["x"]:
                                    reasonable_positions = [p for p in positions if -30 <= p <= 30]
                                    if reasonable_positions:
                                        stage_data[stage_key]["x"] = reasonable_positions[0]
                                        print(f"    ✓ Position from table: {reasonable_positions[0]} m")
    
    except Exception as e:
        print(f"✗ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return None
    
    return stage_data

def print_results(stage_data):
    """Print results in table format"""
    print("\n" + "="*70)
    print("EXTRACTED STAGE DATA")
    print("="*70)
    print(f"{'Stage':<10} {'W_stage_t':<12} {'x_stage_m':<12} {'Source':<10}")
    print("-"*70)
    
    for stage in ["Stage 1", "Stage 2", "Stage 3", "Stage 4", "Stage 5"]:
        w = stage_data[stage]["W"]
        x = stage_data[stage]["x"]
        source = stage_data[stage]["source"]
        
        w_str = f"{w:.0f}" if w is not None else "N/A"
        x_str = f"{x:.1f}" if x is not None else "N/A"
        
        print(f"{stage:<10} {w_str:<12} {x_str:<12} {source:<10}")
    
    print("="*70)
    
    # Excel input format
    print("\nExcel Input Format (copy to RORO_Stage_Scenarios sheet):")
    print("-"*70)
    for stage in ["Stage 3", "Stage 4", "Stage 5"]:
        w = stage_data[stage]["W"]
        x = stage_data[stage]["x"]
        
        if w is not None and x is not None:
            print(f"{stage}: W_stage_t = {w:.0f}, x_stage_m = {x:.1f}")
        elif w is not None:
            print(f"{stage}: W_stage_t = {w:.0f}, x_stage_m = [NOT FOUND]")
        elif x is not None:
            print(f"{stage}: W_stage_t = [NOT FOUND], x_stage_m = {x:.1f}")
        else:
            print(f"{stage}: [NOT FOUND]")

def main():
    """Main execution"""
    print("="*70)
    print("Stage W and X Value Extractor from PDF")
    print("="*70)
    
    stage_data = extract_stage_data(PDF_PATH)
    
    if stage_data:
        print_results(stage_data)
    else:
        print("\n✗ Failed to extract stage data")

if __name__ == "__main__":
    main()

