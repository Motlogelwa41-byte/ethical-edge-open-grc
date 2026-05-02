from sqlalchemy.orm import Session
from app import models


def get_organizations(db: Session):
    return db.query(models.Organization).all()


def create_organization(db: Session, name: str, industry: str):
    org = models.Organization(name=name, industry=industry)
    db.add(org)
    db.commit()
    db.refresh(org)
    return org
