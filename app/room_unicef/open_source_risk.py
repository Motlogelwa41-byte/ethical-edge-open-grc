from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import List, Dict

router = APIRouter(
    prefix="/unicef",
    tags=["UNICEF Challenge - Open-Source Risk Engine"]
)

# 1. UNICEF CLIMATE RISK AND OPEN-SOURCE DATA MODELS
class ClimateRiskAssessmentInput(BaseModel):
    district_location: str = Field(..., example="Chobe / Okavango")
    drought_severity_index: float = Field(..., ge=0.0, le=10.0, description="Localized index from 0 to 10")
    flood_probability_score: float = Field(..., ge=0.0, le=10.0, description="Localized index from 0 to 10")
    impacted_youth_infrastructure: List[str] = Field(..., example=["primary_school_a", "maternal_health_clinic"])

class OpenSourceComplianceInput(BaseModel):
    repository_url: str
    license_type: str = Field(..., example="MIT")
    is_public_repository: bool
    has_documentation_readme: bool
    dependency_audit_passed: bool

# 2. ENDPOINTS
@router.get("/status")
async def get_unicef_room_status():
    """
    Returns the technical status of the Child-Centric Climate GRC Engine.
    """
    return {
        "room": "UNICEF Frontier Tech Challenge",
        "engine_status": "ACTIVE",
        "focus": "AI-Driven Open-Source Climate Risk Mapping & Youth Vulnerability Analytics",
        "funding_framework_alignment": "UNICEF Venture Fund Open Source & AI Safety Guidelines",
        "deployment_tier": "PREPPED_FOR_SANDBOX"
    }

@router.post("/evaluate-climate-risk")
async def evaluate_child_centric_risk(assessment: ClimateRiskAssessmentInput):
    """
    Computes localized climate vulnerability scores specifically scaled to youth infrastructure impact.
    """
    # Algorithmic hazard metric calculation
    base_hazard_score = (assessment.drought_severity_index + assessment.flood_probability_score) / 2.0
    
    # Infrastructure multiplier (more school/clinic exposure increases child-centric vulnerability)
    infrastructure_multiplier = len(assessment.impacted_youth_infrastructure) * 1.5
    final_vulnerability_index = round(base_hazard_score + infrastructure_multiplier, 2)
    
    # Scale categorization for intervention prioritization
    if final_vulnerability_index >= 12.0:
        intervention_priority = "IMMEDIATE - EMERGENCY VENTURE FUNDING TRIGGERED"
    elif final_vulnerability_index >= 6.0:
        intervention_priority = "MEDIUM - ADAPTATION PLANNING LOGGED"
    else:
        intervention_priority = "LOW - ROUTINE ENVIRONMENTAL MONITORING"

    return {
        "geography_monitored": assessment.district_location,
        "vulnerability_metrics": {
            "calculated_base_hazard": base_hazard_score,
            "infrastructure_exposure_count": len(assessment.impacted_youth_infrastructure),
            "final_child_vulnerability_index": final_vulnerability_index
        },
        "unicef_grant_action_tier": intervention_priority
    }

@router.post("/validate-open-source")
async def validate_open_source_compliance(compliance: OpenSourceComplianceInput):
    """
    Enforces strict UNICEF Venture Fund eligibility criteria regarding public repository licensing.
    """
    # UNICEF fund requires permissive open-source licenses (MIT, Apache-2.0, BSD, GPL-3.0)
    approved_licenses = ["MIT", "Apache-2.0", "GPL-3.0", "BSD-3-Clause", "BSD-2-Clause"]
    
    license_valid = compliance.license_type in approved_licenses
    
    # Scoring strict validation variables
    compliance_checks = {
        "approved_permissive_license": license_valid,
        "public_repository_access": compliance.is_public_repository,
        "developer_documentation_present": compliance.has_documentation_readme,
        "clean_dependencies_verified": compliance.dependency_audit_passed
    }
    
    is_fully_compliant = all(compliance_checks.values())

    return {
        "repository_target": compliance.repository_url,
        "compliance_matrix": compliance_checks,
        "unicef_eligibility_status": "APPROVED_FOR_FUNDING_CONSIDERATION" if is_fully_compliant else "REJECTED_NON_COMPLIANT_OPEN_SOURCE"
    }
