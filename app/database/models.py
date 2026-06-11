from sqlalchemy import Column, ForeignKey, String, Float, Integer, Text
from sqlalchemy.orm import relationship, declarative_base # Import this!
from sqlalchemy.dialects.postgresql import UUID
import uuid

# 1. Define Base here, NOT by importing it from this file.
Base = declarative_base()

# 2. Now define your TenantMixin and models below it.
class TenantMixin:
    """Mixin to ensure all models are tenant-aware."""
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenants.id"), nullable=False, index=True)

class ControlFinding(Base, TenantMixin):
    __tablename__ = "control_findings"
    # ... rest of your code remains the same
