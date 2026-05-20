from sqlalchemy import Column, String, Float, DateTime, JSON
import uuid
from datetime import datetime
from app.database import Base

class AICyberThreatLog(Base):
    __tablename__ = "ai_cyberthreat_logs"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()), index=True)
    target_endpoint = Column(String, index=True, nullable=False)
    detected_anomaly_type = Column(String, nullable=False) # PERIMETER_ANOMALY, ADVERSARIAL_INJECTION
    ai_confidence_score = Column(Float, nullable=False)
    nist_impact_rating = Column(String, nullable=False) # CRITICAL, MEDIUM, LOW
    logged_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    model_inference_payload = Column(JSON, nullable=True) # Contains stripped network footprints for BDPA
