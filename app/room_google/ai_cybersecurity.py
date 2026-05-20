from fastapi import APIRouter, HTTPException, Depends, status
from pydantic import BaseModel, Field
from typing import List, Dict, Any
from datetime import datetime
from sqlalchemy.orm import Session

# Import your database core layers and models
from app.database import get_db
from app.room_google.models import AICyberThreatLog
from app.auth.security import strip_pii_for_bdpa_compliance

router = APIRouter(
    prefix="/google",
    tags=["Google Challenge - AI Cybersecurity"]
)

# 1. CYBERSECURITY LOG AND COMPLIANCE INPUT SCHEMAS
class PerimeterThreatLogInput(BaseModel):
    source_ip: str = Field(..., example="192.0.2.1")
    target_cloud_service: str = Field(..., example="Cloud_SQL_Instance")
    failed_login_attempts: int = Field(..., ge=0, example=3)
    unauthorized_api_calls: int = Field(..., ge=0, example=1)
    payload_anomaly_detected: bool = Field(..., description="Flags unexpected vectors targeting AI models")

class SaifComplianceInput(BaseModel):
    organization_id: str = Field(..., example="ORG_SADC_FINTECH_09x")
    infrastructure_sanitization_verified: bool = Field(..., description="SAIF Element: Expand strong security foundations")
    model_input_filtering_active: bool = Field(..., description="SAIF Element: Extend protections to AI deployment")
    automated_drift_detection_enabled: bool = Field(..., description="SAIF Element: Continuous monitoring and evaluation")

# 2. APPLICATION STATUS ENDPOINT
@router.get("/status")
async def get_google_room_status():
    """
    Returns the real-time processing status of the Google Challenge AI module.
    """
    return {
        "room": "Google Challenge",
        "engine_status": "ACTIVE",
        "focus": "AI Anomaly Detection & Cloud Perimeter Threat Intelligence",
        "compliance_frameworks": ["NIST CSF 2.0", "Google Secure AI Framework (SAIF)"],
        "operational_state": "PRODUCTION_READY"
    }

# 3. DATABASE-INTEGRATED THREAT ANALYSIS COMPONENT
@router.post("/analyze-threat", status_code=status.HTTP_201_CREATED)
async def analyze_perimeter_threat(log: PerimeterThreatLogInput, db: Session = Depends(get_db)):
    """
    Evaluates cloud perimeter metrics to determine active threat severity levels,
    scrubs PII network footprints for BDPA, and saves the threat metrics to PostgreSQL.
    """
    # Calculate a composite threat weight matching your equation
    threat_score = (log.failed_login_attempts * 2) + (log.unauthorized_api_calls * 5)
    if log.payload_anomaly_detected:
        threat_score += 25  # Heavy weight for potential adversarial injection attempts

    # Map the score to NIST CSF 2.0 Respond (RS) category behaviors
    if threat_score >= 30:
        severity_tier = "CRITICAL - IMMEDIATE REVOCATION & SOC ESCALATION"
        nist_action_mapping = "RS.MA-01 (Incident Response Management Triggered)"
        nist_rating = "CRITICAL"
    elif threat_score >= 10:
        severity_tier = "MEDIUM - RATE LIMIT & ISOLATE IP"
        nist_action_mapping = "PR.IR-02 (Protective Technology Restraints)"
        nist_rating = "MEDIUM"
    else:
        severity_tier = "LOW - ROUTINE SEC_OPS RECORDING"
        nist_action_mapping = "DE.CM-01 (Continuous Security Monitoring)"
        nist_rating = "LOW"

    # Enforce zero-PII storage: strip IP addresses before logging to Postgres to protect location telemetry under BDPA
    sanitized_metadata = strip_pii_for_bdpa_compliance({
        "raw_source_ip": log.source_ip,
        "failed_logins": log.failed_login_attempts,
        "unauthorized_calls": log.unauthorized_api_calls,
        "payload_anomaly": log.payload_anomaly_detected,
        "recommended_framework_action": nist_action_mapping
    })

    # Instantiate the database row mapping
    threat_record = AICyberThreatLog(
        target_endpoint=log.target_cloud_service,
        detected_anomaly_type="AI_ADVERSARIAL_INJECTION" if log.payload_anomaly_detected else "PERIMETER_ANOMALY",
        ai_confidence_score=round(min(threat_score / 50.0, 1.0), 4), # Generates a normalized score weight vector
        nist_impact_rating=nist_rating,
        model_inference_payload=sanitized_metadata
    )

    # Commit record row to PostgreSQL instance
    db.add(threat_record)
    db.commit()
    db.refresh(threat_record)

    return {
        "log_id": str(threat_record.id),
        "analysis_timestamp": threat_record.logged_at,
        "source_vector": "[REDACTED_BY_BDPA_EDGE_PRIVACY_SHIELD]",
        "threat_telemetry": {
            "calculated_threat_score": threat_score,
            "severity_tier": severity_tier
        },
        "nist_csf_alignment": {
            "recommended_framework_action": nist_action_mapping,
            "status": "LOGGED_FOR_AUDIT"
        },
        "database_sync": "RECORD_COMMITTED"
    }

# 4. GOOGLE SAIF POSTURE COMPLIANCE ENDPOINT
@router.post("/audit-saif")
async def audit_google_saif_posture(audit: SaifComplianceInput):
    """
    Validates model ecosystem alignment against Google's Secure AI Framework core pillars.
    """
    saif_matrix = {
        "Foundational_Infrastructure_Security": audit.infrastructure_sanitization_verified,
        "AI_Boundary_Input_Filtering": audit.model_input_filtering_active,
        "Continuous_Behavioral_Drift_Monitoring": audit.automated_drift_detection_enabled
    }

    passed_pillars = sum(1 for status in saif_matrix.values() if status is True)
    compliance_score = (passed_pillars / 3.0) * 100.0

    return {
        "organization_id": audit.organization_id,
        "saif_audit_results": {
            "pillars_evaluated": 3,
            "pillars_passed": passed_pillars,
            "overall_saif_score": f"{round(compliance_score, 2)}%"
        },
        "posture_breakdown": saif_matrix,
        "deployment_safety_clearance": "APPROVED_FOR_AI_PRODUCTION" if compliance_score == 100.0 else "REJECTED_GOVERNANCE_HOLD"
    }
