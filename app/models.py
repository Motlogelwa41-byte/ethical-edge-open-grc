from sqlalchemy import Column, String, Integer, Text, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
import uuid
import datetime

Base = declarative_base()

class Risk(Base):
    __tablename__ = "risks"
    risk_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    category = Column(String, nullable=False) # Financial, Operational, etc.
    description = Column(Text, nullable=False)
    impact_score = Column(Integer)
    likelihood_score = Column(Integer)
    status = Column(String, default="Identified")
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class ComplianceFramework(Base):
    __tablename__ = "compliance_frameworks"
    framework_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    framework_name = Column(String, nullable=False) # King V, ISO 31000
    requirement_text = Column(Text, nullable=False)
    status = Column(String, default="Under Review")

class AuditLog(Base):
    __tablename__ = "audit_logs"
    log_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    action_taken = Column(Text, nullable=False)
    user_id = Column(String, default="System AI")
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
