import streamlit as st
import pandas as pd
from app.database.connection import SessionLocal

st.set_page_config(page_title="Ethical Edge GRC", layout="wide")

st.title("🛡️ Ethical Edge: Continuous Compliance")

# Fetch data from your database
session = SessionLocal()
gates = pd.read_sql("SELECT gate_id, requirement_text, validation_type FROM room_gates", session.bind)
session.close()

# 1. Compliance Health Metric
passed = len(gates[gates['validation_type'] == 'PASS'])
total = len(gates)
score = (passed / total) * 100 if total > 0 else 0

st.metric("Compliance Health Score", f"{score:.1f}%")

# 2. Status Visualization
st.subheader("Live Control Monitoring")
# Ensure line 23 looks like this (all on one line)
st.dataframe(gates.style.applymap(lambda x: 'background-color: #d4edda' if x == 'PASS' else 'background-color: #f8d7da'))
 from flask import Flask, jsonify
app = Flask(__name__)

@app.route('/api/room/<room_key>')
def get_room_data(room_key):
    # Retrieve the tenant ID from your environment
    tenant_id = os.getenv("TARGET_TENANT_ID")
    
    # Use the helper function we defined earlier
    data = get_dashboard_data(tenant_id)
    
    # Return as JSON so the frontend can read it
    return jsonify({"gates": data})                                 
                                  
