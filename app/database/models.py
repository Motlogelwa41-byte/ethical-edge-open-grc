from sqlalchemy import Column, ForeignKey, String, Float, Integer, Text
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
import uuid
from app.database import Base

class TenantMixin:
    """Mixin to ensure all models are tenant-aware."""
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenants.id"), nullable=False, index=True)

class ControlFinding(Base, TenantMixin):
    __tablename__ = "control_findings"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    audit_run_id = Column(UUID(as_uuid=True), ForeignKey("audit_runs.id"), nullable=False)
    
    # Metadata
    control_reference = Column(String(20), index=True, nullable=False) 
    control_name = Column(String(150), nullable=False)
    domain = Column(String(100), nullable=True)
    framework = Column(String(100), nullable=False)
    
    # Quantitative & Qualitative
    weight = Column(Float, default=1.0)
    status = Column(String(10), nullable=False)
    maturity_score = Column(Integer, nullable=True)
    evidence_payload = Column(Text, nullable=False)
    
    # Relationship (Ensure AuditRun also inherits TenantMixin!)
    audit_run = relationship("AuditRun", back_populates="findings")
