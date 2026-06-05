from fastapi import FastAPI, Request, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pathlib import Path
from app.database.session import init_db

# 1. IMPORT ALL OPERATIONAL ROUTERS & SECURITY GATEKEEPERS
from app.auth.routes import router as auth_router
from app.auth.admin_provisioning import router as admin_provisioning_router
from app.auth.billing_webhooks import router as billing_webhook_router  # Automated Billing Ingest
from app.room_core_grc.regtech_rules import router as core_grc_router
from app.room_google.ai_cybersecurity import router as google_challenge_router
from app.room_gates.donor_vetting import router as gates_foundation_router
from app.room_unicef.open_source_risk import router as unicef_challenge_router
from app.room_isoc.connectivity_trust import router as isoc_challenge_router
from app.room_safeguard.epidemic_surveillance import router as safeguard_router
from app.api.endpoints.audit import router as persistent_audit_router

# 2. INITIALIZE THE MASTER APPLICATION INSTANCE
app = FastAPI(
    title="Ethical Edge Cognitive GRC Research Engine",
    description="Unified multi-tenant orchestration engine handling standard RegTech framework compliance and localized action research tracking rooms.",
    version="3.0.0"
)

# Startup Database Tables Programmatically
@app.on_event("startup")
def startup_event():
    init_db()

# 3. CONFIGURE FILE PATHING FOR JINJA2 FRONTEND UI RENDERING
BASE_DIR = Path(__file__).resolve().parent
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

# 4. ENABLE CROSS-ORIGIN RESOURCE SHARING (CORS) FOR REGIONAL PWAs
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 5. MOUNT ALL BACKEND SECURITY AND COMPLIANCE INFRASTRUCTURE ROUTERS
app.include_router(auth_router)
app.include_router(admin_provisioning_router)
app.include_router(billing_webhook_router)  # Mounted to handle real-time payment gateway triggers
app.include_router(core_grc_router)
app.include_router(google_challenge_router)
app.include_router(gates_foundation_router)
app.include_router(unicef_challenge_router)
app.include_router(isoc_challenge_router)
app.include_router(safeguard_router)
app.include_router(persistent_audit_router)

# 6. SYSTEM STATUS ORCHESTRATION HEALTH ENDPOINT
@app.get("/")
async def get_master_system_status():
    """
    Master root health check demonstrating full multi-room infrastructure visibility.
    """
    return {
        "organization": "Ethical Edge GRC Consulting (Pty) Ltd",
        "system": "Cognitive GRC Orchestrator Engine",
        "status": "ONLINE & FULLY INTEGRATED",
        "total_active_rooms": 6,
        "active_tenants": [
            "Normal GRC - RegTech Core",
            "Google AI Cybersecurity Challenge",
            "Bill Gates Foundation Integrity Suite",
            "UNICEF Frontier Tech Engine",
            "Internet Society Trust Network",
            "Project SAFEGUARD State Dept Center"
        ]
    }

# 7. WEB FRONTEND USER INTERFACE VISUAL DASHBOARD
@app.get("/view/dashboard", response_class=HTMLResponse)
async def serve_visual_dashboard(request: Request):
    """
    Renders the live responsive GRC monitoring command console, injection mapping
    multi-tenant feature parameters straight to structural Tailwind HTML elements.
    """
    context_payload = {
        "request": request,
        "user_identity": "Boitshwarelo Motlogelwa",
        "tenant_id": "EE_TENANT_ETHICAL_EDGE_CORPORATE",
        "tier": "ENTERPRISE",
        "can_access_nist_cyber": True,
        "can_access_safeguard": True
    }
    return templates.TemplateResponse("dashboard.html", context_payload)

from fastapi import FastAPI
from app.database.session import SessionLocal
from app.database.models import AuditRun

app = FastAPI()

@app.get("/api/room/{room_key}")
async def get_room_data(room_key: str):
    db = SessionLocal()
    try:
        # Fetch the latest run for this room (tenant)
        latest_run = db.query(AuditRun).filter(AuditRun.tenant_id == room_key.upper()).order_by(AuditRun.timestamp.desc()).first()
        
        if not latest_run:
            return {"data": {"governing_functions": [], "status": "No data found"}}
            
        return {
            "data": {
                "governing_functions": ["Principle 1", "Principle 2"], # Update this to pull from your findings
                "status": "Success",
                "attainment_rate": latest_run.attainment_rate
            }
        }
    finally:
        db.close()

from fastapi import FastAPI
from app.database.session import SessionLocal
from app.database.models import AuditRun

app = FastAPI()

# This endpoint matches the fetch() call in your dashboard.html
@app.get("/api/room/{room_key}")
async def get_room_data(room_key: str):
    db = SessionLocal()
    try:
        # We search the database for the tenant (room_key)
        # Using .upper() to match potential casing issues
        run = db.query(AuditRun).filter(AuditRun.tenant_id == room_key.upper()).first()
        
        if not run:
            return {"data": {"governing_functions": ["No data available"], "status": "Empty"}}
            
        return {
            "data": {
                "governing_functions": ["Principle 1", "Principle 2"], 
                "status": "Success",
                "attainment_rate": run.attainment_rate
            }
        }
    finally:
        db.close()

def main():
    # In a real scenario, you might pull this from an environment variable 
    # or a list of active tenants in your database.
    target_tenant_id = os.getenv("TARGET_TENANT_ID") 
    
    if not target_tenant_id:
        print("❌ Error: TARGET_TENANT_ID not set.")
        return

    db_generator = get_db_session()
    session = next(db_generator)
    
    try:
        raw_framework = load_framework_source(CHECKLIST_PATH)
        # Pass the tenant_id from the environment/config
        ingest_king_v_framework(raw_framework, session, target_tenant_id)
    except Exception as e:
        session.rollback()
        print(f"❌ Critical Production Pipeline Failure: {str(e)}")
    finally:
        session.close()

import asyncio
from fastapi import FastAPI, Depends, Header
from sqlalchemy.orm import Session
from app.database.connection import get_db
from app.middleware.tier_guard import verify_account_tier, TenantProfile
from app.room_manager import get_room_data_async

app = FastAPI(title="Ethical Edge GRC Platform")

@app.get("/dashboard/summary")
async def get_dashboard_summary(
    db: Session = Depends(get_db),
    tenant: TenantProfile = Depends(verify_account_tier)
):
    """
    Asynchronously aggregates all room data.
    One slow room will not block the others.
    """
    # List of all rooms available in your ecosystem
    rooms_to_query = ["core", "gate", "gougle", "isoc", "safeguard", "unicef"]
    
    # Create a list of coroutines (tasks)
    tasks = [
        get_room_data_async(room_key, "admin", db, tenant.token)
        for room_key in rooms_to_query
    ]
    
    # Execute all rooms concurrently
    # This is where the magic happens: the platform fetches all 6 rooms at once!
    results = await asyncio.gather(*tasks, return_exceptions=True)
    
    # Map results to room names for the frontend
    dashboard = {room: result for room, result in zip(rooms_to_query, results)}
    
    return {"tenant": tenant.name, "dashboard": dashboard}
