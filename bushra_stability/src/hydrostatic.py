"""
Hydrostatic data interpolation engine using SciPy RegularGridInterpolator.

This module provides 2D and 3D interpolation for hydrostatic tables and KN curves.
Based on patch.md implementation with SciPy for improved accuracy.
"""
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import warnings

import numpy as np
import pandas as pd
from scipy.interpolate import RegularGridInterpolator

warnings.filterwarnings("ignore", category=UserWarning)


class HydroEngine:
    """
    Hydrostatic data interpolation engine.
    
    Provides 2D interpolation (Displacement × Trim) for hydrostatic properties
    and 3D interpolation (Displacement × Trim × Heel) for KN curves.
    """
    
    def __init__(self, hydro_path: Path, kn_path: Path):
        """
        Initialize hydrostatic engine with CSV data files.
        
        Args:
            hydro_path: Path to hydrostatics CSV file
            kn_path: Path to KN table CSV file
            
        Raises:
            FileNotFoundError: If CSV files don't exist
            ValueError: If required columns are missing
        """
        self.hydro_df = pd.read_csv(hydro_path)
        self.kn_df = pd.read_csv(kn_path)
        
        # Initialize interpolators
        self._build_hydro_interpolators()
        self._build_kn_interpolator()
        
    def _pick_col(self, df: pd.DataFrame, names: List[str]) -> str:
        """Pick column by name (case-insensitive)."""
        col_map = {c.lower(): c for c in df.columns}
        for name in names:
            if name.lower() in col_map:
                return col_map[name.lower()]
        raise KeyError(f"Missing any of {names} in {list(df.columns)}")
    
    def _build_hydro_interpolators(self):
        """Build 2D interpolators for hydrostatic properties."""
        # Extract and sort unique values
        trim_col = self._pick_col(self.hydro_df, ["Trim", "trim_m"])
        disp_col = self._pick_col(self.hydro_df, ["Displacement", "disp_t"])
        
        trims = np.unique(self.hydro_df[trim_col].values).astype(float)
        disps = np.unique(self.hydro_df[disp_col].values).astype(float)
        trims.sort()
        disps.sort()
        
        # Store axes for reference
        self._hydro_disps = disps
        self._hydro_trims = trims
        
        def make_grid(col_name: str) -> np.ndarray:
            """Create 2D grid for a hydrostatic property."""
            # Pivot: index=Displacement, columns=Trim
            p = self.hydro_df.pivot(
                index=disp_col,
                columns=trim_col,
                values=col_name
            )
            # Reindex to sorted axes
            p = p.reindex(index=disps, columns=trims)
            
            # Handle missing values
            if p.isnull().values.any():
                p = (
                    p.interpolate(axis=0)
                    .ffill()
                    .bfill()
                    .interpolate(axis=1)
                    .ffill()
                    .bfill()
                )
            
            return p.values  # shape: (len(disps), len(trims))
        
        # Build interpolators for each property
        self.hydro_interpolators = {}
        for col in ["Draft", "LCB", "VCB", "KMT", "MTC", "TCP"]:
            try:
                col_name = self._pick_col(self.hydro_df, [col, f"{col}_m", f"{col}_t_m_cm"])
                grid = make_grid(col_name)
                self.hydro_interpolators[col] = RegularGridInterpolator(
                    (disps, trims),
                    grid,
                    bounds_error=False,
                    fill_value=None
                )
            except KeyError:
                # Property not available, skip
                continue
    
    def _build_kn_interpolator(self):
        """Build 3D interpolator for KN curves."""
        # Extract and sort unique values
        trim_col = self._pick_col(self.kn_df, ["Trim", "trim_m"])
        disp_col = self._pick_col(self.kn_df, ["Displacement", "disp_t"])
        
        kn_trims = np.unique(self.kn_df[trim_col].values).astype(float)
        kn_disps = np.unique(self.kn_df[disp_col].values).astype(float)
        kn_trims.sort()
        kn_disps.sort()
        
        # Extract heel angles from column names
        heel_cols = [c for c in self.kn_df.columns if c.lower().startswith("heel_")]
        if not heel_cols:
            raise ValueError("No Heel_* columns found in KN table")
        
        heel_deg = np.array(
            [float(c.split("_")[1]) for c in heel_cols],
            dtype=float
        )
        heel_deg.sort()
        
        # Store for reference
        self._kn_disps = kn_disps
        self._kn_trims = kn_trims
        self._heel_deg = heel_deg
        
        # Build 3D tensor: (ndisp, ntrim, nheel)
        kn_tensor = np.empty(
            (len(kn_disps), len(kn_trims), len(heel_deg)),
            dtype=float
        )
        
        for j, hcol in enumerate(heel_cols):
            # Pivot for each heel angle
            p = self.kn_df.pivot(
                index=disp_col,
                columns=trim_col,
                values=hcol
            )
            # Reindex to sorted axes
            p = p.reindex(index=kn_disps, columns=kn_trims)
            
            # Handle missing values
            if p.isnull().values.any():
                p = (
                    p.interpolate(axis=0)
                    .ffill()
                    .bfill()
                    .interpolate(axis=1)
                    .ffill()
                    .bfill()
                )
            
            kn_tensor[:, :, j] = p.values
        
        # Create 3D interpolator
        self.kn_interpolator = RegularGridInterpolator(
            (kn_disps, kn_trims, heel_deg),
            kn_tensor,
            bounds_error=False,
            fill_value=None
        )
    
    def mean_draft(self, disp_t: float, trim_m: float = 0.0) -> float:
        """
        Get mean draft for given displacement and trim.
        
        Args:
            disp_t: Displacement in tons
            trim_m: Trim in meters (positive = aft)
            
        Returns:
            Mean draft in meters
        """
        if "Draft" not in self.hydro_interpolators:
            raise ValueError("Draft interpolator not available")
        
        pt = np.array([[disp_t, trim_m]])  # shape (1, 2)
        result = self.hydro_interpolators["Draft"](pt)
        return float(np.asarray(result).squeeze())
    
    def LCB(self, disp_t: float, trim_m: float = 0.0) -> float:
        """
        Get LCB (Longitudinal Center of Buoyancy) for given displacement and trim.
        
        Args:
            disp_t: Displacement in tons
            trim_m: Trim in meters (positive = aft)
            
        Returns:
            LCB in meters
        """
        if "LCB" not in self.hydro_interpolators:
            raise ValueError("LCB interpolator not available")
        
        pt = np.array([[disp_t, trim_m]])
        result = self.hydro_interpolators["LCB"](pt)
        return float(np.asarray(result).squeeze())
    
    def KMT(self, disp_t: float, trim_m: float = 0.0) -> float:
        """
        Get KMT (Transverse Metacentric Height) for given displacement and trim.
        
        Args:
            disp_t: Displacement in tons
            trim_m: Trim in meters (positive = aft)
            
        Returns:
            KMT in meters
        """
        if "KMT" not in self.hydro_interpolators:
            raise ValueError("KMT interpolator not available")
        
        pt = np.array([[disp_t, trim_m]])
        result = self.hydro_interpolators["KMT"](pt)
        return float(np.asarray(result).squeeze())
    
    def MTC(self, disp_t: float, trim_m: float = 0.0) -> float:
        """
        Get MTC (Moment to Change Trim) for given displacement and trim.
        
        Args:
            disp_t: Displacement in tons
            trim_m: Trim in meters (positive = aft)
            
        Returns:
            MTC in t·m/cm
        """
        if "MTC" not in self.hydro_interpolators:
            raise ValueError("MTC interpolator not available")
        
        pt = np.array([[disp_t, trim_m]])
        result = self.hydro_interpolators["MTC"](pt)
        return float(np.asarray(result).squeeze())
    
    def KN(self, disp_t: float, heel_deg: float, trim_m: float = 0.0) -> float:
        """
        Get KN (Righting Arm) for given displacement, trim, and heel angle.
        
        Args:
            disp_t: Displacement in tons
            heel_deg: Heel angle in degrees
            trim_m: Trim in meters (positive = aft)
            
        Returns:
            KN in meters
        """
        if self.kn_interpolator is None:
            raise ValueError("KN interpolator not available")
        
        # Clip heel to valid range
        heel_deg = np.clip(heel_deg, self._heel_deg.min(), self._heel_deg.max())
        
        pt = np.array([[disp_t, trim_m, heel_deg]])  # shape (1, 3)
        result = self.kn_interpolator(pt)
        return float(np.asarray(result).squeeze())
    
    def KN_curve(
        self,
        disp_t: float,
        heel_angles_deg: List[int],
        trim_m: float = 0.0
    ) -> Dict[int, float]:
        """
        Get KN curve for multiple heel angles.
        
        Args:
            disp_t: Displacement in tons
            heel_angles_deg: List of heel angles in degrees
            trim_m: Trim in meters (positive = aft)
            
        Returns:
            Dictionary mapping heel angle (deg) to KN (m)
        """
        if self.kn_interpolator is None:
            raise ValueError("KN interpolator not available")
        
        # Clip angles to valid range
        heels = np.clip(
            np.array(heel_angles_deg, dtype=float),
            self._heel_deg.min(),
            self._heel_deg.max()
        )
        
        # Build points array: (n_points, 3)
        points = np.array([
            [disp_t, trim_m, h] for h in heels
        ])
        
        # Interpolate all at once
        results = self.kn_interpolator(points)
        kn_values = np.asarray(results).squeeze()
        
        # Convert to dictionary
        return {
            int(angle): float(kn)
            for angle, kn in zip(heel_angles_deg, kn_values)
        }
    
    @property
    def heel_angles_deg(self) -> np.ndarray:
        """Get available heel angles in degrees."""
        return self._heel_deg.copy()
    
    @property
    def displacement_range(self) -> Tuple[float, float]:
        """Get displacement range (min, max)."""
        return (float(self._hydro_disps.min()), float(self._hydro_disps.max()))
    
    @property
    def trim_range(self) -> Tuple[float, float]:
        """Get trim range (min, max)."""
        return (float(self._hydro_trims.min()), float(self._hydro_trims.max()))

