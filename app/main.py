from fastapi import FastAPI, Depends, Body, HTTPException
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

# FIX 1: Added 'description' to the model so the API knows to accept it
class RiskRequest(BaseModel):
    title: str
    description: str  # <--- THIS WAS MISSING
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
    try:
        engine = engine_logic.CognitiveGRCEngine()
        
        # FIX 2: Now 'data.description' will actually work!
        assessment = engine.assess_risk(
            title=data.title,
            description=data.description,
            impact=data.impact,
            likelihood=data.likelihood,
            control_effectiveness=data.control_effectiveness
        )
        
        # Save to DB - added a .get() safety check for the mapping name
        mapping_name = assessment.get('governance_mapping', {}).get('name', 'General Governance')
        
        new_risk = models.Risk(
            title=data.title,
            description=f"Status: {assessment['status']} | Principle: {mapping_name}"
        )
        db.add(new_risk)
        db.commit()
        
        return assessment
    except Exception as e:
        # This helps us see the REAL error in the browser if it fails again
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/frameworks")
def list_frameworks(db: Session = Depends(get_db)):
    return db.query(models.Framework).all()

@app.get("/risks/summary")
def get_risk_summary(db: Session = Depends(get_db)):
    # 1. Fetch all risks from the database
    all_risks = db.query(models.Risk).all()
    total = len(all_risks)
    
    if total == 0:
        return {"message": "No risks recorded yet. Start by evaluating a risk!"}

    # 2. Categorize the risks based on your engine's status labels
    critical = [r for r in all_risks if "🚨 CRITICAL" in r.description]
    warning = [r for r in all_risks if "⚠️ WARNING" in r.description]
    acceptable = [r for r in all_risks if "✅ ACCEPTABLE" in r.description]

    # 3. Calculate the Governance Health Index
    # (High percentage = Fewer critical risks)
    health_score = round(((total - len(critical)) / total) * 100, 2)

    return {
        "organization_health_index": f"{health_score}%",
        "total_risks_monitored": total,
        "critical_count": len(critical),
        "warning_count": len(warning),
        "acceptable_count": len(acceptable),
        "detailed_view": all_risks
    }
