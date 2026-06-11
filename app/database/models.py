# app/database/models.py

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime

# Initialize Base here, do NOT import it from this file
Base = declarative_base()

# Define your models below
class ComplianceRecord(Base):
    __tablename__ = "compliance_records"
    id = Column(Integer, primary_key=True)
    # ... rest of your model code
