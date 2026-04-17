from enum import Enum

class RiskTreatment(str, Enum):
    TERMINATE = "Terminate"
    TRANSFER = "Transfer"
    TREAT = "Treat"
    TOLERATE = "Tolerate"

class RiskEngine:
    """
    Logic engine for identifying, analyzing, and treating risks.
    """
    
    @staticmethod
    def calculate_score(likelihood: int, impact: int) -> int:
        """
        Calculates a risk score: Likelihood (1-5) * Impact (1-5).
        Result is between 1 and 25.
        """
        if not (1 <= likelihood <= 5) or not (1 <= impact <= 5):
            raise ValueError("Scores must be between 1 and 5")
        return likelihood * impact

    @staticmethod
    def suggest_treatment(score: int) -> RiskTreatment:
        """
        Provides a recommended strategy based on the risk score.
        """
        if score >= 20:
            return RiskTreatment.TERMINATE  # Critical Risk: Walk away
        elif 12 <= score < 20:
            return RiskTreatment.TREAT      # High Risk: Implement controls/firewalls
        elif 5 <= score < 12:
            return RiskTreatment.TRANSFER   # Medium Risk: Get insurance/outsource
        else:
            return RiskTreatment.TOLERATE   # Low Risk: Accept and monitor

    @staticmethod
    def get_risk_level(score: int) -> str:
        if score >= 20: return "CRITICAL"
        if score >= 12: return "HIGH"
        if score >= 5:  return "MEDIUM"
        return "LOW"
