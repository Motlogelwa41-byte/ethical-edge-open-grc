from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Import the 6 operational rooms we built together
from app.room_core_grc.regtech_rules import router as core_grc_router
from app.room_google.ai_cybersecurity import router as google_challenge_router
from app.room_gates.donor_vetting import router as gates_foundation_router
from app.room_unicef.open_source_risk import router as unicef_challenge_router
from app.room_isoc.connectivity_trust import router as isoc_challenge_router
from app.auth.routes import router as auth_router
from app.room_safeguard.epidemic_surveillance import router as safeguard_router

# Initialize the Master FastAPI Application Engine
app = FastAPI(
    title="Ethical Edge Open GRC Engine",
    description="Unified Cognitive GRC Backend Orchestrator handling standard RegTech and global compliance challenge rooms.",
    version="3.0.0"
)

# Enable CORS for cross-platform Progressive Web Apps (PWAs) and dashboards
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount all 6 rooms to the master server instance
app.include_router(core_grc_router)
app.include_router(google_challenge_router)
app.include_router(gates_foundation_router)
app.include_router(unicef_challenge_router)
app.include_router(isoc_challenge_router)
app.include_router(safeguard_router)

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
