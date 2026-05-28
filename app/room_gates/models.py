from sqlalchemy import Column, String, Boolean, ForeignKey, UniqueConstraint, Integer, DateTime, func
from sqlalchemy.dialects.postgresql import UUID
from database.base import Base # Adjust import based on where your declarative base sits

class GateEvaluation(Base):
    __tablename__ = 'gate_evaluations'
    
    id = Column(UUID(as_uuid=True), primary_key=True, server_default=text("uuid_generate_v4()"))
    assessment_id = Column(UUID(as_uuid=True), ForeignKey('governance_assessments.id', ondelete='CASCADE'), nullable=False)
    gate_id = Column(String(50), ForeignKey('room_gates.gate_id', ondelete='CASCADE'), nullable=False)
    is_passed = Column(Boolean, default=False)
    telemetry_proof_url = Column(String)
    evaluated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # FIX: Enforce the unique compound constraint at the SQLAlchemy model layer
    __table_args__ = (
        UniqueConstraint('assessment_id', 'gate_id', name='unique_assessment_gate'),
    )
