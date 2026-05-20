from sqlalchemy import Column, String, Float, DateTime, JSON
import uuid
from datetime import datetime
from app.database import Base

class ClimateRiskAssessment(Base):
    __tablename__ = "climate_risk_assessments"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()), index=True)
    district = Column(String, index=True, nullable=False)  # e.g., Chobe, Okavango, Gaborone
    hazard_type = Column(String, default="COMBINED_CLIMATE_STRESS", nullable=False)
    environmental_hazard_score = Column(Float, nullable=False)
    infrastructure_vulnerability_index = Column(Float, nullable=False)
    calculated_impact_rating = Column(String, nullable=False)  # CRITICAL, HIGH, LOW
    synchronized_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    modeled_parameters = Column(JSON, nullable=True)  # Holds youth infrastructure metrics and tenant tags
