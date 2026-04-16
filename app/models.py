from sqlalchemy import Column, String, Integer, Text, DateTime, Float
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
import uuid
import datetime

Base = declarative_base()

class NGOProfile(Base):
    __tablename__ = "ngo_profiles"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    trust_score = Column(Float)
    compliance_status = Column(String)
    last_vetted = Column(DateTime, default=datetime.datetime.utcnow)

class AuditLog(Base):
    __tablename__ = "audit_logs"
    log_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    action_taken = Column(Text, nullable=False)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
