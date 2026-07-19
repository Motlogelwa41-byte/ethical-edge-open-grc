import os
import sys
import streamlit as st
import pandas as pd
from sqlalchemy import create_engine

# Ensure system paths align to root context
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

st.set_page_config(page_title="Ethical Edge GRC Engine", layout="wide", page_icon="🛡️")

st.title("🛡️ Ethical Edge: Open GRC Dashboard")
st.markdown("### Continuous Compliance & Cognitive Climate Resilience Monitoring")

# 1. Establish Secure Database Connection (Using the Docker Stack URL)
DATABASE_URL = os.getenv(
    "DATABASE_URL", 
    "postgresql://grc_admin:SuperSecurePassword2026!@localhost:5432/ethical_edge_grc_pool"
)

@st.cache_data(ttl=5)  # Auto-refresh cache every 5 seconds for live telemetry
def fetch_grc_dashboard_data():
    engine = create_engine(DATABASE_URL)
    try:
        # Query our production metrics tracking tables
        query = """
            SELECT 
                f.control_reference, 
                f.control_name, 
                f.framework, 
                f.status, 
                r.tenant_id,
                r.timestamp
            FROM control_findings f
            JOIN audit_runs r ON f.audit_run_id = r.id
            ORDER BY r.timestamp DESC;
        """
        df = pd.read_sql(query, engine)
        return df
    except Exception as e:
        st.error(f"Database Engine connection waiting... Details: {e}")
        return pd.DataFrame()

# Fetch Data
findings_df = fetch_grc_dashboard_data()

if not findings_df.empty:
    # 2. Executive GRC Metrics Processing
    total_controls = len(findings_df)
    passed_controls = len(findings_df[findings_df['status'].isin(['PASSED', 'COMPLIANT', 'verified'])])
    
    compliance_score = (passed_controls / total_controls) * 100 if total_controls > 0 else 0.0

    # Layout Key Metrics Highlighting
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("SADC Regional GRC Attainment Score", f"{compliance_score:.1f}%")
    with col2:
        st.metric("Total Monitored Control Gates", total_controls)
    with col3:
        st.metric("Active Sub-recipient Tenants", findings_df['tenant_id'].nunique())

    st.markdown("---")

    # 3. Dedicated Cognitive Climate Resilience View (UNICEF CCRI-V1 Section)
    st.subheader("🌍 UNICEF Climate-Resilient Infrastructure Safeguards")
    climate_df = findings_df[findings_df['framework'] == 'UNICEF_Child_Safeguarding']
    
    if not climate_df.empty:
        st.dataframe(climate_df, use_container_width=True)
    else:
        st.info("No active climate telemetry incoming yet. Run the master pipeline to inject data.")

    # 4. Master Core GRC Frameworks Overview (King V / BDPA Data Protection)
    st.subheader("📑 Master Control Log Matrix")
    
    def highlight_status(val):
        if val in ['PASSED', 'COMPLIANT', 'verified']:
            return 'background-color: #d4edda; color: #155724'
        return 'background-color: #f8d7da; color: #721c24'

    # Apply responsive styling matrix
    st.dataframe(
        findings_df.style.applymap(highlight_status, subset=['status']),
        use_container_width=True
    )

else:
    st.warning("⚡ Waiting for the edge engine ledger to compile active audit data logs...")
    st.info("👉 Try spinning up your docker infrastructure environment or execute: `python test_master_pipeline.py` to seed baseline metrics.")
