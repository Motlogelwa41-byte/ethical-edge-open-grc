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
st.dataframe(gates.style.applymap(lambda x: 'background-color: #d4edda' if x == 'PASS' else 'backg
