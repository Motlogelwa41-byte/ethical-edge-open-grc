import json

def generate_gap_report(intake_data, checklist_file):
    # Load requirements
    with open(checklist_file, 'r') as f:
        checklist = json.load(f)
    
    gaps = []
    
    # Map your intake keys to the checklist IDs
    # This is where your "Consultant Logic" lives
    mapping = {
        "has_privacy_policy": "SEC-52",
        "has_ropa": "SEC-60",
        "has_breach_proc": "SEC-62",
        "has_dpia": "SEC-66",
        "has_dsar_log": "SEC-42",
        "has_cross_border_assessment": "SEC-80"
    }
    
    print(f"--- GAP ANALYSIS FOR {intake_data['client_name']} ---")
    
    for key, status in intake_data['current_status'].items():
        if status == False:  # If the client said 'False' to having the control
            control_id = mapping.get(key)
            # Find the requirement in the checklist
            requirement = next((c for c in checklist['controls'] if c['id'] == control_id), None)
            
            if requirement and requirement['required']:
                gaps.append(f"[CRITICAL] Missing {requirement['domain']}: {requirement['requirement']}")
            elif requirement:
                gaps.append(f"[ADVISORY] Missing {requirement['domain']}: {requirement['requirement']}")
    
    return gaps

# --- Example Usage ---
client_intake = {
    "client_name": "Gaborone Retailers Ltd",
    "current_status": {
        "has_privacy_policy": False, # Missing
        "has_ropa": True,
        "has_breach_proc": False,    # Missing
        "has_dpia": False,
        "has_dsar_log": True,
        "has_cross_border_assessment": False
    }
}

gaps = generate_gap_report(client_intake, 'dpa_checklist.json')
for gap in gaps:
    print(gap)
