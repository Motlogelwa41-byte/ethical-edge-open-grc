from fastapi import APIRouter

router = APIRouter(
    prefix="/isoc",
    tags=["ISOC Challenge - Connectivity & Trust Infrastructure"]
)

@router.get("/status")
async def get_isoc_room_status():
    """
    Returns the routing status of the Internet Society Infrastructure Trust engine.
    """
    return {
        "room": "Internet Society (ISOC) Challenge",
        "engine_status": "ACTIVE",
        "focus": "Community Networks & Encrypted Trust Auditing",
        "target_framework": "ISOC Mutually Assured Norms for Routing Security (MANRS)",
        "operational_state": "PREPPED"
    }
