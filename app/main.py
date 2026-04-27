from flask import Flask, request, jsonify
from engine_logic import CognitiveGRCEngine

app = Flask(__name__)

@app.route('/api/risk/evaluate', methods=['POST'])
def evaluate_risk():
    data = request.json
    
    # 1. Initialize engine (In future, fetch appetite from user profile)
    engine = CognitiveGRCEngine(risk_appetite=data.get('appetite', 15))
    
    # 2. Run the math
    result = engine.assess_risk(
        impact=data['impact'],
        likelihood=data['likelihood'],
        control_effectiveness=data['control_effectiveness']
    )
    
    # 3. Return as JSON for the React/JS frontend to display
    return jsonify(result)
from engine_logic import calculate_risk_score, check_alignment
import os
from flask import Flask, request, jsonify, render_template
from sqlalchemy.orm import Session
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage
import PyPDF2

# Import your local GRC modules
from . import models, database
from .risk import RiskEngine
from .vetting_logic import evaluate_bdpa_compliance, get_compliance_status

# Load environment variables
load_dotenv()

models.Base.metadata.create_all(bind=database.engine)

app = Flask(__name__)

# --- CONFIGURATION ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_PATH = os.path.normpath(os.path.join(BASE_DIR, "..", "uploads"))
app.config['UPLOAD_FOLDER'] = UPLOAD_PATH

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

# --- G: GOVERNANCE & VETTING ENDPOINTS ---

@app.route('/')
def dashboard():
    """Renders the main GRC Dashboard UI."""
    return render_template('dashboard.html')

@app.route('/api/v1/run-vetting', methods=['POST'])
def run_vetting():
    """
    Governance Pillar: Evaluates a vendor against BDPA standards.
    If score is low, it automatically triggers a Risk entry.
    """
    data = request.json
    vendor_name = data.get("vendor_name", "Unknown Vendor")
    answers = data.get("answers", {})

    db = database.SessionLocal()
    try:
        # Pass 'db' to the logic so it can auto-save risks
        score = evaluate_bdpa_compliance(answers, vendor_name, db)
        status = get_compliance_status(score)
        
        return jsonify({
            "vendor": vendor_name,
            "compliance_score": score,
            "status": status,
            "message": "Vetting complete. Low scores are auto-logged to Risk Register."
        })
    finally:
        db.close()

# --- R: RISK MANAGEMENT ENDPOINTS ---

@app.route('/api/v1/risk-register', methods=['GET'])
def get_risk_register():
    """
    Risk Pillar: Retrieves all identified risks from the database.
    This is your 'Radar Screen'.
    """
    db = database.SessionLocal()
    try:
        risks = db.query(models.Risk).order_by(models.Risk.created_at.desc()).all()
        
        # Format for JSON output
        results = []
        for r in risks:
            results.append({
                "id": r.id,
                "title": r.title,
                "level": r.risk_level,
                "score": r.score,
                "strategy": r.treatment,
                "date": r.created_at.strftime("%Y-%m-%d")
            })
        return jsonify({"total_risks": len(results), "risks": results})
    finally:
        db.close()

@app.route('/api/v1/assess-risk', methods=['POST'])
def manual_risk_entry():
    """Allows manual entry of a risk (e.g., from an audit finding)."""
    data = request.json
    db = database.SessionLocal()
    try:
        score = RiskEngine.calculate_score(data['likelihood'], data['impact'])
        new_risk = models.Risk(
            title=data['title'],
            description=data.get('description', ''),
            likelihood=data['likelihood'],
            impact=data['impact'],
            score=score,
            treatment=RiskEngine.suggest_treatment(score),
            risk_level=RiskEngine.get_risk_level(score)
        )
        db.add(new_risk)
        db.commit()
        return jsonify({"status": "success", "message": "Manual risk logged."})
    finally:
        db.close()

# --- AI AUDITOR (AI INTEGRATION) ---

@app.route('/api/v1/analyze-report', methods=['POST'])
def analyze_report():
    """Uses AI to audit a PDF report against King V Principles."""
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    
    file = request.files['file']
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(file_path)

    # Extract PDF Text
    reader = PyPDF2.PdfReader(file_path)
    text = "".join([page.extract_text() for page in reader.pages])

    # AI Analysis
    chat = ChatOpenAI(model="gpt-4-turbo", temperature=0)
    query = f"Analyze this report for King V Governance compliance: {text[:4000]}"
    response = chat.invoke([HumanMessage(content=query)])
    
    return jsonify({"analysis": response.content})

import json
from fastapi import FastAPI, HTTPException
from pathlib import Path

app = FastAPI()

# Path to your JSON data
CHECKLIST_PATH = Path("data/king_v_checklist.json")

@app.get("/api/checklist/king-v")
async def get_king_v_checklist():
    if not CHECKLIST_PATH.exists():
        raise HTTPException(status_code=404, detail="Checklist file not found")
    
    with open(CHECKLIST_PATH, "r") as f:
        data = json.load(f)
    return data


   if __name__ == '__main__':
    # Setting host to '0.0.0.0' allows it to be seen by your browser properly
    app.run(host='0.0.0.0', port=5000, debug=True)

@app.post("/api/checklist/save")
async def save_king_v_assessment(data: dict):
    # For now, we will print to console. Later, we'll save to the database.
    print(f"Received Assessment: {data}")
    return {"message": "Success", "received": data}

from sqlalchemy import create_engine, Column, Integer, String, Boolean, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# Database Connection
DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Define the Table
class AssessmentResult(Base):
    __tablename__ = "assessment_results"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String) # For future user tracking
    data = Column(JSON)

# Create the table
Base.metadata.create_all(bind=engine)

@app.post("/api/checklist/save")
async def save_king_v_assessment(payload: dict):
    db = SessionLocal()
    try:
        new_result = AssessmentResult(data=payload["assessment"])
        db.add(new_result)
        db.commit()
        return {"status": "saved_to_db"}
    except Exception as e:
        db.rollback()
        return {"error": str(e)}
    finally:
        db.close()
