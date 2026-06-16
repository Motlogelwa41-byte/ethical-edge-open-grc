from pydantic import BaseModel, Field, validator
from typing import Optional

class FrameworkRequirement(BaseModel):
    id: str
    category: str
    requirement_text: str
    impact_level: int = Field(..., ge=1, le=5)  # Enforces 1-5 scale
    is_active: bool = True

    @validator('id')
    def id_must_be_alphanumeric(cls, v):
        if not v.isalnum():
            raise ValueError('ID must be alphanumeric')
        return v
