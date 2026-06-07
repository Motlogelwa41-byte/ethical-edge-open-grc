from sqlalchemy import Column, Integer, String, DateTime, JSON, func
from app.database.connection import Base

class AuditLog(Base):
    __tablename__ = "compliance_audit_log"
    
    log_id = Column(Integer, primary_key=True, index=True)
    gate_id = Column(String(50))
    event_type = Column(String(20))
    previous_status = Column(String(20))
    new_status = Column(String(20))
    actor = Column(String(50), default="SYSTEM")
    timestamp = Column(DateTime, default=func.now())
    evidence_snapshot = Column(JSON) # Stores the JSON payload from the observer
