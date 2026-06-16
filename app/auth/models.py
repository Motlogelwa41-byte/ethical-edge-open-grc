from sqlalchemy import Column, Boolean
from app.database.models import Base

class EnterpriseUser(Base):
    __tablename__ = "core_enterprise_users"

    # ... (Keep existing fields: id, full_name, email, etc.) ...

    # UPDATED: Feature Access Controls to match SubscriptionGuard
    can_access_king_v = Column(Boolean, default=True) # Matches 'core_grc'
    
    # These map to 'google', 'unicef' (Professional Tier)
    can_access_professional_tier = Column(Boolean, default=False) 
    
    # These map to 'gates', 'isoc', 'safeguard' (Enterprise Premium Tier)
    can_access_enterprise = Column(Boolean, default=False) 

    # (Optional) Keep 'can_access_nist_cyber' and 'can_access_safeguard' 
    # if you still need them for specific legacy modules

