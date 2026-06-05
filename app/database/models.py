from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects.postgresql import UUID

class TenantMixin:
    """Mixin to ensure all models are tenant-aware."""
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenants.id"), nullable=False, index=True)

class ControlFinding(Base):
    __tablename__ = "control_findings"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    audit_run_id = Column(Integer, ForeignKey("audit_runs.id"), nullable=False)
    
    # Metadata from your JSON
    control_reference = Column(String(20), index=True, nullable=False) 
    control_name = Column(String(150), nullable=False)
    domain = Column(String(100), nullable=True)     # Added: Maps to "domain" (e.g., Leadership)
    framework = Column(String(100), nullable=False)
    
    # Quantitative & Qualitative fields
    weight = Column(Float, default=1.0)              # Added: Maps to "weight"
    status = Column(String(10), nullable=False)       # PASSED or FAILED
    maturity_score = Column(Integer, nullable=True)   # New: For qualitative assessment
    
    evidence_payload = Column(Text, nullable=False)
    
    audit_run = relationship("AuditRun", back_populates="findings")
