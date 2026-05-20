from sqlalchemy import Column, String, Float, DateTime, JSON
from sqlalchemy.dialects.postgresql import UUID
import uuid
from datetime import datetime
from app.database import Base

class GovernanceAssessment(Base):
    __tablename__ = "governance_assessments"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()), index=True)
    company_name = Column(String, index=True, nullable=False)
    framework_standard = Column(String, default="KING_V", nullable=False)
    transparency_score = Column(Float, nullable=False)
    accountability_index = Column(Float, nullable=False)
    overall_compliance_percentage = Column(Float, nullable=False)
    compliance_status = Column(String, nullable=False) # FULLY_COMPLIANT, PARTIALLY_COMPLIANT, NON_COMPLIANT
    evaluated_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    assessment_metadata = Column(JSON, nullable=True) # Holds pillar breakdown and tenant tags
