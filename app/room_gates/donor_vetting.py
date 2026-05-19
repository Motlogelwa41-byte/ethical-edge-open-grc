from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import List, Dict
from datetime import datetime

router = APIRouter(
    prefix="/gates",
    tags=["Bill Gates Foundation - Philanthropic Integrity"]
)

# 1. DONOR VETTING & FUNDING COMPLIANCE SCHEMAS
class FundingDistributionInput(BaseModel):
    grantee_organization: str
    project_title: str
    total_allocated_usd: float = Field(..., ge=0.0)
    funds_disbursed_usd: float = Field(..., ge=0.0)
    milestones_expected: int = Field(..., gt=0)
    milestones_achieved: int = Field(..., ge=0)
    anti_corruption_screening_passed: bool = Field(..., description="Validates zero conflict of interest or policy breaches")

# 2. OPERATIONAL AUDITING ENDPOINTS
@router.get("/status")
async def get_gates_room_status():
    """
    Returns the technical auditing status of the Gates Foundation Vetting Engine.
    """
    return {
        "room": "Bill Gates Foundation Room",
        "engine_status": "ACTIVE",
        "focus": "Philanthropic Integrity, Resource Accountability & Grant Milestone Vetting",
        "compliance_frameworks": ["Global Anti-Corruption Standards", "Milestone-Based Resource Allocation"],
        "operational_state": "PRODUCTION_READY"
    }

@router.post("/audit-grant")
async def audit_grant_distribution(grant: FundingDistributionInput):
    """
    Evaluates resource distribution integrity and calculates project execution alignment.
    """
    # Enforce a strict programmatic stop if basic anti-corruption vetting fails
    if not grant.anti_corruption_screening_passed:
        raise HTTPException(
            status_code=403, 
            detail="CRITICAL GOVERNANCE FAILURE: Grantee failed anti-corruption screening protocol."
        )

    # Prevent logical data errors (disbursing more than allocated)
    if grant.funds_disbursed_usd > grant.total_allocated_usd:
        raise HTTPException(
            status_code=400,
            detail="FINANCIAL ANOMALY: Disbursed funds cannot exceed total allocated grant value."
        )

    # Compute operational milestone completion rate
    milestone_completion_rate = (grant.milestones_achieved / grant.milestones_expected) * 100.0
    
    # Compute financial deployment rate
    financial_deployment_rate = (grant.funds_disbursed_usd / grant.total_allocated_usd) * 100.0 if grant.total_allocated_usd > 0 else 0.0

    # Calculate Resource Distribution Integrity Rating
    # A massive divergence between disbursed funds and achieved milestones drops the integrity index
    efficiency_variance = financial_deployment_rate - milestone_completion_rate
    
    if efficiency_variance > 30.0:
        # Funds are burning significantly faster than project delivery
        integrity_status = "WARNING - CAPITAL OVER-ALLOCATION / MILESTONE DRIFT"
        audit_risk_tier = "HIGH"
    elif efficiency_variance < -20.0:
        # Grantees are over-performing milestones relative to capital disbursed
        integrity_status = "OPTIMAL EXECUTION - REQUEST ACCELERATED FUND RELEASE"
        audit_risk_tier = "LOW"
    else:
        integrity_status = "NORMAL - STABLE FINANCIAL AND OPERATIONAL ALIGNMENT"
        audit_risk_tier = "MINIMAL"

    return {
        "audit_timestamp": datetime.utcnow(),
        "grantee": grant.grantee_organization,
        "project_tracked": grant.project_title,
        "metrics_analysis": {
            "milestone_completion": f"{round(milestone_completion_rate, 2)}%",
            "financial_burn_rate": f"{round(financial_deployment_rate, 2)}%",
            "capital_efficiency_variance": round(efficiency_variance, 2)
        },
        "governance_assessment": {
            "integrity_index_status": integrity_status,
            "risk_tier": audit_risk_tier,
            "next_scheduled_action": "HOLD_FURTHER_DISBURSEMENT" if audit_risk_tier == "HIGH" else "PROCEED_WITH_TRANCHE"
        }
    }
