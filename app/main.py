import os
import json
from fastapi import FastAPI, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage
import PyPDF2

# Import local modules
from . import models, database
from .engine_logic import CognitiveGRCEngine

# Load environment variables
load_dotenv()

# Initialize Database Tables
models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(title="Ethical Edge Open GRC")

# Dependency to get DB session
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- 1. GOVERNANCE & FRAMEWORKS ---

@app.get("/frameworks/")
def list_frameworks(db: Session = Depends(get_db)):
    return db.query(models.Framework).all()

@app.post("/organizations/")
def create_org(name: str, reg_number: str, db: Session = Depends(get_db)):
    new_org = models.Organization(name=name, reg_number=reg_number)
    db.add(new_org)
    db.commit()
    db.refresh(new_org)
    return new_org

# --- 2. RISK: Cognitive Engine Integration ---

@app.post("/api/risk/evaluate")
def evaluate_risk(data: dict, db: Session = Depends(get_db)):
    try:
        engine = CognitiveGRCEngine(risk_appetite=data.get('appetite', 15))
        result = engine.assess_risk(
            impact=data['impact'],
            likelihood=data['likelihood'],
            control_effectiveness=data['control_effectiveness']
        )
        
        new_risk = models.Risk(
            title=data.get('title', 'Manual Assessment'),
            org_id=data.get('org_id'), # Ensure this is passed
            description=f"Score: {result['residual_risk']}"
        )
        db.add(new_risk)
        db.commit()
        return result
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

# --- 3. COMPLIANCE: AI Auditor ---

@app.post("/api/v1/analyze-report")
async def analyze_report(file: UploadFile = File(...)):
    # Extract Text from PDF
    reader = PyPDF2.PdfReader(file.file)
    text = "".join([page.extract_text() for page in reader.pages])
    
    # AI Analysis
    chat = ChatOpenAI(model="gpt-4o", temperature=0)
    query = f"Analyze this report for King V Governance compliance: {text[:4000]}"
    response = chat.invoke([HumanMessage(content=query)]) 
    
    return {"analysis": response.content}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
