"""
Child Vulnerability Index (CVI) Engine

Calculates climate-related vulnerability for
child-centric infrastructure.
"""


class CVIEngine:

    ENVIRONMENTAL_WEIGHT = 0.50
    INFRASTRUCTURE_WEIGHT = 0.30
    HEALTH_WEIGHT = 0.20

    @classmethod
    def calculate(
        cls,
        environmental_stress: int,
        infrastructure_risk: int,
        health_capacity: int
    ):

        score = (
            environmental_stress * cls.ENVIRONMENTAL_WEIGHT
            +
            infrastructure_risk * cls.INFRASTRUCTURE_WEIGHT
            +
            health_capacity * cls.HEALTH_WEIGHT
        )

        score = round(score)

        if score >= 71:
            classification = "CRITICAL"
        elif score >= 41:
            classification = "ELEVATED"
        else:
            classification = "STABLE"

        return {
            "cvi_score": score,
            "classification": classification
        }
