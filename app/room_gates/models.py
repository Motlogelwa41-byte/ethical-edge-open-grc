port Column, String, Float, DateTime, JSON
import uuid
from datetime import datetime
from app.database import Base

class VendorIntegrityAudit(Base):
    __tablename__ = "vendor_integrity_audits"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()), index=True)
    entity_name = Column(String, index=True, nullable=False)
    country_of_origin = Column(String, default="SADC Region", nullable=False)
    pep_status_verified = Column(Boolean, default=True)
    sanction_list_collision = Column(Boolean, default=False)
    calculated_integrity_score = Column(Float, nullable=False)
    vetting_decision = Column(String, nullable=False)  # APPROVED, REVIEW_REQUIRED, REJECTED
    audited_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    audit_metadata = Column(JSON, nullable=True)  # Houses efficiency variances, burn rates, and tenant tags
