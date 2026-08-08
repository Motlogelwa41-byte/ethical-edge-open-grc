from fastapi import APIRouter
from pydantic import BaseModel

from app.climate.cvi_engine import CVIEngine

router = APIRouter()


class CVIInput(BaseModel):
    environmental_stress: int
    infrastructure_risk: int
    health_capacity: int


@router.post(
    "/api/v1/cvi/public-stream",
    tags=["Child Vulnerability Index"]
)
def public_cvi_stream(data: CVIInput):
    result = CVIEngine.calculate(
        environmental_stress=data.environmental_stress,
        infrastructure_risk=data.infrastructure_risk,
        health_capacity=data.health_capacity,
    )

    return {
        "service": "Child Vulnerability Index",
        "platform": "Cognitive GRC Engine - Climate Edition",
        "status": "operational",
        **result,
    }
