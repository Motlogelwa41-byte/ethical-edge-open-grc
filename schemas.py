from pydantic import BaseModel, Field, validator
from typing import List, Optional

class RecommendedPractice(BaseModel):
    practice_id: str
    description: str
    is_mandatory: bool = False

class KingVPrinciple(BaseModel):
    principle_number: int = Field(..., ge=1, le=17) # King IV has 17 principles
    title: str
    description: str
    # Ensures every Principle contains its nested practices
    practices: List[RecommendedPractice]

    @validator('practices')
    def must_have_practices(cls, v):
        if not v:
            raise ValueError('A King IV Principle must have associated recommended practices.')
        return v
