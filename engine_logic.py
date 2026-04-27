class CognitiveGRCEngine:
    def __init__(self, risk_appetite=15):
        # The appetite can be set per client from the database
        self.risk_appetite = risk_appetite

    def assess_risk(self, impact, likelihood, control_effectiveness):
        """
        Calculates risk and returns a structured dictionary for the database/UI.
        """
        inherent_risk = impact * likelihood
        residual_risk = inherent_risk * (1 - control_effectiveness)
        
        status = "ALIGNED" if residual_risk <= self.risk_appetite else "ACTION REQUIRED"
        
        return {
            "inherent_risk": inherent_risk,
            "residual_risk": round(residual_risk, 2),
            "status": status,
            "appetite_used": self.risk_appetite
        }
