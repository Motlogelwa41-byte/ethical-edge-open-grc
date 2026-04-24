def calculate_risk_score(impact, likelihood, control_effectiveness):
    """
    COSO Performance Logic:
    1. Inherent Risk = Impact * Likelihood
    2. Residual Risk = Inherent Risk * (1 - Control Effectiveness)
    """
    inherent_risk = impact * likelihood
    residual_risk = inherent_risk * (1 - control_effectiveness)
    
    return inherent_risk, residual_risk

def check_alignment(residual_risk, risk_appetite):
    # If residual risk > appetite, it triggers a 'Governance' alert
    return "ALIGNED" if residual_risk <= risk_appetite else "ACTION REQUIRED"

# Example Data for 'InnovateCorp' Operations
business_objective = "99.9% System Uptime"
risk_appetite_score = 15  # Scaled 1-100

# Inputs: Impact (1-10), Likelihood (1-10), Control % (0.0-1.0)
i_risk, r_risk = calculate_risk_score(impact=8, likelihood=5, control_effectiveness=0.7)
status = check_alignment(r_risk, risk_appetite_score)

print(f"Objective: {business_objective}")
print(f"Residual Risk: {r_risk} | Status: {status}")
