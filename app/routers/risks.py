from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.connection import SessionLocal
from app import models

router = APIRouter(prefix="/risks", tags=["Risks"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/")
def get_risks(db: Session = Depends(get_db)):
    return db.query(models.Risk).all()


@router.post("/")
def add_risk(
    title: str,
    description: str,
    likelihood: int,
    impact: int,
    organization_id: int,
    db: Session = Depends(get_db)
):
    risk = models.Risk(
        title=title,
        description=description,
        likelihood=likelihood,
        impact=impact,
        organization_id=organization_id
    )

    db.add(risk)
    db.commit()
    db.refresh(risk)

    return risk
