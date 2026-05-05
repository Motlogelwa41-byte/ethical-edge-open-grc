from sqlalchemy import Column, String, Integer, Text, DateTime, Float
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
import uuid
import datetime

Base = declarative_base()

class NGOProfile(Base):
    __tablename__ = "ngo_profiles"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    registration_number = Column(String, unique=True)
    trust_score = Column(Float, default=0.0) # Used by dashboard.html
    compliance_status = Column(String, default="Pending") # Used by dashboard.html
    last_updated = Column(DateTime, default=datetime.datetime.utcnow)

class Risk(Base):
    __tablename__ = "risks"
    risk_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    category = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    impact_score = Column(Integer)
    likelihood_score = Column(Integer)
    status = Column(String, default="Identified")
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class ComplianceFramework(Base):
    __tablename__ = "compliance_frameworks"
    framework_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    framework_name = Column(String, nullable=False)
    requirement_text = Column(Text, nullable=False)
    status = Column(String, default="Under Review")
