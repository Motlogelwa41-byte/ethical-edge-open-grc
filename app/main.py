from fastapi import FastAPI, Depends, Body
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
import sys
import os

# Ensure engine_logic is discoverable
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import engine_logic
from . import models, database

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(title="Ethical Edge Open GRC")

# Data structure for incoming risk assessments
class RiskRequest(BaseModel):
    title: str
    impact: int = Field(..., ge=1, le=5)
    likelihood: int = Field(..., ge=1, le=5)
    control_effectiveness: float = Field(..., ge=0, le=1)

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def read_root():
    return {"message": "Ethical Edge API is LIVE", "version": "1.0"}

@app.post("/risks/evaluate")
def evaluate_risk(data: RiskRequest, db: Session = Depends(get_db)):
    # 1. Initialize Engine
    engine = engine_logic.CognitiveGRCEngine()
    
    # 2. Execute Risk Math
    assessment = engine.assess_risk(data.impact, data.likelihood, data.control_effectiveness)
    
    # 3. Persist to Database
    new_risk = models.Risk(
        title=data.title,
        description=f"Status: {assessment['status']} | Residual Risk: {assessment['residual_risk']}"
    )
    db.add(new_risk)
    db.commit()
    db.refresh(new_risk)
    
    return {
        "risk_id": new_risk.id,
        "analysis": assessment,
        "message": "Cognitive assessment complete."
    }

@app.get("/frameworks")
def list_frameworks(db: Session = Depends(get_db)):
    return db.query(models.Framework).all()
