<<<<<<< Updated upstream
from sqlalchemy import Column, Integer, String, Float, DateTime, Text, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class AuditRun(Base):
    __tablename__ = "audit_runs"
    id = Column(Integer, primary_key=True, index=True)
    tenant_id = Column(String, index=True, nullable=False)
    timestamp = Column(DateTime, nullable=False)
    attainment_rate = Column(Float, nullable=False)
    findings = relationship("ControlFinding", back_populates="audit_run", cascade="all, delete-orphan")

class ControlFinding(Base):
    __tablename__ = "control_findings"
    id = Column(Integer, primary_key=True, index=True)
    audit_run_id = Column(Integer, ForeignKey("audit_runs.id"), nullable=False)
    control_reference = Column(String, nullable=False)
    control_name = Column(String, nullable=False)
    framework = Column(String, nullable=False)
    status = Column(String, nullable=False)
    evidence_payload = Column(Text, nullable=False)
    audit_run = relationship("AuditRun", back_populates="findings")
=======
from sqlalchemy.orm import declarative_base
Base = declarative_base()
>>>>>>> Stashed changes
