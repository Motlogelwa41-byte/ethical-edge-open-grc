from sqlalchemy.orm import Session
from app import models


def get_risks(db: Session):
    return db.query(models.Risk).all()


def create_risk(
    db: Session,
    title: str,
    description: str,
    likelihood: int,
    impact: int,
    organization_id: int
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
