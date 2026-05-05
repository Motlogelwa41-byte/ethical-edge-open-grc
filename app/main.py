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

from fastapi import Body
import sys
import os

# This ensures Python can see engine_logic.py in the root folder
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import engine_logic

@app.post("/risks/evaluate")
def evaluate_risk(
    title: str = Body(...), 
    description: str = Body(...), 
    db: Session = Depends(get_db)
):
    # 1. Run the "Cognitive" assessment from your engine_logic.py
    # This simulates the automated audit logic you've been building
    assessment = engine_logic.evaluate_compliance_gap(description)
    
    # 2. Save the risk to your database
    new_risk = models.Risk(
        title=title,
        description=description
    )
    db.add(new_risk)
    db.commit()
    db.refresh(new_risk)
    
    return {
        "risk_id": new_risk.id,
        "analysis": assessment,
        "message": "Risk analyzed and indexed against GRC standards"
    }

