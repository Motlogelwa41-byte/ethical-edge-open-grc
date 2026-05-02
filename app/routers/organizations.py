from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.connection import SessionLocal
from app import models

router = APIRouter(prefix="/organizations", tags=["Organizations"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/")
def get_organizations(db: Session = Depends(get_db)):
    return db.query(models.Organization).all()


@router.post("/")
def add_organization(name: str, industry: str, db: Session = Depends(get_db)):
    org = models.Organization(name=name, industry=industry)
    db.add(org)
    db.commit()
    db.refresh(org)
    return org
