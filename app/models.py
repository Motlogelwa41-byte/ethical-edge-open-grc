from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from .database import Base

class Risk(Base):
    __tablename__ = "risks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    likelihood = Column(Integer, nullable=False)
    impact = Column(Integer, nullable=False)
    score = Column(Integer, nullable=False)
    level = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
