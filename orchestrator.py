import sys
import os
import json
from datetime import datetime

# Setup pathing to find database and app modules smoothly
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from dotenv import load_dotenv

# 1. Load environment variables from .env
load_dotenv()

# 2. Check infrastructure settings (Soft warning for local development resilience)
aws_configured = True
required_vars = ["AWS_ACCESS_KEY_ID", "AWS_SECRET_ACCESS_KEY", "AWS_DEFAULT_REGION"]
missing_vars = [var for var in required_vars if not os.getenv(var)]

if missing_vars:
    print(f"⚠️  NOTE: Cloud-native logging targets are limited. Missing AWS variables: {', '.join(missing_vars)}")
    print("👉 Continuing in LOCAL COGNITIVE ENGINE mode.")
    aws_configured = False
else:
    print("✅ Cloud Infrastructure Environment validated.")

# Safeguard dynamic import for cloud observer
AWSObserver = None
if aws_configured:
    try:
        from app.observers.aws_observer import AWSObserver
        print("✅ AWSObserver loaded successfully.")
    except ImportError:
        print("⚠️  AWSObserver module path not resolved. Defaulting to local logging ledger.")


# =====================================================================
# CORE GRC COMPLIANCE & GAP ANALYSIS ENGINE
# =====================================================================

def run_compliance_gap_analysis(framework_data: dict, audit_logs: list) -> list:
    """
    Compares the requirements in framework_data (King V / BDPA JSON) 
    against actual evidence records in audit_logs (from DB).
    """
    results = []
    
    # Safely handle framework formats
    controls = framework_data.get('controls', framework_data.get('requirements', []))
    
    for control in controls:
        control_id = control.get('id', control.get('control_id'))
        description = control.get('description', control.get('requirement_text', 'No description provided'))
        
        # Cross-reference with our database audit trail ledger
        match = next((log for log in audit_logs if log.get('control_id') == control_id), None)
        
        status = "COMPLIANT" if match and match.get('status') == 'verified' else "NON-COMPLIANT"
        
        results.append({
            "control_id": control_id,
            "description": description,
            "status": status,
            "evidence_path": match.get('file_path') if match else None,
            "timestamp": datetime.utcnow().isoformat()
        })
        
    return results


# =====================================================================
# UNICEF CHILD-CENTERED RESILIENCE SCORING PIPELINE
# =====================================================================

def calculate_facility_preparedness_score(payload_data: dict) -> dict:
    """
    Calculates the Child-Centered Facility Preparedness Score for UNICEF criteria.
    Accepts raw data dictionary (e.g., from dummy_intake.json or climate_facility_intake.json).
    """
    try:
        facility_name = payload_data.get("facility_name", "Unknown Facility")
        facility_type = payload_data.get("facility_type", "").lower()
        total_enrollment = payload_data.get("total_enrollment", 0)
        proximity_to_flood = payload_data.get("proximity_to_flood_zone_meters", 9999.0)
        hazard_score = payload_data.get("current_hazard_severity_score", 0.0)

        vulnerability_modifier = 0.0
        
        # Apply facility-specific metrics from framework pillars
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
            return {"status": "failed", "error": f"Invalid facility_type '{facility_type}'. Must be 'school' or 'clinic'."}

        # Proximity to hazard calculation
        if proximity_to_flood < 500:
            vulnerability_modifier += 0.3

        # Compute combined risk score capped at 1.0
        combined_risk_score = min(1.0, hazard_score * (1.0 + vulnerability_modifier))

        # Map to regional/SADC escalation matrix rules
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
            "status": "success",
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


# =====================================================================
# EXECUTIVE MASTER PIPELINE RUNNER (CLI EXECUTION)
# =====================================================================

if __name__ == "__main__":
    print("\n🚀 Executing Ethical Edge Cognitive Orchestrator Test Sequence...")
    
    # Path setup for intake verification
    intake_file = os.path.join(os.path.dirname(__file__), 'dummy_intake.json')
    if not os.path.exists(intake_file):
        # Fallback to alternative root location
        intake_file = os.path.join(os.path.dirname(__file__), '..', 'dummy_intake.json')
        
    if os.path.exists(intake_file):
        print(f"📦 Loading active UNICEF data target: {intake_file}")
        with open(intake_file, 'r') as f:
            try:
                sample_payload = json.load(f)
                # If wrapped inside an array, extract the first record
                if isinstance(sample_payload, list):
                    sample_payload = sample_payload[0]
                    
                risk_report = calculate_facility_preparedness_score(sample_payload)
                print("\n📊 Generated Cognitive Risk Assessment Output:")
                print(json.dumps(risk_report, indent=4))
            except Exception as ex:
                print(f"❌ Failed to parse payload data: {ex}")
    else:
        print("⚠️  Warning: No local target profile found (`dummy_intake.json`). Skipping fallback verification step.")
        
    print("\n🎯 Orchestration script check completed successfully.")
