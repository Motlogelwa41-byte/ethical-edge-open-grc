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


   if __name__ == '__main__':
    # Setting host to '0.0.0.0' allows it to be seen by your browser properly
    app.run(host='0.0.0.0', port=5000, debug=True)
