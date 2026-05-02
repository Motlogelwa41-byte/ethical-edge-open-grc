from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
import enum

from database import Base


# --------------------
# ENUMS
# --------------------
class RiskStatus(str, enum.Enum):
    open = "open"
    in_progress = "in_progress"
    mitigated = "mitigated"
    closed = "closed"


# --------------------
# ORGANIZATION
# --------------------
class Organization(Base):
    __tablename__ = "organizations"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    industry = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    risks = relationship("Risk", back_populates="organization")


# --------------------
# RISK
# --------------------
class Risk(Base):
    __tablename__ = "risks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)

    likelihood = Column(Integer, default=1)
    impact = Column(Integer, default=1)

    status = Column(Enum(RiskStatus), default=RiskStatus.open)

    organization_id = Column(Integer, ForeignKey("organizations.id"))

    organization = relationship("Organization", back_populates="risks")
    controls = relationship("Control", back_populates="risk")


# --------------------
# CONTROL
# --------------------
class Control(Base):
    __tablename__ = "controls"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(Text, nullable=True)

    effectiveness = Column(Integer, default=1)

    risk_id = Column(Integer, ForeignKey("risks.id"))

    risk = relationship("Risk", back_populates="controls")
