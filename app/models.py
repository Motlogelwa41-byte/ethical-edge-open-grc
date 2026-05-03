from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base

class Organization(Base):
    __tablename__ = "organizations"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    reg_number = Column(String(100), unique=True)
    risks = relationship("Risk", back_populates="owner")

class Framework(Base):
    __tablename__ = "frameworks"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100))        # King V, ISO 27001, NIST
    section = Column(String(100))     # Principle 1, A.5.1, etc.
    description = Column(Text)

class Risk(Base):
    __tablename__ = "risks"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255))
    description = Column(Text)
    org_id = Column(Integer, ForeignKey("organizations.id"))
    owner = relationship("Organization", back_populates="risks")
   
