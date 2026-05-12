from fastapi import FastAPI, Depends, Body, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
import sys
import os

# 1. Import specialized Grant Rooms
from modules.society_research.trust_metrics import get_connectivity_trust
from modules.unicef_climate.climate_logic import get_climate_risk

# 2. Setup the Engine and Database
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import engine_logic
from . import models, database

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(title="Ethical Edge Open GRC")

class RiskRequest(BaseModel):
    title: str
    description: str
    impact: int = Field(..., ge=1, le=5)
    likelihood: int = Field(..., ge=1, le=5)
    control_effectiveness: float = Field(..., ge=0, le=1)

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- ROUTES ---

@app.get("/")
def home():
    return {
        "engine": "Ethical Edge Open GRC",
        "status": "Ready",
        "active_modules": ["Core_GRC", "UNICEF_Climate", "Society_Research"]
    }

# ROOM 1: UNICEF ($100k Grant)
@app.get("/unicef/{district}")
def unicef_hazard_check(district: str):
    data = get_climate_risk(district)
    return {
        "module": "UNICEF Climate Venture", 
        "district": district,
        "data": data
    }

# ROOM 2: INTERNET SOCIETY ($500k Grant)
@app.get("/society/{region}")
async def society_trust_check(region: str):
    try:
        data = get_connectivity_trust(region)
        if not data:
            raise HTTPException(status_code=404, detail=f"Trust metrics for '{region}' not found.")
            
        return {
            "module": "Internet Society Research",
            "region": region,
            "trust_metrics": data,
            "status": "Verified via Ethical Edge Open GRC"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Society Module Error: {str(e)}")
        
# CORE ENGINE: Risk Evaluation
@app.post("/risks/evaluate")
def evaluate_risk(data: RiskRequest, db: Session = Depends(get_db)):
    try:
        # 1. Run the Cognitive GRC Logic
        engine = engine_logic.CognitiveGRCEngine()
        assessment = engine.assess_risk(
            title=data.title,
            description=data.description,
            impact=data.impact,
            likelihood=data.likelihood,
            control_effectiveness=data.control_effectiveness
        )
        
        # 2. Extract the Governance Mapping (e.g., ISO or King IV)
        mapping_name = assessment.get('governance_mapping', {}).get('name', 'General Governance')
        
        # 3. Create the DB record matching your updated models.py
        new_risk = models.Risk(
            title=data.title,
            description=f"Status: {assessment['status']} | Principle: {mapping_name}",
            impact_score=data.impact,
            likelihood_score=data.likelihood,
            status=assessment['status']
        )
        
        # 4. Save and return
        db.add(new_risk)
        db.commit()
        return assessment
        
    except Exception as e:
        # Only error handling goes here
        raise HTTPException(status_code=500, detail=f"Engine Error: {str(e)}")

@app.get("/frameworks")
def list_frameworks(db: Session = Depends(get_db)):
    return db.query(models.Framework).all()

@app.get("/risks/summary")
def get_risk_summary(db: Session = Depends(get_db)):
    all_risks = db.query(models.Risk).all()
    total = len(all_risks)
    if total == 0:
        return {"message": "No risks recorded yet."}

    critical = [r for r in all_risks if "🚨 CRITICAL" in r.description]
    warning = [r for r in all_risks if "⚠️ WARNING" in r.description]
    acceptable = [r for r in all_risks if "✅ ACCEPTABLE" in r.description]
    health_score = round(((total - len(critical)) / total) * 100, 2)

    return {
        "organization_health_index": f"{health_score}%",
        "total_risks_monitored": total,
        "critical_count": len(critical),
        "warning_count": len(warning),
        "acceptable_count": len(acceptable)
    }
