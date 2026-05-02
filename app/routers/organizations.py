from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.connection import SessionLocal
from app.services import organization_service
from app.schemas.organization import OrganizationCreate, OrganizationOut

router = APIRouter(prefix="/organizations", tags=["Organizations"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/", response_model=list[OrganizationOut])
def get_organizations(db: Session = Depends(get_db)):
    return organization_service.get_organizations(db)


@router.post("/", response_model=OrganizationOut)
def add_organization(
    org: OrganizationCreate,
    db: Session = Depends(get_db)
):
    return organization_service.create_organization(
        db,
        org.name,
        org.industry
    )
