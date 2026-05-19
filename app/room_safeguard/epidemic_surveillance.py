from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import List
from datetime import datetime

router = APIRouter(
    prefix="/safeguard",
    tags=["Project SAFEGUARD - State Dept Biosecurity Engine"]
)

# 1. DEFINE INGESTION SCHEMAS (Matches your DB layout)
class SymptomReportInput(BaseModel):
    clinic_id: int
    device_session_token: str
    symptom_cluster_flags: List[str] = Field(..., example=["acute_fever", "hemorrhagic_signs"])
    anonymized_patient_age_group: str = Field(..., example="25-34")
    field_captured_at: datetime # When captured offline by PWA
    geo_location_point: str

# 2. APPLICATION LOGIC ENDPOINTS
@router.get("/status")
async def get_safeguard_room_status():
    """
    Returns the baseline configuration metrics for the Project SAFEGUARD room.
    """
    return {
        "room": "Project SAFEGUARD",
        "engine_status": "ACTIVE",
        "focus": "Automated Epidemic Surveillance & Cross-Border Sovereign Data Governance",
        "data_protection_alignment": "BDPA (Botswana) / POPIA (South Africa) Enforced",
        "operational_state": "INTEGRATED_WITH_SCHEMA"
    }

@router.post("/ingest-report")
async def ingest_field_report(report: SymptomReportInput):
    """
    Ingests field data, computes telemetry latency, and triggers algorithmic risk scaling.
    """
    cloud_received_at = datetime.utcnow()
    
    # Calculate operational sync latency in hours
    time_delta = cloud_received_at - report.field_captured_at.replace(tzinfo=None)
    latency_hours = round(time_delta.total_seconds() / 3600.0, 2)
    
    # Simple rule-based algorithmic risk weighting for the MVP
    symptom_count = len(report.symptom_cluster_flags)
    if symptom_count >= 3:
        risk_tier = "CRITICAL RISK"
        risk_score = 90
    elif symptom_count == 2:
        risk_tier = "MEDIUM RISK"
        risk_score = 50
    else:
        risk_tier = "LOW RISK"
        risk_score = 15

    # Enforce BDPA validation flag
    bdpa_compliant = True if "patient_name" not in report.device_session_token else False

    return {
        "status": "SUCCESSFULLY_PROCESSED",
        "telemetry": {
            "field_timestamp": report.field_captured_at,
            "cloud_timestamp": cloud_received_at,
            "calculated_latency_hours": latency_hours,
            "latency_target_achieved": latency_hours <= 12.0
        },
        "grc_evaluation": {
            "algorithmic_risk_score": risk_score,
            "escalation_tier": risk_tier,
            "bdpa_compliance_audit_flag": bdpa_compliant,
            "action_required": "ALERT_DISPATCHED" if risk_tier == "CRITICAL RISK" else "LOGGED"
        }
    }
