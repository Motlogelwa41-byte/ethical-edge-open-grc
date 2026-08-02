from app.climate.cvi_engine import CVIEngine


result = CVIEngine.calculate(
    environmental_stress=85,
    infrastructure_risk=75,
    health_capacity=60
)

print(result)
