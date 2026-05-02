from pydantic import BaseModel


# Shared fields
class OrganizationBase(BaseModel):
    name: str
    industry: str


# Request schema (Create)
class OrganizationCreate(OrganizationBase):
    pass


# Response schema
class OrganizationOut(OrganizationBase):
    id: int

    class Config:
        from_attributes = True
