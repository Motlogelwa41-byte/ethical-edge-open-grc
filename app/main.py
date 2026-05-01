from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from . import models, database

app = FastAPI()

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/organizations/")
def create_org(name: str, reg_number: str, db: Session = Depends(get_db)):
    new_org = models.Organization(name=name, reg_number=reg_number)
    db.add(new_org)
    db.commit()
    db.refresh(new_org)
    return new_org

@app.get("/frameworks/")
def list_frameworks(db: Session = Depends(get_db)):
    return db.query(models.Framework).all()
import os
import json
from flask import Flask, request, jsonify, render_template
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage
import PyPDF2

# Import local modules
from engine_logic import CognitiveGRCEngine
import models
import database

# Load environment variables
load_dotenv()

# Initialize Database Tables
models.Base.metadata.create_all(bind=database.engine)

app = Flask(__name__)

# --- CONFIGURATION ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
app.config['UPLOAD_FOLDER'] = os.path.normpath(os.path.join(BASE_DIR, "..", "uploads"))
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

# --- 1. GOVERNANCE: Dashboard & King V ---

@app.route('/')
def dashboard():
    return render_template('dashboard.html')

@app.route('/api/checklist/king-v', methods=['GET'])
def get_king_v_checklist():
    path = os.path.join(BASE_DIR, "..", "data", "king_v_checklist.json")
    if not os.path.exists(path):
        return jsonify({"error": "Checklist not found"}), 404
    with open(path, "r") as f:
        return jsonify(json.load(f))

# --- 2. RISK: Cognitive Engine Integration ---

@app.route('/api/risk/evaluate', methods=['POST'])
def evaluate_risk():
    """
    The 'Cognitive Engine' endpoint.
    Calculates residual risk and saves to the DB.
    """
    data = request.json
    db = database.SessionLocal()
    
    try:
        # 1. Math via Cognitive Engine
        engine = CognitiveGRCEngine(risk_appetite=data.get('appetite', 15))
        result = engine.assess_risk(
            impact=data['impact'],
            likelihood=data['likelihood'],
            control_effectiveness=data['control_effectiveness']
        )
        
        # 2. Save to Database (using your models.Risk)
        new_risk = models.Risk(
            title=data.get('title', 'Manual Assessment'),
            category=data.get('category', 'Operational'),
            impact=data['impact'],
            likelihood=data['likelihood'],
            score=result['inherent_risk'],
            residual_score=result['residual_risk'],
            status=result['status']
        )
        db.add(new_risk)
        db.commit()
        
        return jsonify(result)
    except Exception as e:
        db.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        db.close()

# --- 3. COMPLIANCE: AI Auditor ---

@app.route('/api/v1/analyze-report', methods=['POST'])
def analyze_report():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    
    file = request.files['file']
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(file_path)

    # Extract Text
    reader = PyPDF2.PdfReader(file_path)
    text = "".join([page.extract_text() for page in reader.pages])

    # AI Analysis against King V
    chat = ChatOpenAI(model="gpt-4-turbo", temperature=0)
    query = f"Analyze this report for King V Governance compliance in Botswana: {text[:4000]}"
    response = chat.invoke([HumanMessage(content=query)])
    
    return jsonify({"analysis": response.content})

# Ensure these lines are flush against the left margin
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
