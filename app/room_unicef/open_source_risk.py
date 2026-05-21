from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from typing import List, Dict, Any
from sqlalchemy.orm import Session

# Import your database core layer and models
from app.database import get_db
from app.room_unicef.models import ClimateRiskAssessment

# Import the monetization tier guard
from app.auth.monetization import SubscriptionGuard

router = APIRouter(
    prefix="/unicef",
    tags=["UNICEF Challenge - Open-Source Risk Engine"]
)

# 1. UNICEF CLIMATE RISK AND OPEN-SOURCE INPUT SCHEMAS
class ClimateRiskAssessmentInput(BaseModel):
    district_location: str = Field(..., example="Chobe / Okavango")
    drought_severity_index: float = Field(..., ge=0.0, le=10.0, description="Localized index from 0 to 10")
    flood_probability_score: float = Field(..., ge=0.0, le=10.0, description="Localized index from 0 to 10")
    impacted_youth_infrastructure: List[str] = Field(..., example=["primary_school_a", "maternal_health_clinic"])

class OpenSourceComplianceInput(BaseModel):
    repository_url: str = Field(..., example="https://github.com/ethical-edge/open-grc-engine")
    license_type: str = Field(..., example="MIT")
    is_public_repository: bool = Field(..., example=True)
    has_documentation_readme: bool = Field(..., example=True)
    dependency_audit_passed: bool = Field(..., example=True)

# 2. STATUS TRACKING ENDPOINT
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

# 3. DATABASE-INTEGRATED CLIMATE VULNERABILITY COMPONENT (WITH MONETIZATION GUARD)
@router.post("/evaluate-climate-risk", status_code=status.HTTP_201_CREATED)
async def evaluate_child_centric_risk(
    assessment: ClimateRiskAssessmentInput, 
    tenant_id: str, # Requires the client to pass their UUID token
    db: Session = Depends(get_db),
    _sub_check = Depends(SubscriptionGuard(required_room="unicef")) # Verifies Professional/Enterprise tier
):
    """
    Computes localized climate vulnerability scores scaled to youth infrastructure impact,
    checks if the tenant has paid for this tier, and logs the assessment directly to PostgreSQL.
    """
    # Calculate algorithmic hazard metrics matching your model logic
    base_hazard_score = (assessment.drought_severity_index + assessment.flood_probability_score) / 2.0
    infrastructure_multiplier = len(assessment.impacted_youth_infrastructure) * 1.5
    final_vulnerability_index = round(base_hazard_score + infrastructure_multiplier, 2)
    
    # Scale categorization for programmatic intervention
    if final_vulnerability_index >= 12.0:
        intervention_priority = "IMMEDIATE - EMERGENCY VENTURE FUNDING TRIGGERED"
        impact_rating = "CRITICAL"
    elif final_vulnerability_index >= 6.0:
        intervention_priority = "MEDIUM - ADAPTATION PLANNING LOGGED"
        impact_rating = "HIGH"
    else:
        intervention_priority = "LOW - ROUTINE ENVIRONMENTAL MONITORING"
        impact_rating = "LOW"

    # Normalize your input fields into our Postgres relational structure
    risk_record = ClimateRiskAssessment(
        district=assessment.district_location,
        hazard_type="COMBINED_CLIMATE_STRESS",
        environmental_hazard_score=round(base_hazard_score / 10.0, 4),
        infrastructure_vulnerability_index=round(min(infrastructure_multiplier / 10.0, 1.0), 4),
        calculated_impact_rating=impact_rating,
        modeled_parameters={
            "drought_severity_index": assessment.drought_severity_index,
            "flood_probability_score": assessment.flood_probability_score,
            "impacted_youth_infrastructure": assessment.impacted_youth_infrastructure,
            "calculated_child_vulnerability_index": final_vulnerability_index,
            "unicef_grant_action_tier": intervention_priority,
            "verified_tenant_id": tenant_id
        }
    )
    
    # Commit transaction block to database pool
    db.add(risk_record)
    db.commit()
    db.refresh(risk_record)

    return {
        "assessment_id": str(risk_record.id),
        "geography_monitored": risk_record.district,
        "vulnerability_metrics": {
            "calculated_base_hazard": base_hazard_score,
            "infrastructure_exposure_count": len(assessment.impacted_youth_infrastructure),
            "final_child_vulnerability_index": final_vulnerability_index
        },
        "unicef_grant_action_tier": intervention_priority,
        "database_sync": "RECORD_COMMITTED"
    }

# 4. OPEN SOURCE ETHICAL COMPLIANCE ENDPOINT
@router.post("/validate-open-source")
async def validate_open_source_compliance(
    compliance: OpenSourceComplianceInput,
    tenant_id: str,
    _sub_check = Depends(SubscriptionGuard(required_room="unicef"))
):
    """
    Enforces strict open-source licensing compliance checks for authorized Professional/Enterprise tiers.
    """
    approved_licenses = ["MIT", "Apache-2.0", "GPL-3.0", "BSD-3-Clause", "BSD-2-Clause"]
    license_valid = compliance.license_type in approved_licenses
    
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
