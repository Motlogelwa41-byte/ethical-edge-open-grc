from sqlalchemy import Column, String, Float, Boolean, DateTime, JSON
from sqlalchemy.dialects.postgresql import UUID
import uuid
from datetime import datetime
from app.database import Base

class NetworkTelemetry(Base):
    __tablename__ = "network_telemetry_logs"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()), index=True)
    node_identifier = Column(String, index=True, nullable=False)
    latency = Column(Float, nullable=False)
    packet_loss = Column(Float, nullable=False)
    is_manrs_compliant = Column(Boolean, default=True, nullable=False)
    node_status = Column(String, nullable=False) # OPTIMAL_HEALTH, DEGRADED, BREACH
    synchronized_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    # Store critical metadata like solar battery capacity and tenant reference keys
    telemetry_metadata = Column(JSON, nullable=True)
