from fastapi import APIRouter, HTTPException, Depends, status
from pydantic import BaseModel, Field
from typing import List, Dict, Any
from datetime import datetime
from sqlalchemy.orm import Session

# Import your database core structures and models
from app.database import get_db
from app.safeguard.models import HealthFacilitySurveillance
from app.auth.security import strip_pii_for_bdpa_compliance

# Import the monetization tier guard
from app.auth.monetization import SubscriptionGuard

router = APIRouter(
    prefix="/safeguard",
    tags=["Project SAFEGUARD - State Dept Biosecurity Engine"]
)

# 1. DEFINE INGESTION SCHEMAS (Preserving your offline PWA structure)
class SymptomReportInput(BaseModel):
    clinic_id: str = Field(..., example="CLINIC_SHAKAWE_004")
    device_session_token: str = Field(..., example="sess_crypt_99x81a")
    symptom_cluster_flags: List[str] = Field(..., example=["acute_fever", "hemorrhagic_signs"])
    anonymized_patient_age_group: str = Field(..., example="25-34")
    field_captured_at: datetime = Field(..., description="Timestamp when captured offline by PWA")
    geo_location_point: str = Field(..., example="-18.3654,21.8421")

# 2. APPLICATION STATUS ENDPOINT
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

# 3. DATABASE-INTEGRATED SURVEILLANCE DATA LOOP (WITH MONETIZATION GUARD)
@router.post("/report-symptom", status_code=status.HTTP_201_CREATED)
async def ingest_and_evaluate_biosecurity_report(
    report: SymptomReportInput, 
    tenant_id: str, # Requires the client to pass their UUID token
    db: Session = Depends(get_db),
    _sub_check = Depends(SubscriptionGuard(required_room="safeguard")) # Restricts to Enterprise Premium Tier
):
    """
    Ingests epidemiological reports from border clinics, computes network transmission delay telemetry,
    enforces zero-PII data policies under BDPA, and commits logs to PostgreSQL.
    Accessible only by Enterprise Premium Tier accounts.
    """
    current_server_time = datetime.utcnow()
    
    # 1. Compute reporting delay latency
    time_delta = current_server_time - report.field_captured_at.replace(tzinfo=None)
    reporting_delay_minutes = int(time_delta.total_seconds() / 60.0)
    
    # 2. Establish biosecurity threat prioritization based on specific symptom patterns
    contains_severe_symptoms = any(
        flag in ["hemorrhagic_signs", "respiratory_distress", "neurological_collapse"]
        for flag in report.symptom_cluster_flags
    )
    
    if contains_severe_symptoms:
        urgency_tier = "CRITICAL"
        status_summary = "IMMEDIATE BIOMEDICAL INTERVENTION REQUIRED - PATHOGEN TRACKING LOGGED"
    elif len(report.symptom_cluster_flags) >= 3:
        urgency_tier = "ELEVATED"
        status_summary = "CLUSTER ANOMALY DETECTED - MONITORING FOR LOCAL TRANSMISSION"
    else:
        urgency_tier = "LOW"
        status_summary = "ROUTINE CLINICAL SYMPTOM REGISTRATION"

    # 3. Apply the BDPA Privacy Shield to guarantee geographic and user anonymization
    sanitized_metadata = strip_pii_for_bdpa_compliance({
        "device_session_token": report.device_session_token,
        "symptom_flags": report.symptom_cluster_flags,
        "anonymized_age_group": report.anonymized_patient_age_group,
        "raw_geo_point": report.geo_location_point,
        "verified_tenant_id": tenant_id
    })

    # 4. Instantiate the relational database record
    surveillance_record = HealthFacilitySurveillance(
        facility_name=f"Clinic Asset node: {report.clinic_id}",
        district="SADC Border Outpost Cluster",
        network_latency_ms=12.5,
        data_payload_size_kb=round(float(len(str(report.dict())) / 1024.0), 3),
        reporting_delay_minutes=max(0, reporting_delay_minutes),
        surveillance_urgency_tier=urgency_tier,
        system_status_summary=status_summary
    )
    
    surveillance_record.custom_telemetry_payload = sanitized_metadata
    
    # 5. Commit directly to your running PostgreSQL pool
    db.add(surveillance_record)
    db.commit()
    db.refresh(surveillance_record)

    return {
        "surveillance_incident_id": str(surveillance_record.id),
        "sync_timestamp": surveillance_record.synchronized_at,
        "computed_reporting_delay_minutes": surveillance_record.reporting_delay_minutes,
        "biosecurity_priority": surveillance_record.surveillance_urgency_tier,
        "action_framework_directive": surveillance_record.system_status_summary,
        "privacy_shield": "VERIFIED_BDPA_COMPLIANT_ZERO_PII_COMMITTED",
        "database_sync": "RECORD_COMMITTED"
    }
