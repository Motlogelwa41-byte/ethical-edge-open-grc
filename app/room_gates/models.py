from sqlalchemy import Column, String, Boolean, Float, DateTime, JSON
from sqlalchemy.dialects.postgresql import UUID
from app.database import Base
import uuid
from datetime import datetime

class VendorIntegrityAudit(Base):
    __tablename__ = "vendor_integrity_audits"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    entity_name = Column(String(255), nullable=False, index=True)
    registration_number = Column(String(100), nullable=True)
    country_of_origin = Column(String(100), default="Botswana", index=True)
    
    # Risk and Integrity Ratings
    pep_status_verified = Column(Boolean, default=False)
    sanction_list_collision = Column(Boolean, default=False)
    calculated_integrity_score = Column(Float, nullable=False) # 0.0 to 100.0
    vetting_decision = Column(String(50), nullable=False) # APPROVED, REVIEW_REQUIRED, REJECTED
    
    # Audit trail details
    audit_metadata = Column(JSON, nullable=True)
    audited_at = Column(DateTime, default=datetime.utcnow, index=True)
