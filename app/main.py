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
