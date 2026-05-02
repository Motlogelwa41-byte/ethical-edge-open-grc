from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.connection import SessionLocal
from app.services import organization_service

router = APIRouter(prefix="/organizations", tags=["Organizations"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/")
def get_organizations(db: Session = Depends(get_db)):
    return organization_service.get_organizations(db)


@router.post("/")
def add_organization(name: str, industry: str, db: Session = Depends(get_db)):
    return organization_service.create_organization(db, name, industry)
