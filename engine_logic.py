import json
import os

class CognitiveGRCEngine:
    def __init__(self, risk_appetite=12):
        """
        risk_appetite: The threshold for 'Unacceptable' risk. 
        Calibrated for Ethical Edge at 12 (High-Medium boundary).
        """
        self.risk_appetite = risk_appetite
        # Points to data/king_v_checklist.json relative to this file
        self.checklist_path = os.path.join(os.path.dirname(__file__), 'data', 'king_v_checklist.json')

    def _get_governance_advice(self):
        """Internal helper to pull King V principles."""
        try:
            if os.path.exists(self.checklist_path):
                with open(self.checklist_path, 'r') as f:
                    data = json.load(f)
                    return data[0] if data else "No principles found."
            return "King V checklist file missing from data folder."
        except Exception as e:
            return f"Error loading governance data: {str(e)}"

    def assess_risk(self, impact, likelihood, control_effectiveness):
        # 1. Calculate Inherent Risk (Raw threat)
        inherent_risk = impact * likelihood
        
        # 2. Apply Control Effectiveness (0.0 to 1.0)
        # 1.0 means controls are 100% effective.
        residual_risk = inherent_risk * (1 - control_effectiveness)
        
        # 3. Determine Status based on Ethical Edge Calibration
        if residual_risk > self.risk_appetite:
            status = "🚨 CRITICAL: Board-Level Escalation"
            action = "Immediate mitigation or transfer required."
        elif residual_risk > (self.risk_appetite * 0.6):
            status = "⚠️ WARNING: Management Attention"
            action = "Active monitoring and control improvement."
        else:
            status = "✅ ACCEPTABLE: Monitor Locally"
            action = "Risk is within appetite."

        # 4. Integrate Cognitive Governance Mapping
        advice = self._get_governance_advice()

        return {
            "inherent_risk": inherent_risk,
            "residual_risk": round(residual_risk, 2),
            "status": status,
            "recommended_action": action,
            "governance_mapping": advice
        }
        
