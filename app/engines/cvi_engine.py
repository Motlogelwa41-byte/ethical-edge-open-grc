class CVIEngine:
    """
    Child Vulnerability Index calculation engine.
    """

    ENVIRONMENTAL_WEIGHT = 0.50
    INFRASTRUCTURE_WEIGHT = 0.30
    HEALTH_WEIGHT = 0.20

    @staticmethod
    def calculate(
        environmental_stress: int,
        infrastructure_risk: int,
        health_capacity: int
    ):

        score = (
            environmental_stress * CVIEngine.ENVIRONMENTAL_WEIGHT
            +
            infrastructure_risk * CVIEngine.INFRASTRUCTURE_WEIGHT
            +
            health_capacity * CVIEngine.HEALTH_WEIGHT
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
            "breakdown": {
                "environmental_stress": environmental_stress,
                "infrastructure_risk": infrastructure_risk,
                "health_capacity": health_capacity
            }
        }
