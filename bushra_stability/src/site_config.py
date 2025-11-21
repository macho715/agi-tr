"""
Site-specific configuration for DAS Island and AGI Site RORO operations.

This module implements site-specific requirements based on:
- DAS Island: Mina Zayed departure, strict PTW, HM pilotage
- AGI Site: Khalifa Port departure, relaxed PTW, exemption available

Reference: 변압기 섬행 RORO 운송 표준 지침 v1.2-patch (2025-11-10)
"""
from enum import Enum
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any
import warnings


class SiteType(Enum):
    """Site types for RORO operations."""
    DAS_ISLAND = "DAS"
    AGI_SITE = "AGI"
    UNKNOWN = "UNKNOWN"


@dataclass
class SiteRequirements:
    """Site-specific requirements for RORO operations."""
    
    site_type: SiteType
    site_name: str
    departure_port: str
    arrival_jetty: str
    
    # PTW (Permit to Work) requirements
    ptw_lead_time_hours: int
    ptw_hot_work_restricted: bool
    
    # Navigation requirements
    pilotage_required: bool
    pilotage_exemption_available: bool
    harbor_master_approval: bool
    
    # RORO operational limits
    max_ramp_angle_deg: float
    lashing_points_required: int
    max_trim_m: float
    
    # Gate pass requirements
    gate_pass_validity_hours: int
    gate_pass_system: str  # "ATLP + Security Clearance"
    
    # Reporting requirements
    incident_report_hours: int
    final_report_days: int
    photo_evidence_minimum: int
    
    # Optional/default fields (must come after required fields)
    min_gm_m: float = 0.15  # IMO minimum
    max_gm_m: Optional[float] = None
    
    # Ballast requirements (if applicable)
    ballast_requirements: Dict[str, Any] = field(default_factory=dict)
    
    # Additional checks
    additional_checks: List[str] = field(default_factory=list)
    
    @classmethod
    def get_das_requirements(cls) -> 'SiteRequirements':
        """
        Get DAS Island site requirements.
        
        Reference: DAS Island operations from guideline Section 2.1
        """
        return cls(
            site_type=SiteType.DAS_ISLAND,
            site_name="DAS Island",
            departure_port="Mina Zayed",
            arrival_jetty="DAS Jetty",
            ptw_lead_time_hours=48,
            ptw_hot_work_restricted=True,
            pilotage_required=True,
            pilotage_exemption_available=False,
            harbor_master_approval=True,
            max_ramp_angle_deg=8.0,
            lashing_points_required=12,
            max_trim_m=0.50,
            gate_pass_validity_hours=24,
            gate_pass_system="ATLP + DAS Security Clearance",
            incident_report_hours=1,
            final_report_days=7,
            photo_evidence_minimum=18,
            ballast_requirements={
                "real_time_gm_monitoring": True,
                "berth_load_chart_required": True,
                "ramp_plate_cert_required": True,
            },
            additional_checks=[
                "DAS Berth Load Chart",
                "DAS Pilotage Request Form",
                "DAS Security Clearance",
                "Ramp Angle Calculation (≤8°)",
                "12-point Lashing with GPS photos",
            ]
        )
    
    @classmethod
    def get_agi_requirements(cls) -> 'SiteRequirements':
        """
        Get AGI Site requirements.
        
        Reference: AGI Site operations from guideline Section 2.1
        """
        return cls(
            site_type=SiteType.AGI_SITE,
            site_name="AGI Site",
            departure_port="Khalifa Port",
            arrival_jetty="AGI Quay",
            ptw_lead_time_hours=24,
            ptw_hot_work_restricted=False,
            pilotage_required=False,
            pilotage_exemption_available=True,
            harbor_master_approval=True,
            max_ramp_angle_deg=10.0,
            lashing_points_required=10,
            max_trim_m=0.50,
            gate_pass_validity_hours=48,
            gate_pass_system="ATLP + AGI ePass",
            incident_report_hours=2,
            final_report_days=7,
            photo_evidence_minimum=15,
            ballast_requirements={
                "stability_template_required": True,
                "mws_pre_verification": True,
                "ramp_plate_strength": "150t/m²",
            },
            additional_checks=[
                "AGI Stability Template",
                "AGI Ramp Plate Cert (150t/m²)",
                "Pilotage Exemption Cert (if applicable)",
                "AGI Trim Control Sheet",
                "10-point Lashing",
            ]
        )
    
    @classmethod
    def from_site_code(cls, site_code: str) -> 'SiteRequirements':
        """
        Create SiteRequirements from site code.
        
        Args:
            site_code: "DAS" or "AGI" or "DAS-001" or "AGI-002"
            
        Returns:
            SiteRequirements object
        """
        site_code_upper = site_code.upper().strip()
        
        if "DAS" in site_code_upper:
            return cls.get_das_requirements()
        elif "AGI" in site_code_upper:
            return cls.get_agi_requirements()
        else:
            warnings.warn(f"Unknown site code '{site_code}', using DAS defaults")
            return cls.get_das_requirements()


