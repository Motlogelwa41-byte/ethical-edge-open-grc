from fastapi import APIRouter

router = APIRouter(
    prefix="/unicef",
    tags=["UNICEF Challenge - Open-Source Risk Engine"]
)

@router.get("/status")
async def get_unicef_room_status():
    """
    Returns the tracking status of the UNICEF Open-Source Climate & Risk Engine.
    """
    return {
        "room": "UNICEF Frontier Tech Challenge",
        "engine_status": "ACTIVE",
        "focus": "Open-Source Infrastructure & Child-Centric Climate GRC",
        "target_framework": "UNICEF Venture Fund Open-Source Standards",
        "operational_state": "PREPPED"
    }
