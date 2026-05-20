from fastapi import APIRouter, HTTPException, Depends, status
from pydantic import BaseModel, Field
from typing import Dict, List, Any
from sqlalchemy.orm import Session

# Import your database core layers and models
from app.database import get_db
from app.room_core_grc.models import GovernanceAssessment

# Import the monetization tier guard we just created
from app.auth.monetization import SubscriptionGuard

router = APIRouter(
    prefix="/grc",
    tags=["Normal GRC - RegTech Frameworks"]
)

# 1. ENTERPRISE GOVERNANCE INTAKE SCHEMAS
class KingVChecklistInput(BaseModel):
    company_name: str = Field(..., example="Ethical Edge Corporate Client")
    ethical_culture_verified: bool = Field(..., description="King V Principle 1-3 Compliance")
    corporate_citizenship_verified: bool = Field(..., description="King V Principle 4-5 Compliance")
    effective_control_mechanisms: bool = Field(..., description="King V Principle 6-10 Compliance")
    stakeholder_legitimacy_verified: bool = Field(..., description="King V Principle 11-16 Compliance")
    additional_metric_flags: Dict[str, bool] = Field(default_factory=dict, example={"data_privacy_shield": True})

class InherentRiskInput(BaseModel):
    risk_title: str = Field(..., example="Cross-Border Data Transfer Leak")
    impact_score: int = Field(..., ge=1, le=5, description="Scale of 1 (Minimal) to 5 (Catastrophic)")
    probability_score: int = Field(..., ge=1, le=5, description="Scale of 1 (Rare) to 5 (Almost Certain)")

# 2. APPLICATION STATUS ENDPOINT
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

# 3. DATABASE-INTEGRATED KING V COMPLIANCE ENDPOINT (WITH MONETIZATION GUARD)
@router.post("/evaluate-king-v", status_code=status.HTTP_201_CREATED)
async def evaluate_king_v_compliance(
    checklist: KingVChecklistInput, 
    tenant_id: str, # Requires the client to pass their UUID token
    db: Session = Depends(get_db),
    _sub_check = Depends(SubscriptionGuard(required_room="core_grc")) # Intercepts and validates payment status
):
    """
    Ingests a corporate governance checklist, checks if the tenant has paid for this tier,
    computes King V compliance, and logs the assessment metadata straight into PostgreSQL.
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
    
    # Map corporate standing categories and statuses for database recording
    if compliance_percentage == 100.0:
        standing = "EXCELLENT - FULL KING V ALIGNMENT"
        compliance_status = "FULLY_COMPLIANT"
    elif compliance_percentage >= 75.0:
        standing = "SATISFACTORY - MINOR REFORM REQUIRED"
        compliance_status = "PARTIALLY_COMPLIANT"
    else:
        standing = "NON_COMPLIANT - URGENT GOVERNANCE REMEDIATION REQUIRED"
        compliance_status = "NON_COMPLIANT"

    # Instantiate the database row using our relational model mapping
    assessment_record = GovernanceAssessment(
        company_name=checklist.company_name,
        framework_standard="KING_V",
        transparency_score=100.0 if checklist.stakeholder_legitimacy_verified else 50.0,
        accountability_index=compliance_percentage,
        overall_compliance_percentage=compliance_percentage,
        compliance_status=compliance_status,
        assessment_metadata={
            "pillar_breakdown": pillars,
            "corporate_governance_standing": standing,
            "additional_metric_flags": checklist.additional_metric_flags,
            "verified_tenant_id": tenant_id
        }
    )

    # Securely commit transaction to the PostgreSQL database instance
    db.add(assessment_record)
    db.commit()
    db.refresh(assessment_record)

    return {
        "assessment_id": str(assessment_record.id),
        "company_name": assessment_record.company_name,
        "evaluation_metric": {
            "total_pillars_assessed": 4,
            "pillars_passed": passed_count,
            "calculated_compliance_rating": f"{compliance_percentage}%"
        },
        "pillar_breakdown": pillars,
        "corporate_governance_standing": standing,
        "database_sync": "RECORD_COMMITTED"
    }

# 4. QUANTITATIVE RISK MATRIX ENDPOINT
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
