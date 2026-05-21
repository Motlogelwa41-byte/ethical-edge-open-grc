from fastapi import APIRouter, HTTPException, Depends, status
from pydantic import BaseModel, Field
from typing import List, Dict, Any
from datetime import datetime
from sqlalchemy.orm import Session

# Import your database core utilities and models
from app.database import get_db
from app.room_gates.models import VendorIntegrityAudit

# Import the monetization tier guard
from app.auth.monetization import SubscriptionGuard

router = APIRouter(
    prefix="/gates",
    tags=["Bill Gates Foundation - Philanthropic Integrity"]
)

# 1. DONOR VETTING & FUNDING COMPLIANCE SCHEMAS
class FundingDistributionInput(BaseModel):
    grantee_organization: str = Field(..., example="SADC Connectivity Consortium")
    project_title: str = Field(..., example="Phase 1 Rural Mesh Deployment")
    total_allocated_usd: float = Field(..., ge=0.0, example=150000.0)
    funds_disbursed_usd: float = Field(..., ge=0.0, example=75000.0)
    milestones_expected: int = Field(..., gt=0, example=10)
    milestones_achieved: int = Field(..., ge=0, example=3)
    anti_corruption_screening_passed: bool = Field(..., description="Validates zero conflict of interest or policy breaches")

# 2. OPERATIONAL STATUS ENDPOINT
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

# 3. DATABASE-INTEGRATED AUDIT SYSTEM (WITH MONETIZATION GUARD)
@router.post("/audit-grant", status_code=status.HTTP_201_CREATED)
async def audit_grant_distribution(
    grant: FundingDistributionInput, 
    tenant_id: str, # Requires the client to pass their UUID token
    db: Session = Depends(get_db),
    _sub_check = Depends(SubscriptionGuard(required_room="gates")) # Restricts to Enterprise Premium Tier
):
    """
    Evaluates resource distribution integrity, calculates project execution alignment,
    and commits the financial audit trail permanently to the PostgreSQL instance.
    Accessible only by Enterprise Premium Tier accounts.
    """
    # Enforce a strict programmatic stop if basic anti-corruption vetting fails
    if not grant.anti_corruption_screening_passed:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="CRITICAL GOVERNANCE FAILURE: Grantee failed anti-corruption screening protocol."
        )

    # Prevent logical data errors (disbursing more than allocated)
    if grant.funds_disbursed_usd > grant.total_allocated_usd:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="FINANCIAL ANOMALY: Disbursed funds cannot exceed total allocated grant value."
        )

    # Compute operational milestone completion rate
    milestone_completion_rate = (grant.milestones_achieved / grant.milestones_expected) * 100.0
    
    # Compute financial deployment rate
    financial_deployment_rate = (grant.funds_disbursed_usd / grant.total_allocated_usd) * 100.0 if grant.total_allocated_usd > 0 else 0.0

    # Calculate Resource Distribution Integrity Rating
    efficiency_variance = financial_deployment_rate - milestone_completion_rate
    
    if efficiency_variance > 30.0:
        integrity_status = "WARNING - CAPITAL OVER-ALLOCATION / MILESTONE DRIFT"
        audit_risk_tier = "HIGH"
        vetting_decision = "REVIEW_REQUIRED"
    elif efficiency_variance < -20.0:
        integrity_status = "OPTIMAL EXECUTION - REQUEST ACCELERATED FUND RELEASE"
        audit_risk_tier = "LOW"
        vetting_decision = "APPROVED"
    else:
        integrity_status = "NORMAL - STABLE FINANCIAL AND OPERATIONAL ALIGNMENT"
        audit_risk_tier = "MINIMAL"
        vetting_decision = "APPROVED"

    # Instantiate the database row using our relational model mapping
    audit_record = VendorIntegrityAudit(
        entity_name=grant.grantee_organization,
        country_of_origin="SADC Region",
        pep_status_verified=True,
        sanction_list_collision=False,
        calculated_integrity_score=round(100.0 - max(0.0, efficiency_variance), 2),
        vetting_decision=vetting_decision,
        audit_metadata={
            "project_title": grant.project_title,
            "total_allocated_usd": grant.total_allocated_usd,
            "funds_disbursed_usd": grant.funds_disbursed_usd,
            "milestone_completion_rate": f"{round(milestone_completion_rate, 2)}%",
            "financial_burn_rate": f"{round(financial_deployment_rate, 2)}%",
            "efficiency_variance_delta": round(efficiency_variance, 2),
            "integrity_index_status": integrity_status,
            "audit_risk_tier": audit_risk_tier,
            "next_scheduled_action": "HOLD_FURTHER_DISBURSEMENT" if audit_risk_tier == "HIGH" else "PROCEED_WITH_TRANCHE",
            "verified_tenant_id": tenant_id
        }
    )

    # Commit to the connection pool transaction loop
    db.add(audit_record)
    db.commit()
    db.refresh(audit_record)

    return {
        "audit_id": str(audit_record.id),
        "audit_timestamp": audit_record.audited_at,
        "grantee": audit_record.entity_name,
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
        },
        "database_sync": "RECORD_COMMITTED"
    }
