def collect(self):
    # logic to get data...
    return [
        {
            "gate_id": "GITHUB_MFA_ENABLED",
            "is_passed": True, 
            "evidence_snapshot": {"mfa_status": "active"} 
        }
    ]