def validate_stability_for_site(
    stability_result: Any,  # StabilityResult
    site_req: SiteRequirements,
    verbose: bool = True
) -> Dict[str, Any]:
    """
    Validate stability results against site-specific requirements.
    
    Args:
        stability_result: StabilityResult object from stability.py
        site_req: SiteRequirements for the target site
        verbose: Print validation details
        
    Returns:
        Dictionary with validation results
    """
    checks = {}
    
    # 1. Trim check
    trim_ok = abs(stability_result.trim) <= site_req.max_trim_m
    checks["trim_within_limit"] = {
        "pass": trim_ok,
        "value": stability_result.trim,
        "limit": site_req.max_trim_m,
        "message": f"Trim {stability_result.trim:.3f}m {'OK' if trim_ok else 'EXCEEDS'} limit {site_req.max_trim_m:.2f}m"
    }
    
    # 2. GM check
    gm_ok = stability_result.gm >= site_req.min_gm_m
    checks["gm_sufficient"] = {
        "pass": gm_ok,
        "value": stability_result.gm,
        "limit": site_req.min_gm_m,
        "message": f"GM {stability_result.gm:.3f}m {'OK' if gm_ok else 'BELOW'} minimum {site_req.min_gm_m:.2f}m"
    }
    
    if site_req.max_gm_m:
        gm_high_ok = stability_result.gm <= site_req.max_gm_m
        checks["gm_not_excessive"] = {
            "pass": gm_high_ok,
            "value": stability_result.gm,
            "limit": site_req.max_gm_m,
            "message": f"GM {stability_result.gm:.3f}m {'OK' if gm_high_ok else 'EXCEEDS'} maximum {site_req.max_gm_m:.2f}m"
        }
    
    # 3. Draft checks (generic)
    draft_ok = all([
        stability_result.draft_fwd > 0,
        stability_result.draft_aft > 0,
        stability_result.draft_mean > 0
    ])
    checks["drafts_positive"] = {
        "pass": draft_ok,
        "value": {
            "fwd": stability_result.draft_fwd,
            "aft": stability_result.draft_aft,
            "mean": stability_result.draft_mean
        },
        "message": f"Drafts {'OK' if draft_ok else 'INVALID'}"
    }
    
    # 4. Site-specific checks
    if site_req.site_type == SiteType.DAS_ISLAND:
        # DAS-specific: Real-time GM monitoring requirement
        checks["das_specific"] = {
            "pass": True,  # Placeholder - needs real-time data
            "requirements": site_req.additional_checks,
            "message": "DAS Island additional checks required"
        }
    
    elif site_req.site_type == SiteType.AGI_SITE:
        # AGI-specific: Trim control sheet
        checks["agi_specific"] = {
            "pass": True,  # Placeholder
            "requirements": site_req.additional_checks,
            "message": "AGI Site additional checks required"
        }
    
    # 5. Overall pass
    checks["overall_pass"] = all(
        c.get("pass", False) 
        for k, c in checks.items() 
        if k not in ["das_specific", "agi_specific"]
    )
    
    # Verbose output
    if verbose:
        print(f"\n{'='*60}")
        print(f"Site Validation: {site_req.site_name} ({site_req.site_type.value})")
        print(f"{'='*60}")
        for key, result in checks.items():
            if key == "overall_pass":
                continue
            status = "✅ PASS" if result.get("pass", False) else "❌ FAIL"
            print(f"{status} | {result.get('message', key)}")
        
        print(f"{'='*60}")
        overall = "✅ OVERALL PASS" if checks["overall_pass"] else "❌ OVERALL FAIL"
        print(f"{overall}")
        print(f"{'='*60}\n")
    
    return checks


