from sqlalchemy import Column, Integer, String, Boolean, DateTime
from datetime import datetime
from app.database import Base  # Directly wired to our global connection engine

class EnterpriseUser(Base):
    """
    SQLAlchemy database model defining SaaS authorization, multi-tenant company isolation,
    and granular feature flag permissions mapped directly to PostgreSQL.
    """
    __tablename__ = "core_enterprise_users"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(150), nullable=False)
    email = Column(String(150), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    
    # Commercial Isolation Engine
    company_tenant_id = Column(String(100), index=True, nullable=False)
    subscription_tier = Column(String(50), default="STANDARD_FREE")
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)
    
    # Granular Feature Access Controls
    can_access_king_v = Column(Boolean, default=True)
    can_access_nist_cyber = Column(Boolean, default=False)
    can_access_safeguard = Column(Boolean, default=False)
    
    created_at = Column(DateTime, default=datetime.utcnow)
