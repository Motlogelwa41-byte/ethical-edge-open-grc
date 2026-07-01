import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from dotenv import load_dotenv

# 1. Load environment variables from .env
load_dotenv()

# 2. Validate critical infrastructure
missing_vars = []
required_vars = ["AWS_ACCESS_KEY_ID", "AWS_SECRET_ACCESS_KEY", "AWS_DEFAULT_REGION"]

for var in required_vars:
    if not os.getenv(var):
        missing_vars.append(var)

if missing_vars:
    print(f"CRITICAL: Missing environment variables: {', '.join(missing_vars)}")
    print("Please check your .env file and ensure all required AWS credentials are set.")
    sys.exit(1) # Stop the script immediately

print("Environment validated. Starting orchestration...")

# Now proceed with your imports and logic...
from app.observers.aws_observer import AWSObserver
# ... rest of your code

# PROPOSED ADDITION TO orchestrator.py

def run_compliance_gap_analysis(framework_data, audit_logs):
    """
    Compares the requirements in framework_data (from JSON) 
    against the actual evidence in audit_logs (from DB).
    """
    results = []
    
    for control in framework_data['controls']:
        # Check if the control ID exists in our audit logs
        match = next((log for log in audit_logs if log['control_id'] == control['id']), None)
        
        status = "COMPLIANT" if match and match['status'] == 'verified' else "NON-COMPLIANT"
        
        results.append({
            "control_id": control['id'],
            "description": control['description'],
            "status": status,
            "evidence_path": match['file_path'] if match else None
        })
    
    return results

# This list would then be passed to your dashboard.py to render the UI

# =====================================================================
# UNICEF CHILD-CENTERED RESILIENCE SCORING PIPELINE
# =====================================================================

def calculate_facility_preparedness_score(payload_data: dict) -> dict:
    """
    Calculates the Child-Centered Facility Preparedness Score for UNICEF criteria.
    Accepts raw data dictionary (e.g., from dummy_intake.json).
    """
    try:
        facility_name = payload_data.get("facility_name", "Unknown Facility")
        facility_type = payload_data.get("facility_type", "").lower()
        total_enrollment = payload_data.get("total_enrollment", 0)
        proximity_to_flood = payload_data.get("proximity_to_flood_zone_meters", 9999.0)
        hazard_score = payload_data.get("current_hazard_severity_score", 0.0)

        vulnerability_modifier = 0.0
        
        # Apply facility-specific metrics from your JSON framework pillars
        if facility_type == "school":
            if payload_data.get("missing_active_cooling"): vulnerability_modifier += 0.3
            if payload_data.get("missing_clean_water_reserve"): vulnerability_modifier += 0.4
            if payload_data.get("missing_offgrid_power_backup"): vulnerability_modifier += 0.2
        elif facility_type == "clinic":
            if payload_data.get("missing_active_cooling"): vulnerability_modifier += 0.5
            if payload_data.get("missing_clean_water_reserve"): vulnerability_modifier += 0.4
            if payload_data.get("missing_offgrid_power_backup"): vulnerability_modifier += 0.4
            if payload_data.get("cold_chain_vaccine_storage_exposed"): vulnerability_modifier += 0.6
        else:
            return {"status": "failed", "error": "Invalid facility_type. Must be 'school' or 'clinic'."}

        # Proximity to hazard increase
        if proximity_to_flood < 500:
            vulnerability_modifier += 0.3

        # Compute combined risk score capped at 1.0
        combined_risk_score = min(1.0, hazard_score * (1.0 + vulnerability_modifier))

        # Map to escalation matrix rules
        if combined_risk_score >= 0.7:
            classification = "critical_escalation"
            color_code = "#FF0000"
            action_window = "2 hours"
            targets = ["Facility_Head", "District_Authority", "Ministry_SADC_Dashboard"]
        elif combined_risk_score >= 0.4:
            classification = "medium_monitoring"
            color_code = "#FFA500"
            action_window = "24 hours"
            targets = ["Facility_Head", "Local_GRC_Auditor"]
        else:
            classification = "stable_baseline"
            color_code = "#008000"
            action_window = "168 hours"
            targets = ["Internal_Log_Only"]

        return {
            "facility_name": facility_name,
            "facility_type": facility_type,
            "impacted_population_count": total_enrollment,
            "metrics": {
                "infrastructure_vulnerability_modifier": round(vulnerability_modifier, 2),
                "combined_risk_score": round(combined_risk_score, 2)
            },
            "governance_action": {
                "classification": classification,
                "color_code": color_code,
                "required_action_window": action_window,
                "notification_targets": targets
            }
        }

    except Exception as e:
        return {"status": "failed", "error": str(e)}
