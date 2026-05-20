from sqlalchemy import Column, String, Float, Integer, DateTime, ForeignKey, JSON
from sqlalchemy.dialects.postgresql import UUID
from app.database import Base
import uuid
from datetime import datetime

class NetworkTelemetry(Base):
    __tablename__ = "network_telemetry"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    node_id = Column(String(50), nullable=False, index=True) # Unique ID per village router node
    district = Column(String(100), nullable=False, index=True) # e.g., Chobe, Kgalagadi
    
    # Meaningful Connectivity & Performance Indicators (Pillar 3 & 4)
    packet_loss_percentage = Column(Float, nullable=False)
    latency_ms = Column(Float, nullable=False)
    bandwidth_mbps = Column(Float, nullable=False)
    manrs_violations_count = Column(Integer, default=0)
    
    # Greening the Internet Environmental Tracking (Pillar 2)
    solar_battery_voltage = Column(Float, nullable=True)
    solar_panel_output_watts = Column(Float, nullable=True)
    ambient_temperature_celsius = Column(Float, nullable=True)
    local_weather_anomaly = Column(String(255), default="NORMAL") # Captures extreme events (floods/droughts)
    
    # Extensible Metadata Layer for Regional Parameters
    custom_telemetry_payload = Column(JSON, nullable=True)
    
    # Auditing & Open Knowledge Timestamping
    captured_at = Column(DateTime, default=datetime.utcnow, index=True)
