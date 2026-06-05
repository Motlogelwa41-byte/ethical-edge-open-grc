from sqlalchemy import Column, String, Integer, Text, DateTime, Float, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
import uuid
import datetime

Base = declarative_base()

class Tenant(Base):
    """The root container for all client data."""
    __tablename__ = "tenants"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False, unique=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    # Allows us to easily fetch all resources for this client
    ngo_profiles = relationship("NGOProfile", back_populates="tenant")

class NGOProfile(Base):
    __tablename__ = "ngo_profiles"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    # MANDATORY: Link to the Tenant
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenants.id"), nullable=False)
    
    name = Column(String, nullable=False)
    registration_number = Column(String, unique=True)
    trust_score = Column(Float, default=0.0) 
    compliance_status = Column(String, default="Pending") 
    last_updated = Column(DateTime, default=datetime.datetime.utcnow)
    
    tenant = relationship("Tenant", back_populates="ngo_profiles")
    risks = relationship("Risk", back_populates="owner")

class Risk(Base):
    __tablename__ = "risks"
    risk_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    # MANDATORY: Link to the Tenant
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenants.id"), nullable=False)
    
    title = Column(String, nullable=False)
    category = Column(String, nullable=True)
    description = Column(Text, nullable=False)
    impact_score = Column(Integer)
    likelihood_score = Column(Integer)
    status = Column(String, default="Identified")
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    
    ngo_id = Column(UUID(as_uuid=True), ForeignKey("ngo_profiles.id"), nullable=True)
    owner = relationship("NGOProfile", back_populates="risks")

class ComplianceFramework(Base):
    __tablename__ = "compliance_frameworks"
    framework_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    # MANDATORY: Link to the Tenant
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenants.id"), nullable=False)
    
    framework_name = Column(String, nullable=False)
    requirement_text = Column(Text, nullable=False)
    status = Column(String, default="Under Review")

# Add this class to your models.py
class TenantMixin:
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenants.id"), nullable=False, index=True)

# Update your existing classes to inherit from TenantMixin
class Risk(Base, TenantMixin):
    # ... existing fields ...
    pass

class GovernanceAssessment(Base, TenantMixin):
    # ... existing fields ...
    pass
