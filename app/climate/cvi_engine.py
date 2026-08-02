"""
Child Vulnerability Index (CVI) Engine

Calculates climate-related vulnerability for
child-centric infrastructure such as schools
and health facilities.
"""


class CVIEngine:
    """
    Cognitive GRC Engine - Child Vulnerability Index Calculator

    Formula:
    CVI =
    Environmental Stress (50%)
    + Infrastructure Risk (30%)
    + Health Capacity (20%)
    """

    ENVIRONMENTAL_WEIGHT = 0.50
    INFRASTRUCTURE_WEIGHT = 0.30
    HEALTH_WEIGHT = 0.20

    @classmethod
    def calculate(
        cls,
        environmental_stress: int,
        infrastructure_risk: int,
        health_capacity: int
    ) -> dict:

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
            "classification": classification,

            "weights": {
                "environmental_stress": cls.ENVIRONMENTAL_WEIGHT,
                "infrastructure_risk": cls.INFRASTRUCTURE_WEIGHT,
                "health_capacity": cls.HEALTH_WEIGHT
            },

            "inputs": {
                "environmental_stress": environmental_stress,
                "infrastructure_risk": infrastructure_risk,
                "health_capacity": health_capacity
            }
        }
