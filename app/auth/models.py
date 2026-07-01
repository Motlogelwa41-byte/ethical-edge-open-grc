from sqlalchemy import Column, Integer, String, Boolean
from app.database.models import Base

class EnterpriseUser(Base):
    __tablename__ = "core_enterprise_users"

    # RESTORED CORE FIELDS (Fixes the Primary Key Crash)
    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, nullable=True)
    email = Column(String, unique=True, index=True, nullable=False)

    # Feature Access Controls to match SubscriptionGuard
    can_access_king_v = Column(Boolean, default=True) # Matches 'core_grc'
    
    # These map to 'google', 'unicef' (Professional Tier)
    can_access_professional_tier = Column(Boolean, default=False) 
    
    # These map to 'gates', 'isoc', 'safeguard' (Enterprise Premium Tier)
    can_access_enterprise = Column(Boolean, default=False)
