from sqlalchemy import Column, String, Boolean, DateTime, Integer, text
from sqlalchemy.dialects.postgresql import UUID
from database.base import Base

class GateEvaluation(Base):
    __tablename__ = "gate_evaluations"
    
    id = Column(UUID(as_uuid=True), primary_key=True, server_default=text("uuid_generate_v4()"))
    vendor_name = Column(String, nullable=False)
    vetting_score = Column(Integer, default=0)
    passed_integrity = Column(Boolean, default=False)
    checked_at = Column(DateTime, nullable=True)

class VendorIntegrityAudit(Base):
    __tablename__ = "vendor_integrity_audits"
    
    id = Column(UUID(as_uuid=True), primary_key=True, server_default=text("uuid_generate_v4()"))
    vendor_id = Column(String, nullable=False)
    risk_rating = Column(String, nullable=False)
    compliance_status = Column(String, nullable=False)
    last_evaluated = Column(DateTime, nullable=True)
