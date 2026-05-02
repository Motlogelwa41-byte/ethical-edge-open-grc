from app.auth.dependencies import get_current_user
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.connection import SessionLocal
from app.services import risk_service
from app.schemas.risk import RiskCreate, RiskOut

router = APIRouter(prefix="/risks", tags=["Risks"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/", response_model=list[RiskOut])
def get_risks(db: Session = Depends(get_db)):
    return risk_service.get_risks(db)


@router.post("/", response_model=RiskOut)
def add_risk(
    risk: RiskCreate,
    db: Session = Depends(get_db)
):
    return risk_service.create_risk(
        db,
        risk.title,
        risk.description,
        risk.likelihood,
        risk.impact,
        risk.organization_id
    )
