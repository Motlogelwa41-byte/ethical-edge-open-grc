from sqlalchemy import Column, String, Float, Integer, DateTime, JSON
import uuid
from datetime import datetime
from app.database import Base

class HealthFacilitySurveillance(Base):
    __tablename__ = "health_facility_surveillance"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()), index=True)
    facility_name = Column(String, index=True, nullable=False)
    district = Column(String, nullable=False)
    network_latency_ms = Column(Float, default=0.0)
    data_payload_size_kb = Column(Float, nullable=False)
    reporting_delay_minutes = Column(Integer, nullable=False)
    surveillance_urgency_tier = Column(String, nullable=False)  # CRITICAL, ELEVATED, LOW
    system_status_summary = Column(String, nullable=False)
    synchronized_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    custom_telemetry_payload = Column(JSON, nullable=True)  # Stores zero-PII metrics and tenant tokens
