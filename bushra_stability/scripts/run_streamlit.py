#!/usr/bin/env python
"""
Run the BUSHRA Stability Calculation Streamlit app.

This script sets up the Python path and runs the Streamlit app as a module.
"""
import sys
import os
from pathlib import Path

# Get project root directory
base_path = Path(__file__).parent.parent.resolve()
src_path = base_path / "src"

# Add src to Python path
if str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))

# Set PYTHONPATH environment variable for subprocess
os.environ["PYTHONPATH"] = str(src_path)

if __name__ == "__main__":
    # Change to project root for relative paths
    original_cwd = os.getcwd()
    try:
        os.chdir(str(base_path))
        
        # Run streamlit as module: python -m streamlit run src/streamlit_app.py
        app_path = src_path / "streamlit_app.py"
        
        # Use subprocess to run streamlit with proper environment
        import subprocess
        result = subprocess.run(
            [sys.executable, "-m", "streamlit", "run", str(app_path)],
            cwd=str(base_path),
            env=os.environ.copy()
        )
        sys.exit(result.returncode)
    finally:
        os.chdir(original_cwd)

