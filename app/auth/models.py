<<<<<<< Updated upstream
from sqlalchemy import Column, Integer, String, Boolean
from app.database.models import Base

class EnterpriseUser(Base):
    __tablename__ = "core_enterprise_users"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, nullable=True)
    email = Column(String, unique=True, index=True, nullable=False)

    can_access_king_v = Column(Boolean, default=True)
    can_access_professional_tier = Column(Boolean, default=False)
    can_access_enterprise = Column(Boolean, default=False)
=======
from sqlalchemy import Column, Integer, String, Boolean; from app.database.models import Base; class EnterpriseUser(Base): __tablename__ = "core_enterprise_users"; id = Column(Integer, primary_key=True, index=True); full_name = Column(String, nullable=True); email = Column(String, unique=True, index=True, nullable=False); can_access_king_v = Column(Boolean, default=True); can_access_professional_tier = Column(Boolean, default=False); can_access_enterprise = Column(Boolean, default=False)
>>>>>>> Stashed changes
