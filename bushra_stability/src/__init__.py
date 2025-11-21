"""BUSHRA Stability Calculation - Python implementation matching Excel workbook."""

from .displacement import calculate_displacement, WeightItem, DisplacementResult
from .stability import calculate_stability, StabilityResult

# Optional imports (may not be available if dependencies missing)
try:
    from .hydrostatic import HydroEngine
    HYDROSTATIC_AVAILABLE = True
except ImportError:
    HYDROSTATIC_AVAILABLE = False
    HydroEngine = None

try:
    from .imo_check import check_imo_a749
    IMO_CHECK_AVAILABLE = True
except ImportError:
    IMO_CHECK_AVAILABLE = False
    check_imo_a749 = None

try:
    from .site_config import SiteRequirements, validate_stability_for_site, generate_site_checklist
    SITE_CONFIG_AVAILABLE = True
except ImportError:
    SITE_CONFIG_AVAILABLE = False
    SiteRequirements = None
    validate_stability_for_site = None
    generate_site_checklist = None

__all__ = [
    "calculate_displacement",
    "WeightItem",
    "DisplacementResult",
    "calculate_stability",
    "StabilityResult",
    "HydroEngine",
    "check_imo_a749",
    "SiteRequirements",
    "validate_stability_for_site",
    "generate_site_checklist",
    "HYDROSTATIC_AVAILABLE",
    "IMO_CHECK_AVAILABLE",
    "SITE_CONFIG_AVAILABLE",
]

