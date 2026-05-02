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

@app.get("/")
def home():
    return {"message": "Ethical Edge Open GRC Running"}

@app.get("/risks")
def get_risks(db: Session = Depends(get_db)):
    return db.query(models.Risk).all()

@app.post("/risks")
def add_risk(
    title: str,
    description: str,
    likelihood: int,
    impact: int,
    db: Session = Depends(get_db)
):
    score = likelihood * impact

    if score <= 5:
        level = "Low"
    elif score <= 12:
        level = "Medium"
    else:
        level = "High"

    risk = models.Risk(
        title=title,
        description=description,
        likelihood=likelihood,
        impact=impact,
        score=score,
        level=level
    )

    db.add(risk)
    db.commit()
    db.refresh(risk)

    return risk
