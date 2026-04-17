#from .risk import RiskEngine  # Import the engine we just built

def evaluate_bdpa_compliance(answers, vendor_name="Unknown Vendor"):
    """
    Evaluates 5 critical BDPA questions and returns a total risk score.
    Now automatically flags risks in the Risk Register.
    """
    score = 0
    total_questions = 5

    # 1. Data Localization
    if answers.get("data_outside_botswana") == "No":
        score += 10
    else:
        score += 2 

    # 2. Consent Management
    if answers.get("consent_process") == "Yes":
        score += 10
    else:
        score += 1 

    # 3. Data Protection Officer
    if answers.get("has_dpo") == "Yes":
        score += 10
    else:
        score += 4 

    # 4. Security Measures
    if answers.get("security_measures") == "Yes":
        score += 10
    else:
        score += 1 

    # 5. Purpose Specification
    if answers.get("purpose_limit") == "Yes":
        score += 10
    else:
        score += 3 

    # Calculate final score
    final_score = round(score / total_questions, 1)

    # --- THE POWER MOVE: AUTOMATIC RISK TRIGGER ---
    # If the score is below 7, we automatically define the Risk Level
    if final_score < 7:
        # We determine impact based on how low the score is
        impact = 5 if final_score < 4 else 3
        
        auto_risk_data = {
            "title": f"BDPA Compliance Gap: {vendor_name}",
            "likelihood": 4, # High likelihood of regulatory fine
            "impact": impact,
            "description": f"Compliance score of {final_score}/10. Review needed for BDPA Sections 48, 8, and 24."
        }
        print(f"⚠️ ALERT: Low Compliance detected. Risk flagged for {vendor_name}.")
        # Note: In the next step, we will pass this auto_risk_data to the database
    
    return final_score

def get_compliance_status(score):
    if score >= 8:
        return "GREEN: Low Risk - Compliant"
    elif score >= 5:
        return "AMBER: Medium Risk - Remediation Required"
    else:
        return "RED: High Risk - Non-Compliant"

# --- TEST BLOCK (Move to bottom) ---
if __name__ == "__main__":
    sample_answers = {
        "data_outside_botswana": "Yes",
        "consent_process": "No",
        "has_dpo": "No",
        "security_measures": "No",
        "purpose_limit": "Yes"
    }
    score = evaluate_bdpa_compliance(sample_answers, "Test Corp")
    print(f"--- TEST RUN COMPLETE ---")
    print(f"Compliance Score: {score}/10")
    print(f"Status: {get_compliance_status(score)}") vetting_logic.py

