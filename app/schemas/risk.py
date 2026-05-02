from pydantic import BaseModel


# Shared fields
class RiskBase(BaseModel):
    title: str
    description: str
    likelihood: int
    impact: int
    organization_id: int


# Request schema (Create)
class RiskCreate(RiskBase):
    pass


# Response schema
class RiskOut(RiskBase):
    id: int

    class Config:
        from_attributes = True
