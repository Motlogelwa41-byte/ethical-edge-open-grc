from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.connection import SessionLocal
from app.services import risk_service

router = APIRouter(prefix="/risks", tags=["Risks"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/")
def get_risks(db: Session = Depends(get_db)):
    return risk_service.get_risks(db)


@router.post("/")
def add_risk(
    title: str,
    description: str,
    likelihood: int,
    impact: int,
    organization_id: int,
    db: Session = Depends(get_db)
):
    return risk_service.create_risk(
        db,
        title,
        description,
        likelihood,
        impact,
        organization_id
    )
