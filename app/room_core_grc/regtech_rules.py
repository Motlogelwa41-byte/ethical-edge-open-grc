from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Dict, List

router = APIRouter(
    prefix="/grc",
    tags=["Normal GRC - RegTech Frameworks"]
)

# 1. ENTERPRISE GOVERNANCE INTAKE SCHEMAS
class KingVChecklistInput(BaseModel):
    company_name: str
    ethical_culture_verified: bool = Field(..., description="King V Principle 1-3 Compliance")
    corporate_citizenship_verified: bool = Field(..., description="King V Principle 4-5 Compliance")
    effective_control_mechanisms: bool = Field(..., description="King V Principle 6-10 Compliance")
    stakeholder_legitimacy_verified: bool = Field(..., description="King V Principle 11-16 Compliance")
    additional_metric_flags: Dict[str, bool] = Field(default_factory=dict, example={"data_privacy_shield": True})

class InherentRiskInput(BaseModel):
    risk_title: str
    impact_score: int = Field(..., ge=1, le=5, description="Scale of 1 (Minimal) to 5 (Catastrophic)")
    probability_score: int = Field(..., ge=1, le=5, description="Scale of 1 (Rare) to 5 (Almost Certain)")

# 2. APPLICATION LOGIC ENDPOINTS
@router.get("/status")
async def get_grc_status():
    """
    Returns the real-time versioning and alignment matrix of the baseline RegTech module.
    """
    return {
        "room": "Normal GRC - RegTech Core",
        "engine_status": "ACTIVE",
        "governance_standard": "King V Principles Integration Layer",
        "jurisdiction_focus": "Botswana / SADC Regional Enterprise Markets",
        "compliance_tracking_state": "OPERATIONAL"
    }

@router.post("/evaluate-king-v")
async def evaluate_king_v_compliance(checklist: KingVChecklistInput):
    """
    Ingests a corporate governance checklist and computes a localized King V compliance rating.
    """
    # Track the core pillars based on King V operational outcomes
    pillars = {
        "Ethical Culture": checklist.ethical_culture_verified,
        "Good Performance & Citizenship": checklist.corporate_citizenship_verified,
        "Effective Control Environment": checklist.effective_control_mechanisms,
        "Institutional Legitimacy": checklist.stakeholder_legitimacy_verified
    }
    
    passed_count = sum(1 for status in pillars.values() if status is True)
    compliance_percentage = (passed_count / 4.0) * 100.0
    
    # Define corporate standing categories
    if compliance_percentage == 100.0:
        standing = "EXCELLENT - FULL KING V ALIGNMENT"
    elif compliance_percentage >= 75.0:
        standing = "SATISFACTORY - MINOR REFORM REQUIRED"
    else:
        standing = "NON_COMPLIANT - URGENT GOVERNANCE REMEDIATION REQUIRED"

    return {
        "company_name": checklist.company_name,
        "evaluation_metric": {
            "total_pillars_assessed": 4,
            "pillars_passed": passed_count,
            "calculated_compliance_rating": f"{compliance_percentage}%"
        },
        "pillar_breakdown": pillars,
        "corporate_governance_standing": standing
    }

@router.post("/calculate-matrix")
async def calculate_risk_matrix(risk: InherentRiskInput):
    """
    Computes a standard 5x5 enterprise inherent risk score and generates risk categories.
    """
    inherent_risk_score = risk.impact_score * risk.probability_score
    
    if inherent_risk_score >= 15:
        risk_tier = "CRITICAL RISK"
        remediation_window = "Immediate Action Required / Board Level Escalation"
    elif inherent_risk_score >= 8:
        risk_tier = "MEDIUM RISK"
        remediation_window = "Quarterly Monitoring / Management Mitigation"
    else:
        risk_tier = "LOW RISK"
        remediation_window = "Routine Operational Logging"

    return {
        "risk_title": risk.risk_title,
        "matrix_metrics": {
            "impact_input": risk.impact_score,
            "probability_input": risk.probability_score,
            "calculated_inherent_score": inherent_risk_score
        },
        "risk_classification": risk_tier,
        "governance_action_protocol": remediation_window
    }
