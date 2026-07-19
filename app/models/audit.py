from sqlalchemy import Column, Integer, String, DateTime, Float, JSON, ForeignKey, func
from sqlalchemy.orm import relationship
from app.database.connection import Base

# =====================================================================
# 1. HISTORICAL EVENT TRANSACTION LOG (Immutable Audit Trail)
# =====================================================================
class AuditLog(Base):
    """
    Tracks state-machine changes, gate transitions, and system telemetry events.
    Provides the core evidence trail required for King V and SADC regional frameworks.
    """
    __tablename__ = "compliance_audit_log"
    
    log_id = Column(Integer, primary_key=True, index=True)
    gate_id = Column(String(50), index=True)
    event_type = Column(String(20), index=True)  # e.g., "SWEEP", "ESCALATION"
    previous_status = Column(String(20))
    new_status = Column(String(20))
    actor = Column(String(50), default="SYSTEM")
    timestamp = Column(DateTime, default=func.now())
    evidence_snapshot = Column(JSON)  # Stores raw payload from observers or intake engines


# =====================================================================
# 2. EXECUTIVE COMPLIANCE RUNS (Aggregated Batches)
# =====================================================================
class AuditRun(Base):
    """
    Represents an overarching evaluation sequence for a tenant at a specific point in time.
    Calculates overall GRC performance (attainment rate) for reporting dashboards.
    """
    __tablename__ = "audit_runs"

    id = Column(Integer, primary_key=True, index=True)
    tenant_id = Column(String(100), index=True, nullable=False)
    timestamp = Column(DateTime, default=func.now(), nullable=False)
    attainment_rate = Column(Float, default=0.0)  # Numeric performance score (e.g., 85.5%)

    # Relationship to individual granular findings
    findings = relationship("ControlFinding", back_populates="audit_run", cascade="all, delete-orphan")


# =====================================================================
# 3. GRANULAR CONTROL FINDINGS (Framework Requirements Alignment)
# =====================================================================
class ControlFinding(Base):
    """
    Maps specific evaluations against discrete regulatory frameworks (UNICEF, King V, BDPA).
    Links directly back to an AuditRun for relational tracking and historical trend analysis.
    """
    __tablename__ = "control_findings"

    id = Column(Integer, primary_key=True, index=True)
    audit_run_id = Column(Integer, ForeignKey("audit_runs.id", ondelete="CASCADE"), nullable=False)
    control_reference = Column(String(50), index=True, nullable=False)  # e.g., "UNICEF-CCRI-V1", "KING-V-CH1"
    control_name = Column(String(150), nullable=False)
    framework = Column(String(100), index=True, nullable=False)        # e.g., "UNICEF_Child_Safeguarding", "BDPA"
    status = Column(String(50), nullable=False)                        # e.g., "PASSED", "ACTION_REQUIRED", "COMPLIANT"
    evidence_payload = Column(JSON)                                    # Anonymized scoring output or data verification context

    # Inverse relationship mapping back to parent batch
    audit_run = relationship("AuditRun", back_populates="findings")
