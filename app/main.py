import os
from flask import Flask, request, jsonify, render_template
from sqlalchemy.orm import Session
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage
import PyPDF2

# Import your GRC modules
from . import models, database
from .risk import RiskEngine
from .vetting_logic import evaluate_bdpa_compliance, get_compliance_status
2. Replace the Risk Register Route
Find your @app.get("/risk-register/") blocks (you have two) and delete them both. Replace them with this Flask-compatible version:

Python
@app.route('/api/v1/risk-register', methods=['GET'])
def get_risk_register():
    db = database.SessionLocal() # Get DB session for Flask
    try:
        risks = db.query(models.Risk).order_by(models.Risk.created_at.desc()).all()
        if not risks:
            return jsonify({"message": "No risks identified yet. Your radar is clear!"})
        
        # Convert SQLAlchemy objects to a list of dictionaries for JSON
        risk_list = []
        for r in risks:
            risk_list.append({
                "id": r.id,
                "title": r.title,
                "score": r.score,
                "level": r.risk_level,
                "strategy": r.treatment
            })
        return jsonify({"total_risks_monitored": len(risk_list), "risks": risk_list})
    finally:
        db.close()
