class CognitiveGRCEngine:
    def __init__(self, risk_appetite=12):
        """
        risk_appetite: The threshold above which a risk is considered 'Unacceptable'.
        For Ethical Edge, we set this to 12 (High-Medium boundary).
        """
        self.risk_appetite = risk_appetite

    def assess_risk(self, impact, likelihood, control_effectiveness):
        # 1. Calculate Inherent Risk (Raw threat)
        inherent_risk = impact * likelihood
        
        # 2. Apply Control Effectiveness (0.0 to 1.0)
        # 1.0 means controls are 100% effective, reducing risk to near zero.
        residual_risk = inherent_risk * (1 - control_effectiveness)
        
        # 3. Determine Status based on your Calibration
        if residual_risk > self.risk_appetite:
            status = "🚨 CRITICAL: Board-Level Escalation"
            action = "Immediate mitigation or transfer required."
        elif residual_risk > (self.risk_appetite * 0.6):
            status = "⚠️ WARNING: Management Attention"
            action = "Active monitoring and control improvement."
        else:
            status = "✅ ACCEPTABLE: Monitor Locally"
            action = "Risk is within appetite."

        return {
            "inherent_risk": inherent_risk,
            "residual_risk": round(residual_risk, 2),
            "status": status,
            "recommended_action": action
        }
import json
import os

class CognitiveGRCEngine:
    def __init__(self, risk_appetite=12):
        self.risk_appetite = risk_appetite
        # Load the King V data
        self.checklist_path = os.path.join(os.path.dirname(__file__), 'data', 'king_v_checklist.json')

    def get_governance_advice(self):
        try:
            with open(self.checklist_path, 'r') as f:
                data = json.load(f)
                # For now, return the first principle as a sample
                return data[0] if data else "No principles found."
        except Exception:
            return "King V data unavailable."

    def assess_risk(self, impact, likelihood, control_effectiveness):
        inherent_risk = impact * likelihood
        residual_risk = inherent_risk * (1 - control_effectiveness)
        
        # Determine status
        if residual_risk > self.risk_appetite:
            status = "🚨 CRITICAL: Board-Level Escalation"
            action = "Immediate mitigation or transfer required."
        elif residual_risk > (self.risk_appetite * 0.6):
            status = "⚠️ WARNING: Management Attention"
            action = "Active monitoring."
        else:
            status = "✅ ACCEPTABLE: Monitor Locally"
            action = "Risk is within appetite."

        # Add the 'Cognitive' King V mapping
        advice = self.get_governance_advice()

        return {
            "inherent_risk": inherent_risk,
            "residual_risk": round(residual_risk, 2),
            "status": status,
            "recommended_action": action,
            "governance_mapping": advice
        }
