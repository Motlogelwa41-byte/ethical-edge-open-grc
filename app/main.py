"""
Ethical Edge Cognitive GRC Research Engine
File: main.py

Objective:
Unified master orchestration backend incorporating:
- Child safeguarding
- Climate risk intelligence
- Core GRC compliance modules
- UNICEF Climate Demo capability
"""

from typing import Dict, Any

from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from app.middleware.tier_guard import verify_account_tier, TenantProfile

# Database
from app.database.session import init_db

# Core Routers
from app.auth.routes import router as auth_router
from app.room_core_grc.regtech_rules import router as core_grc_router

# UNICEF Climate Demo Routers
from app.api.endpoints import climate_dashboard, climate_demo, cvi

# Climate Intelligence Engine
from climate_risk_manager import (
    sanitize_environmental_payload,
    ClimateRiskManager,
    ClimateTelemetryInput,
    ResilienceParameters
)

from run_compliance_checks import GRCComplianceEngine


# ============================================================
# 1. APPLICATION INITIALIZATION
# ============================================================

app = FastAPI(
    title="Ethical Edge Cognitive GRC Research Engine",
    description=(
        "AI-powered governance, risk and compliance engine "
        "with integrated UNICEF Climate Resilience Decision Support."
    ),
    version="3.0.0"
)


compliance_auditor = GRCComplianceEngine()


# ============================================================
# 2. STARTUP & MIDDLEWARE
# ============================================================

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


# ============================================================
# 3. ROUTER REGISTRATION
# ============================================================

app.include_router(auth_router)

app.include_router(core_grc_router)

app.include_router(
    climate_dashboard.router,
    tags=["Climate Dashboard"]
)

app.include_router(
    climate_demo.router
)

app.include_router(
    cvi.router
)


# ============================================================
# 4. UNICEF CLIMATE DATA INTAKE PIPELINE
# ============================================================

@app.post(
    "/api/v1/climate/intake",
    tags=["Cognitive Climate Core"]
)
async def receive_climate_data(
    raw_payload: Dict[Any, Any]
):

    try:

        clean_data = sanitize_environmental_payload(
            raw_payload
        )


        telemetry_contract = ClimateTelemetryInput(

            facility_id=clean_data["telemetry_id"],

            facility_type=raw_payload.get(
                "facility_type",
                "school"
            ),

            temperature_celsius=clean_data[
                "environmental_metrics"
            ]["heat_index_celsius"],

            flood_water_level_meters=raw_payload.get(
                "flood_water_level_meters",
                0.0
            ),

            drought_index_spi=raw_payload.get(
                "drought_index_spi",
                0.0
            ),

            active_power_outage=raw_payload.get(
                "active_power_outage",
                False
            )
        )


        infrastructure_contract = ResilienceParameters(

            student_or_patient_count=raw_payload.get(
                "student_or_patient_count",
                0
            ),

            has_active_cooling=raw_payload.get(
                "has_active_cooling",
                False
            ),

            has_clean_water_reserve=raw_payload.get(
                "has_clean_water_reserve",
                True
            ),

            has_offgrid_power_backup=raw_payload.get(
                "has_offgrid_power_backup",
                False
            )
        )


        assessment_result = (
            ClimateRiskManager
            .evaluate_facility_governance_score(
                telemetry=telemetry_contract,
                infrastructure=infrastructure_contract
            )
        )


        final_audit_ledger = (
            compliance_auditor
            .evaluate_facility_telemetry_compliance(
                assessment_result
            )
        )


        return {

            "status": "success",

            "anonymized_telemetry_id":
                clean_data["telemetry_id"],

            "audit_ledger_output":
                final_audit_ledger
        }


    except Exception as e:

        raise HTTPException(
            status_code=400,
            detail=(
                "Cognitive climate engine "
                f"orchestration failed: {str(e)}"
            )
        )


# ============================================================
# 5. DASHBOARD SUMMARY
# ============================================================

@app.get("/dashboard/summary")
async def get_dashboard_summary(
    tenant: TenantProfile = Depends(
        verify_account_tier
    )
):

    return {

        "tenant": tenant.name,

        "dashboard": {

            "status":
                "Dashboard aggregator online",

            "modules": [

                "core",

                "climate",

                "unicef"

            ]

        }
    }



# ============================================================
# 6. HEALTH CHECK
# ============================================================

@app.get("/")
async def root():

    return {

        "status":
            "Ethical Edge Engine ONLINE"

    }
