from fastapi import FastAPI, HTTPException, Depends
from typing import Dict, Any
# Import your new modules
from climate_risk_manager import sanitize_environmental_payload, ClimateRiskManager, ClimateTelemetryInput, ResilienceParameters

app = FastAPI(title="Ethical Edge Cognitive GRC Engine")

@app.post("/api/v1/climate/intake", tags=["Cognitive Climate Core"])
async def receive_climate_data(raw_payload: Dict[Any, Any]):
    """
    Ingests raw environmental telemetry, strips identifying markers automatically 
    via the privacy pipeline, runs a GRC vulnerability assessment, and logs results.
    """
    try:
        # 1. Enforce Privacy-by-Design on raw data strings immediately
        clean_data = sanitize_environmental_payload(raw_payload)
        
        # 2. Extract configuration contexts into validation contracts
        telemetry_contract = ClimateTelemetryInput(
            facility_id=clean_data["telemetry_id"],
            facility_type=raw_payload.get("facility_type", "school"),
            temperature_celsius=clean_data["environmental_metrics"]["heat_index_celsius"],
            flood_water_level_meters=clean_data["environmental_metrics"]["pm25_concentration"], # cross-mapped parameters
            drought_index_spi=raw_payload.get("drought_index_spi", 0.0),
            active_power_outage=raw_payload.get("active_power_outage", False)
        )
        
        infra_contract = ResilienceParameters(
            student_or_patient_count=raw_payload.get("student_or_patient_count", 0),
            has_active_cooling=raw_payload.get("has_active_cooling", False),
            has_clean_water_reserve=raw_payload.get("has_clean_water_reserve", True),
            has_offgrid_power_backup=raw_payload.get("has_offgrid_power_backup", False)
        )
        
        # 3. Process GRC evaluation calculations 
        assessment_result = ClimateRiskManager.evaluate_facility_governance_score(
            telemetry=telemetry_contract, 
            infrastructure=infra_contract
        )
        
        return {"status": "success", "assessment": assessment_result}
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Data pipeline orchestration failed: {str(e)}")

import os
import asyncio
from pathlib import Path
from fastapi import FastAPI, Request, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

# Database & Infrastructure
from app.database.connection import get_db
from app.database.session import init_db
from app.middleware.tier_guard import verify_account_tier, TenantProfile
from app.room_manager import get_room_data_async

# Routers
from app.auth.routes import router as auth_router
from app.room_core_grc.regtech_rules import router as core_grc_router
# ... (Import all your other room routers here)

# 1. INITIALIZE MASTER ENGINE
app = FastAPI(
    title="Ethical Edge Cognitive GRC Research Engine",
    description="Unified multi-tenant orchestration engine.",
    version="3.0.0"
)

# 2. LIFECYCLE MANAGEMENT
@app.on_event("startup")
def startup_event():
    init_db()

# 3. MIDDLEWARE
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 4. MOUNT ROUTERS
app.include_router(auth_router)
app.include_router(core_grc_router)

# 5. DASHBOARD ORCHESTRATOR (The "Magic" Endpoint)
@app.get("/dashboard/summary")
async def get_dashboard_summary(
    db: Session = Depends(get_db),
    tenant: TenantProfile = Depends(verify_account_tier)
):
    """
    Asynchronously aggregates all room data for the authenticated tenant.
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

# 6. ROOT HEALTH CHECK
@app.get("/")
async def root():
    return {"status": "Ethical Edge Engine ONLINE"}

from app.api.endpoints import questionnaire

app.include_router(questionnaire.router)

from app.api.endpoints import certiguard_ai
app.include_router(certiguard_ai.router)

@app.post("/api/v1/climate/intake")
async def receive_climate_data(raw_data: dict):
    # 1. Enforce privacy controls at entry point
    clean_payload = sanitize_environmental_payload(raw_data)
    
    # 2. Proceed with GRC evaluation risk scoring
    # ...