def generate_site_checklist(site_req: SiteRequirements) -> str:
    """
    Generate site-specific checklist for operations.
    
    Args:
        site_req: SiteRequirements object
        
    Returns:
        Formatted checklist string
    """
    checklist = []
    checklist.append(f"\n{'='*70}")
    checklist.append(f"RORO OPERATION CHECKLIST: {site_req.site_name}")
    checklist.append(f"{'='*70}\n")
    
    checklist.append(f"📍 SITE INFORMATION")
    checklist.append(f"   Departure Port: {site_req.departure_port}")
    checklist.append(f"   Arrival Jetty: {site_req.arrival_jetty}")
    checklist.append(f"   Site Code: {site_req.site_type.value}\n")
    
    checklist.append(f"📋 PRE-OPERATION REQUIREMENTS")
    checklist.append(f"   ☐ PTW submitted ≥{site_req.ptw_lead_time_hours}h before operation")
    if site_req.ptw_hot_work_restricted:
        checklist.append(f"   ☐ Hot Work restrictions confirmed")
    checklist.append(f"   ☐ Gate Pass obtained ({site_req.gate_pass_system})")
    checklist.append(f"   ☐ Valid for {site_req.gate_pass_validity_hours}h")
    if site_req.pilotage_required:
        checklist.append(f"   ☐ Pilotage request submitted and confirmed")
    else:
        checklist.append(f"   ☐ Pilotage exemption verified (if applicable)")
    checklist.append(f"   ☐ Harbor Master approval obtained\n")
    
    checklist.append(f"⚓ OPERATIONAL LIMITS")
    checklist.append(f"   • Max Ramp Angle: ≤{site_req.max_ramp_angle_deg}°")
    checklist.append(f"   • Lashing Points: {site_req.lashing_points_required} points")
    checklist.append(f"   • Max Trim: ≤{site_req.max_trim_m}m")
    checklist.append(f"   • Min GM: ≥{site_req.min_gm_m}m\n")
    
    checklist.append(f"📸 DOCUMENTATION REQUIREMENTS")
    checklist.append(f"   ☐ Minimum {site_req.photo_evidence_minimum} photos with GPS tags")
    checklist.append(f"   ☐ Incident report within {site_req.incident_report_hours}h (if applicable)")
    checklist.append(f"   ☐ Final report within {site_req.final_report_days} days\n")
    
    if site_req.additional_checks:
        checklist.append(f"✓ SITE-SPECIFIC CHECKS")
        for check in site_req.additional_checks:
            checklist.append(f"   ☐ {check}")
        checklist.append("")
    
    checklist.append(f"{'='*70}\n")
    
    return "\n".join(checklist)


# Example usage
if __name__ == "__main__":
    # Test DAS requirements
    das_req = SiteRequirements.get_das_requirements()
    print(generate_site_checklist(das_req))
    
    # Test AGI requirements
    agi_req = SiteRequirements.get_agi_requirements()
    print(generate_site_checklist(agi_req))
    
    # Test site code parsing
    das_from_code = SiteRequirements.from_site_code("DAS-001")
    print(f"\nParsed site code 'DAS-001': {das_from_code.site_name}")
