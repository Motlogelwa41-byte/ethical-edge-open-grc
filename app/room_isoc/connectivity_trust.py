from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from typing import List, Dict, Any
from sqlalchemy.orm import Session

# Import your database core layer and models
from app.database import get_db
from app.room_isoc.models import NetworkTelemetry

# Import the monetization tier guard
from app.auth.monetization import SubscriptionGuard

router = APIRouter(
    prefix="/isoc",
    tags=["Internet Society - Community Network Trust"]
)

# 1. ISOC TELEMETRY INGESTION SCHEMAS
class MeshNodeTelemetryInput(BaseModel):
    node_id: str = Field(..., example="NODE_CHOBE_EAST_01")
    latency_ms: float = Field(..., ge=0.0, description="Ping round-trip latency")
    packet_loss_percentage: float = Field(..., ge=0.0, le=100.0)
    manrs_security_profile_passed: bool = Field(..., description="Validates routing security standard compliance")
    solar_power_reserve_percentage: float = Field(..., ge=0.0, le=100.0, description="Off-grid battery status")

# 2. STATUS TRACKING ENDPOINT
@router.get("/status")
async def get_isoc_room_status():
    """
    Returns the real-time status of the Community Network Trust engine.
    """
    return {
        "room": "Internet Society Community Wing",
        "engine_status": "ACTIVE",
        "focus": "Resilient Mesh Networking, Telemetry Auditing & MANRS Security",
        "operational_state": "PRODUCTION_READY"
    }

# 3. DATABASE-INTEGRATED TELEMETRY COMPONENT (WITH MONETIZATION GUARD)
@router.post("/log-telemetry", status_code=status.HTTP_201_CREATED)
async def log_node_telemetry(
    telemetry: MeshNodeTelemetryInput,
    tenant_id: str, # Requires the client to pass their UUID token
    db: Session = Depends(get_db),
    _sub_check = Depends(SubscriptionGuard(required_room="isoc")) # Restricts to Enterprise Premium Tier
):
    """
    Ingests off-grid mesh node telemetry, computes system resiliency metrics,
    checks tier authorization, and logs the payload directly into PostgreSQL.
    Accessible only by Enterprise Premium Tier accounts.
    """
    # Algorithmic calculation of operational health
    is_operational = not (telemetry.packet_loss_percentage > 5.0 or telemetry.latency_ms > 150.0)
    
    if is_operational and telemetry.manrs_security_profile_passed:
        health_status = "OPTIMAL_HEALTH"
        incident_alert_level = "NONE"
    elif not telemetry.manrs_security_profile_passed:
        health_status = "SECURITY_BREACH_VULNERABILITY"
        incident_alert_level = "HIGH"
    else:
        health_status = "DEGRADED_PERFORMANCE"
        incident_alert_level = "MEDIUM"

    # Instantiate the database record using our relational model mapping
    telemetry_record = NetworkTelemetry(
        node_identifier=telemetry.node_id,
        latency=telemetry.latency_ms,
        packet_loss=telemetry.packet_loss_percentage,
        is_manrs_compliant=telemetry.manrs_security_profile_passed,
        node_status=health_status,
        telemetry_metadata={
            "solar_power_reserve_percentage": telemetry.solar_power_reserve_percentage,
            "incident_alert_level": incident_alert_level,
            "verified_tenant_id": tenant_id
        }
    )

    # Commit transaction to the PostgreSQL database pool
    db.add(telemetry_record)
    db.commit()
    db.refresh(telemetry_record)

    return {
        "telemetry_id": str(telemetry_record.id),
        "node_monitored": telemetry_record.node_identifier,
        "computed_metrics": {
            "node_operational_state": telemetry_record.node_status,
            "incident_alert_level": incident_alert_level
        },
        "database_sync": "RECORD_COMMITTED"
    }
