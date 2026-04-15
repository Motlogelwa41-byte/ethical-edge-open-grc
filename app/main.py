from fastapi import FastAPI, Depends, Request
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from . import models, database, governance

app = FastAPI(title="Ethical Edge GRC: Integrity Bridge")
templates = Jinja2Templates(directory="templates")

# Initialize Database
models.Base.metadata.create_all(bind=database.engine)

@app.get("/")
def read_root():
    return {"status": "Engine Online", "framework": "King V + BDPA"}

@app.get("/dashboard")
def get_dashboard(request: Request, db: Session = Depends(database.get_db)):
    # Fetch NGOs from the database
    ngos = db.query(models.NGOProfile).all()
    
    # If database is empty, we provide sample data for the demo
    if not ngos:
        ngos = [
            {"name": "Botswana Educational Fund", "trust_score": 95, "compliance_status": "Institutional Grade"},
            {"name": "SADC Youth Initiative", "trust_score": 65, "compliance_status": "Development Grade"}
        ]
        
    return templates.TemplateResponse("dashboard.html", {
        "request": request,
        "ngos": ngos
    })

@app.post("/vet-ngo/")
def vet_ngo(name: str, has_audit: bool, has_dpo: bool, years: int, db: Session = Depends(database.get_db)):
    # Calculate score using our Intelligence Layer
    score = governance.engine.calculate_trust_score(has_audit, has_dpo, years)
    tier = governance.engine.get_compliance_tier(score)
    
    # Save to Integrity Registry
    new_ngo = models.NGOProfile(
        name=name,
        trust_score=score,
        compliance_status=tier
    )
    db.add(new_ngo)
    db.commit()
    
    return {"name": name, "trust_score": score, "tier": tier}
