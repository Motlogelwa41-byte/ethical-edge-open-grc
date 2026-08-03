from fastapi import APIRouter
from fastapi.responses import FileResponse
from pathlib import Path

router = APIRouter(tags=["Climate Demo"])

@router.get("/climate-demo")
async def climate_demo():
    """
    UNICEF Climate Demo Dashboard
    """
    project_root = Path(__file__).resolve().parents[3]
    return FileResponse(project_root / "dashboard_climate.html")
