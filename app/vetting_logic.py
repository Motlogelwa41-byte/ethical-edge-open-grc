import json
import os

class VettingEngine:
    def __init__(self):
        # Load the King V principles we created earlier
        path = os.path.join(os.path.dirname(__file__), '../data/king_v_checklist.json')
        with open(path, 'r') as f:
            self.principles = json.load(f)

    def assess_organization(self, data: dict):
        """
        Input: Dictionary of NGO attributes
        Output: Detailed Compliance Report
        """
        findings = []
        score_deductions = 0
        
        # Check against Principle 3: Effective Control
        if not data.get("has_audit_committee"):
            findings.append("Missing Audit Committee (King V P3 violation)")
            score_deductions += 20
            
        # Check against Principle 4: Transparency
        if not data.get("public_annual_report"):
            findings.append("Annual Report not public (Transparency risk)")
            score_deductions += 15
            
        final_score = 100 - score_deductions
        
        return {
            "score": final_score,
            "findings": findings,
            "status": "Verified" if final_score > 70 else "Action Required"
        }

vetter = VettingEngine()
