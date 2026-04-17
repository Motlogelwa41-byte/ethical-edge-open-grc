from .database import Base
from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime

class Risk(Base):
    __tablename__ = "risks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    likelihood = Column(Integer)  # 1-5
    impact = Column(Integer)      # 1-5
    score = Column(Integer)       # Likelihood * Impact
    treatment = Column(String)    # Terminate, Transfer, Treat, Tolerate
    risk_level = Column(String)   # Low, Medium, High, Critical
    created_at = Column(DateTime, default=datetime.utcnow)
