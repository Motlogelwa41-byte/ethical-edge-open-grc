# vetting_logic.py

def evaluate_bdpa_compliance(answers):
    """
    Evaluates 5 critical BDPA questions and returns a total risk score.
    Higher score = Higher Compliance (10 is perfect, 1 is critical risk).
    """
    score = 0
    total_questions = 5

    # Question 1: Data Localization (Section 48 of BDPA)
    # "Do you transfer or store personal data outside of Botswana?"
    if answers.get("data_outside_botswana") == "No":
        score += 10
    else:
        score += 2 # Risk: International transfers require specific safeguards/consent

    # Question 2: Consent Management (Section 8)
    # "Do you obtain explicit written consent before collecting sensitive personal data?"
    if answers.get("consent_process") == "Yes":
        score += 10
    else:
        score += 1 # High Risk: Processing without consent is a major violation
        if __name__ == "__main__":
    # Test Data
    sample_answers = {
        "data_outside_botswana": "No",
        "consent_process": "Yes",
        "has_dpo": "Yes",
        "security_measures": "Yes",
        "purpose_limit": "Yes"
    }
    score = evaluate_bdpa_compliance(sample_answers)
    print(f"--- TEST RUN COMPLETE ---")
    print(f"Compliance Score: {score}/10")

    # Question 3: Data Protection Officer (Section 20)
    # "Have you appointed or designated a Data Protection Officer (DPO)?"
    if answers.get("has_dpo") == "Yes":
        score += 10
    else:
        score += 4 # Moderate Risk: Administrative requirement

    # Question 4: Security Measures (Section 24)
    # "Do you have technical measures (encryption/firewalls) to protect data?"
    if answers.get("security_measures") == "Yes":
        score += 10
    else:
        score += 1 # Critical Risk: Security is non-negotiable

    # Question 5: Purpose Specification (Section 6)
    # "Do you only use data for the specific reason it was collected?"
    if answers.get("purpose_limit") == "Yes":
        score += 10
    else:
        score += 3 # High Risk: "Scope creep" is a common audit finding

    # Calculate average score out of 10
    final_score = score / total_questions
    return round(final_score, 1)

def get_compliance_status(score):
    if score >= 8:
        return "GREEN: Low Risk - Compliant"
    elif score >= 5:
        return "AMBER: Medium Risk - Remediation Required"
    else:
        return "RED: High Risk - Non-Compliant"
Step 2: Testing the Core (The "Quick Win")
To see if this works without errors, we are going to use main.py just to test this logic. Open main.py and replace everything with this:

Python
# main.py
from vetting_logic import evaluate_bdpa_compliance, get_compliance_status

# Simulate a client's answers (This would eventually come from a form)
client_data = {
    "data_outside_botswana": "Yes",
    "consent_process": "Yes",
    "has_dpo": "No",
    "security_measures": "Yes",
    "purpose_limit": "Yes"
}

# Run the engine
result_score = evaluate_bdpa_compliance(client_data)
status = get_compliance_status(result_score)

print("--- ETHICAL EDGE GRC: BDPA READINESS REPORT ---")
print(f"Final Compliance Score: {result_score}/10")
print(f"Status: {status}")
print("-----------------------------------------------")
