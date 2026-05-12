from sqlalchemy import Column, String, Integer, Text, DateTime, Float, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
import uuid
import datetime

Base = declarative_base()

class NGOProfile(Base):
    __tablename__ = "ngo_profiles"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    registration_number = Column(String, unique=True)
    trust_score = Column(Float, default=0.0) 
    compliance_status = Column(String, default="Pending") 
    last_updated = Column(DateTime, default=datetime.datetime.utcnow)
    
    # Relationship: One NGO can have many risks
    risks = relationship("Risk", back_populates="owner")

class Risk(Base):
    __tablename__ = "risks"
    risk_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String, nullable=False) # Aligned with RiskRequest in main.py
    category = Column(String, nullable=True)
    description = Column(Text, nullable=False)
    impact_score = Column(Integer)
    likelihood_score = Column(Integer)
    status = Column(String, default="Identified")
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    
    # Foreign Key to link to an NGO
    ngo_id = Column(UUID(as_uuid=True), ForeignKey("ngo_profiles.id"), nullable=True)
    owner = relationship("NGOProfile", back_populates="risks")

class ComplianceFramework(Base):
    __tablename__ = "compliance_frameworks"
    framework_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    framework_name = Column(String, nullable=False) # e.g., "King IV", "ISO 31000"
    requirement_text = Column(Text, nullable=False)
    status = Column(String, default="Under Review")
