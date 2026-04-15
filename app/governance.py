class EthicalEdgeEngine:
    def __init__(self):
        self.version = "2.0 - Sprint Edition"

    def calculate_trust_score(self, has_audit_committee: bool, has_dpo: bool, years_active: int):
        """
        Comprehensive scoring based on King V and Botswana DPA.
        """
        score = 50.0  # Base score
        
        # King V: Effective Control (P3)
        if has_audit_committee:
            score += 25.0
            
        # Botswana DPA: Protection of Personal Info
        if has_dpo:
            score += 15.0
            
        # Stability Factor
        if years_active > 5:
            score += 10.0
            
        return min(score, 100.0)

    def get_compliance_tier(self, score):
        if score >= 85: return "High - Institutional Grade"
        if score >= 60: return "Medium - Development Grade"
        return "Low - Review Required"

# Initialize for the platform
engine = EthicalEdgeEngine()
