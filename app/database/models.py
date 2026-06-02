from sqlalchemy import Column, String, Float, Integer, ForeignKey, Text, DateTime
from sqlalchemy.orm import relationship, declarative_base
from datetime import datetime, timezone

Base = declarative_base()

class AuditRun(Base):
    """Tracks every time the GRC Engine executes a scan for a specific client."""
    __tablename__ = "audit_runs"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    tenant_id = Column(String(50), index=True, nullable=False)
    timestamp = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    attainment_rate = Column(Float, nullable=False)
    
    # Relationship to individual control findings
    findings = relationship("ControlFinding", back_populates="audit_run", cascade="all, delete-orphan")

class ControlFinding(Base):
    """Stores the granular cryptographic/API evidence payload for each individual control."""
    __tablename__ = "control_findings"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    audit_run_id = Column(Integer, ForeignKey("audit_runs.id"), nullable=False)
    control_reference = Column(String(20), index=True, nullable=False)  # e.g., A.8.5, PR.DS-01
    control_name = Column(String(150), nullable=False)
    framework = Column(String(100), nullable=False)                    # e.g., ISO 27001, King V
    status = Column(String(10), nullable=False)                       # PASSED or FAILED
    evidence_payload = Column(Text, nullable=False)                    # Raw JSON data stored as Text
    
    audit_run = relationship("AuditRun", back_populates="findings")
