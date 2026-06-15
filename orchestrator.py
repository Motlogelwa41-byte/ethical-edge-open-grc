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
