from sqlalchemy import Column, String, Float, Integer, DateTime, JSON
from sqlalchemy.dialects.postgresql import UUID
from app.database import Base
import uuid
from datetime import datetime

class HealthFacilitySurveillance(Base):
    __tablename__ = "health_facility_surveillance"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    facility_name = Column(String(255), nullable=False, index=True) # e.g., Shakawe Clinic
    district = Column(String(100), nullable=False, index=True) # e.g., Ngamiland
    
    # Technical Latency & Reporting Transmission Metrics
    network_latency_ms = Column(Float, nullable=False)
    data_payload_size_kb = Column(Float, nullable=False)
    reporting_delay_minutes = Column(Integer, nullable=False) # Time elapsed between field capture and server sync
    
    # Epidemiological Impact Calculation Metrics
    surveillance_urgency_tier = Column(String(50), nullable=False) # LOW, ELEVATED, CRITICAL
    system_status_summary = Column(String(255), nullable=False)
    
    # Audit & Tracking
    synchronized_at = Column(DateTime, default=datetime.utcnow, index=True)
