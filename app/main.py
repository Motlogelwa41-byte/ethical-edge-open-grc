from .vetting_logic import vetter
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
def vet_ngo(
    name: str, 
    has_audit: bool, 
    public_report: bool, 
    db: Session = Depends(database.get_db)
):
    # 1. Run the data through the Intelligence Engine
    results = vetter.assess_organization({
        "has_audit_committee": has_audit,
        "public_annual_report": public_report
    })
    
    # 2. Map the results to your Database Model
    new_ngo = models.NGOProfile(
        name=name,
        trust_score=results["score"],
        compliance_status=results["status"]
    )
    
    # 3. Commit to the permanent Audit Log
    db.add(new_ngo)
    db.commit()
    db.refresh(new_ngo)
    
    return {
        "message": "Vetting Complete",
        "entity": name,
        "integrity_score": results["score"],
        "findings": results["findings"]
