from sqlalchemy import Column, String, Float, DateTime, JSON
from sqlalchemy.dialects.postgresql import UUID
from app.database import Base
import uuid
from datetime import datetime

class AICyberThreatLog(Base):
    __tablename__ = "ai_cyber_threat_logs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    target_endpoint = Column(String(255), nullable=False, index=True)
    detected_anomaly_type = Column(String(100), nullable=False, index=True) # e.g., SQL_INJECTION, REVERSE_SHELL
    
    # AI Inference Matrix Vectors
    ai_confidence_score = Column(Float, nullable=False) # 0.0 to 1.0 model threshold
    nist_impact_rating = Column(String(50), nullable=False) # LOW, MEDIUM, HIGH, CRITICAL
    
    # Research Metadata Storage
    model_inference_payload = Column(JSON, nullable=True) # Stores vector weights and tokens
    logged_at = Column(DateTime, default=datetime.utcnow, index=True)
