from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from typing import Optional, Dict, Any
from app.database import get_db
from app.isoc.models import NetworkTelemetry
from app.auth.security import strip_pii_for_bdpa_compliance

router = APIRouter(
    prefix="/isoc",
    tags=["Pillar 4 - Internet Society Trust Network Room"]
)

class TelemetryIngestInput(BaseModel):
    node_id: str = Field(..., example="NODE_CHOBE_012")
    district: str = Field(..., example="Chobe District")
    packet_loss_percentage: float = Field(..., example=0.45)
    latency_ms: float = Field(..., example=12.4)
    bandwidth_mbps: float = Field(..., example=45.2)
    solar_battery_voltage: Optional[float] = Field(None, example=13.8)
    solar_panel_output_watts: Optional[float] = Field(None, example=85.0)
    ambient_temperature_celsius: Optional[float] = Field(None, example=34.5)
    local_weather_anomaly: Optional[str] = Field("NORMAL", example="EXTREME_HEAT")
    raw_device_metadata: Optional[Dict[str, Any]] = Field(None, description="Contains non-PII operational settings")

@router.post("/telemetry/ingest", status_code=status.HTTP_201_CREATED)
async def ingest_edge_research_data(payload: TelemetryIngestInput, db: Session = Depends(get_db)):
    """
    Ingests live telemetry from experimental rural nodes, runs it through the BDPA Privacy Shield 
    interceptor at the edge, and logs the records safely to PostgreSQL.
    """
    # 1. Convert input to dict and enforce zero-PII data stripping under the BDPA
    raw_data = payload.dict()
    sanitized_metadata = strip_pii_for_bdpa_compliance(raw_data.get("raw_device_metadata") or {})
    
    # 2. Map input variables directly to the relational database structure
    telemetry_record = NetworkTelemetry(
        node_id=payload.node_id,
        district=payload.district,
        packet_loss_percentage=payload.packet_loss_percentage,
        latency_ms=payload.latency_ms,
        bandwidth_mbps=payload.bandwidth_mbps,
        solar_battery_voltage=payload.solar_battery_voltage,
        solar_panel_output_watts=payload.solar_panel_output_watts,
        ambient_temperature_celsius=payload.ambient_temperature_celsius,
        local_weather_anomaly=payload.local_weather_anomaly,
        custom_telemetry_payload=sanitized_metadata
    )
    
    # 3. Securely commit transaction block
    db.add(telemetry_record)
    db.commit()
    db.refresh(telemetry_record)
    
    return {
        "status": "TELEMETRY_INGESTED",
        "record_id": str(telemetry_record.id),
        "node_context": telemetry_record.node_id,
        "privacy_shield": "VERIFIED_ZERO_PII_COMPLIANT"
    }
