from sqlalchemy import Column, String, Float, DateTime, JSON
from sqlalchemy.dialects.postgresql import UUID
from app.database import Base
import uuid
from datetime import datetime

class ClimateRiskAssessment(Base):
    __tablename__ = "climate_risk_assessments"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    district = Column(String(100), nullable=False, index=True) # e.g., Ngamiland, Central
    hazard_type = Column(String(100), nullable=False) # e.g., FLOOD, DROUGHT, EXTREME_HEAT
    
    # Computational Risk Indicators (Ingested by Room 4)
    environmental_hazard_score = Column(Float, nullable=False) # 0.0 to 1.0
    infrastructure_vulnerability_index = Column(Float, nullable=False) # 0.0 to 1.0
    calculated_impact_rating = Column(String(50), nullable=False) # LOW, MEDIUM, HIGH, CRITICAL
    
    # Open Knowledge Metadata Layer
    modeled_parameters = Column(JSON, nullable=True) # Stores weather variables, drought indices
    
    # Audit & Tracking
    assessed_at = Column(DateTime, default=datetime.utcnow, index=True)
