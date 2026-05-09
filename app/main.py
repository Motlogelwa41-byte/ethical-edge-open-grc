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

@app.post("/risks")
def add_and_evaluate_risk(
    title: str = Body(...),
    impact: int = Body(..., ge=1, le=5),
    likelihood: int = Body(..., ge=1, le=5),
    control_effectiveness: float = Body(..., ge=0, le=1),
    db: Session = Depends(get_db)
):
    # 1. Trigger the Cognitive Engine
    engine = engine_logic.CognitiveGRCEngine()
    assessment = engine.assess_risk(impact, likelihood, control_effectiveness)
    
    # 2. Store the risk with its automated status
    new_risk = models.Risk(
        title=title,
        description=f"Status: {assessment['status']} | Advice: {assessment['recommended_action']}"
    )
    db.add(new_risk)
    db.commit()
    db.refresh(new_risk)
    
    return {
        "risk_id": new_risk.id,
        "cognitive_analysis": assessment
    }
@app.post("/risks/evaluate")
def evaluate_risk(data: RiskEvaluation, db: Session = Depends(get_db)):
    # Then access data via data.title, data.impact, etc.
    title: str = Body(...), 
    impact: int = Body(..., ge=1, le=5), 
    likelihood: int = Body(..., ge=1, le=5), 
    control_effectiveness: float = Body(..., ge=0, le=1),
    db: Session = Depends(get_db)
):
    # 1. Initialize your Engine class
    engine = engine_logic.CognitiveGRCEngine()
    
    # 2. Run the actual math logic from your file
    assessment = engine.assess_risk(impact, likelihood, control_effectiveness)
    
    # 3. Save the risk to your database
    new_risk = models.Risk(
        title=title,
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
