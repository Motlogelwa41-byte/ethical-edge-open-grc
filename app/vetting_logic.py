from .risk import RiskEngine
from .database import save_automated_risk
from . import models

def evaluate_bdpa_compliance(answers, vendor_name="Unknown Vendor", db=None):
    """
    Evaluates 5 critical BDPA questions and returns a total risk score out of 10.
    Now automatically flags risks in the Risk Register if compliance lapses.
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

    # Calculate final score out of 10
    final_score = score / total_questions

    # --- AUTOMATIC RISK TRIGGER ---
    if final_score < 7:
        # Determine impact based on how severe the lapse is
        impact = 5 if final_score < 4 else 3

        auto_risk_data = {
            "title": f"BDPA Compliance Gap: {vendor_name}",
            "likelihood": 4,  # High likelihood of regulatory fine
            "impact": impact,
            "description": f"Compliance score of {round(final_score, 1)}/10. Review needed for BDPA compliance metrics."
        }
        print(f"⚠️ ALERT: Low Compliance detected. Risk flagged for {vendor_name}.")
        
        if db:
            save_automated_risk(db, auto_risk_data)
            print(f"✅ Risk recorded in database for {vendor_name}")

    return round(final_score, 1)


def evaluate_vendor_risk(score, red_line_fail):
    """
    Applies King V 'Red Line' rules to corporate vendor risk scores.
    """
    if red_line_fail:
        impact = 5
        likelihood = 4
        total_risk = impact * likelihood  # 20 (Critical)
    else:
        total_risk = score

    # The Decision Engine
    if total_risk >= 20:
        return "TERMINATE", "Vendor fails critical ethical standards."
    elif 13 <= total_risk < 20:
        return "MITIGATION REQUIRED", "Upload a Remediation Plan to proceed."
    else:
        return "APPROVED", "Vendor meets Ethical Edge standards."


def get_compliance_status(score):
    if score >= 8:
        return "GREEN: Low Risk - Compliant"
    elif score >= 5:
        return "AMBER: Medium Risk - Remediation Required"
    else:
        return "RED: High Risk - Non-Compliant"


def calculate_unicef_child_index(climate_score: float, school_density: int, clinic_status: str):
    """
    Calculates the Child Vulnerability Index for the UNICEF Venture Fund.
    """
    impact_weight = 0.7
    resilience_weight = 0.3

    # If clinics are overwhelmed, risk increases
    resilience_penalty = 0.2 if clinic_status == "low_capacity" else 0.0

    # Calculation
    child_index = (climate_score * impact_weight) + (school_density * resilience_weight) + resilience_penalty

    return {
        "unicef_priority": "CRITICAL" if child_index > 0.8 else "STANDARD",
        "score": round(min(child_index, 1.0), 2)  # Cap at 1.0
    }


# --- CLEAN TEST BLOCK ---
if __name__ == "__main__":
    sample_answers = {
        "data_outside_botswana": "Yes",
        "consent_process": "No",
        "has_dpo": "No",
        "security_measures": "No",
        "purpose_limit": "Yes"
    }
    calculated_score = evaluate_bdpa_compliance(sample_answers, "Test Corp")
    status, message = evaluate_vendor_risk(calculated_score * 2, red_line_fail=False)
    
    print(f"--- TEST RUN COMPLETE ---")
    print(f"Compliance Score: {calculated_score}/10")
    print(f"Status Category: {get_compliance_status(calculated_score)}")
    print(f"Risk Decision: {status} ({message})")
