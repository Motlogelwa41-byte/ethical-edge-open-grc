from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from .database import Base

# This defines the "AuditLog" table your main.py is looking for
class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, index=True)
    action_taken = Column(String)
    user_id = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)

# This defines the "Risk" blueprint
class Risk(Base):
    __tablename__ = "risks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    impact = Column(Integer)
    likelihood = Column(Integer)
    score = Column(Integer)
