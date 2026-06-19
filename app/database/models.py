from sqlalchemy import Column, Integer, String, Float, DateTime, Text, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

# Define the declarative base that session.py is looking for
Base = declarative_base()

class AuditRun(Base):
    __tablename__ = "audit_runs"

    id = Column(Integer, primary_key=True, index=True)
    tenant_id = Column(String, index=True, nullable=False)
    timestamp = Column(DateTime, nullable=False)
    attainment_rate = Column(Float, nullable=False)

    # Relationship to link findings to this specific audit run
    findings = relationship("ControlFinding", back_populates="audit_run", cascade="all, delete-orphan")


class ControlFinding(Base):
    __tablename__ = "control_findings"

    id = Column(Integer, primary_key=True, index=True)
    audit_run_id = Column(Integer, ForeignKey("audit_runs.id"), nullable=False)
    control_reference = Column(String, nullable=False)  # e.g., "ISO 31000-5.1" or "BDPA-Section 3"
    control_name = Column(String, nullable=False)
    framework = Column(String, nullable=False)          # e.g., "ISO31000", "BDPA", "NIST"
    status = Column(String, nullable=False)             # e.g., "COMPLIANT", "NON_COMPLIANT"
    evidence_payload = Column(Text, nullable=False)     # JSON string storing telemetry snapshot

    # Back reference to the parent audit run
    audit_run = relationship("AuditRun", back_populates="findings")
