print(">>> MAIN.PY IS LOADED <<<")
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from .database import engine, SessionLocal
from . import models

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Ethical Edge Open GRC")


# Database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Home
@app.get("/")
def home():
    return {"message": "Ethical Edge Open GRC Running"}


# -------------------------
# ORGANIZATIONS
# -------------------------
@app.get("/organizations")
def get_organizations(db: Session = Depends(get_db)):
    return db.query(models.Organization).all()


@app.post("/organizations")
def add_organization(name: str, industry: str, db: Session = Depends(get_db)):
    org = models.Organization(name=name, industry=industry)
    db.add(org)
    db.commit()
    db.refresh(org)
    return org


# -------------------------
# RISKS
# -------------------------
@app.get("/risks")
def get_risks(db: Session = Depends(get_db)):
    return db.query(models.Risk).all()


@app.post("/risks")
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
