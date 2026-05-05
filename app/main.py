from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from . import models, database

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(title="Ethical Edge Open GRC")

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def read_root():
    return {"message": "Ethical Edge API is LIVE", "version": "1.0"}

@app.get("/frameworks")
def list_frameworks(db: Session = Depends(get_db)):
    return db.query(models.Framework).all()

@app.get("/risks")
def get_risks(db: Session = Depends(get_db)):
    return db.query(models.Risk).all()

@app.post("/risks")
def add_risk(
    category: str,
    description: str,
    likelihood_score: int,
    impact_score: int,
    db: Session = Depends(get_db)
):
    risk = models.Risk(
        category=category,
        description=description,
        likelihood_score=likelihood_score,
        impact_score=impact_score
    )

    db.add(risk)
    db.commit()
    db.refresh(risk)
    return risk
