"""
Ethical Edge Cognitive GRC Research Engine
File: main.py
Objective: Unified master multi-tenant orchestration backend incorporating 
           child safeguarding, climate triage, and core compliance modules.
"""

import os
import asyncio
from pathlib import Path
from typing import Dict, Any
from fastapi import FastAPI, Request, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

# Database & Core Infrastructure
from app.database.connection import get_db
from app.database.session import init_db
from app.middleware.tier_guard import verify_account_tier, TenantProfile
from app.room_manager import get_room_data_async

# Standard Routers
from app.auth.routes import router as auth_router
from app.room_core_grc.regtech_rules import router as core_grc_router
from app.api.endpoints import questionnaire, certiguard_ai, climate_dashboard

# Cognitive Climate Core Infrastructure Components
from climate_risk_manager import sanitize_environmental_payload, ClimateRiskManager, ClimateTelemetryInput, ResilienceParameters
from run_compliance_checks import GRCComplianceEngine

# =====================================================================
# 1. INITIALIZE MASTER APPLICATION ENGINE
# =====================================================================
app = FastAPI(
    title="Ethical Edge Cognitive GRC Research Engine",
    description="Unified multi-tenant orchestration engine with integrated Child Safeguarding and Climate Risk Core.",
    version="3.0.0"
)

# Instantiate the custom rules auditor factory
compliance_auditor = GRCComplianceEngine()

# =====================================================================
# 2. MIDDLEWARE & LIFECYCLE MANAGEMENT
# =====================================================================
@app.on_event("startup")
def startup_event():
    init_db()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =====================================================================
# 3. MOUNT CORE ARCHITECTURE ROUTERS
# =====================================================================
app.include_router(auth_router)
app.include_router(core_grc_router)
app.include_router(questionnaire.router)
app.include_router(certiguard_ai.router)

# =====================================================================
# 4. COGNITIVE CLIMATE INTAKE PIPELINE (UNICEF SPEC)
# =====================================================================
@app.post("/api/v1/climate/intake", tags=["Cognitive Climate Core"])
async def receive_climate_data(raw_payload: Dict[Any, Any]):
    """
    Ingests raw environmental telemetry, enforces immediate Privacy-by-Design spatial scrubbing, 
    calculates dynamic child-centric vulnerability scores, and evaluates structural framework compliance.
    """
    try:
        # 1. Apply absolute privacy filters on raw input coordinates and structural identifiers
        clean_data = sanitize_environmental_payload(raw_payload)
        
        # 2. Extract configuration conditions into structured Pydantic schemas
        telemetry_contract = ClimateTelemetryInput(
            facility_id=clean_data["telemetry_id"],
            facility_type=raw_payload.get("facility_type", "school"),
            temperature_celsius=clean_data["environmental_metrics"]["heat_index_celsius"],
            flood_water_level_meters=raw_payload.get("flood_water_level_meters", 0.0),
            drought_index_spi=raw_payload.get("drought_index_spi", 0.0),
            active_power_outage=raw_payload.get("active_power_outage", False)
        )
        
        infra_contract = ResilienceParameters(
            student_or_patient_count=raw_payload.get("student_or_patient_count", 0),
            has_active_cooling=raw_payload.get("has_active_cooling", False),
            has_clean_water_reserve=raw_payload.get("has_clean_water_reserve", True),
            has_offgrid_power_backup=raw_payload.get("has_offgrid_power_backup", False)
        )
        
        # 3. Compute dynamic threat severity coefficients
        assessment_result = ClimateRiskManager.evaluate_facility_governance_score(
            telemetry=telemetry_contract, 
            infrastructure=infra_contract
        )
        
        # 4. Execute programmatic matching audit ledger routines
        final_audit_ledger = compliance_auditor.evaluate_facility_telemetry_compliance(assessment_result)
        
        return {
            "status": "success",
            "anonymized_telemetry_id": clean_data["telemetry_id"],
            "audit_ledger_output": final_audit_ledger
        }
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Cognitive climate engine orchestration failed: {str(e)}")

# =====================================================================
# 5. DASHBOARD SUMMARY AGGREGATOR
# =====================================================================
@app.get("/dashboard/summary")
async def get_dashboard_summary(
    db: Session = Depends(get_db),
    tenant: TenantProfile = Depends(verify_account_tier)
):
    """
    Asynchronously aggregates all system data layers for the authenticated tenant context.
    """
    rooms_to_query = ["core", "gate", "gougle", "isoc", "safeguard", "unicef"]
    
    tasks = [
        get_room_data_async(room_key, "admin", db, tenant.token)
        for room_key in rooms_to_query
    ]
    
    results = await asyncio.gather(*tasks, return_exceptions=True)
    
    return {
        "tenant": tenant.name, 
        "dashboard": {room: result for room, result in zip(rooms_to_query, results)}
    }

# =====================================================================
# 6. ROOT MONITORING HEALTH CHECK
# =====================================================================
@app.get("/")
async def root():
    return {"status": "Ethical Edge Engine ONLINE"}
