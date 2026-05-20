from sqlalchemy import Column, String, Float, DateTime, JSON
from sqlalchemy.dialects.postgresql import UUID
from app.database import Base
import uuid
from datetime import datetime

class GovernanceAssessment(Base):
    __tablename__ = "governance_assessments"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    company_name = Column(String(255), nullable=False, index=True)
    framework_standard = Column(String(50), default="KING_V", index=True)
    
    # Quantitative Compliance & Auditing Vectors
    transparency_score = Column(Float, nullable=False) # 0.0 to 100.0
    accountability_index = Column(Float, nullable=False) # 0.0 to 100.0
    overall_compliance_percentage = Column(Float, nullable=False)
    
    # Audit trail details
    compliance_status = Column(String(50), nullable=False) # FULLY_COMPLIANT, PARTIALLY_COMPLIANT, NON_COMPLIANT
    assessment_metadata = Column(JSON, nullable=True) # Stores itemized rule checks
    evaluated_at = Column(DateTime, default=datetime.utcnow, index=True)
