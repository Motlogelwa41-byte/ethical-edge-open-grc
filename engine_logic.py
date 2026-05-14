import json
import os
import re

class CognitiveGRCEngine:
    def __init__(self, risk_appetite=12):
        self.risk_appetite = risk_appetite
        self.checklist_path = os.path.join(os.path.dirname(__file__), 'data', 'king_v_checklist.json')
        self.unicef_path = os.path.join(os.path.dirname(__file__), 'data', 'unicef_hazards.json')

    def assess_unicef_vulnerability(self, hazard_type, school_or_clinic_id=None):
        """
        PHASE 1: UNICEF CLIMATE WING
        Maps climate hazards to child-centric vulnerability scores.
        """
        try:
            if not os.path.exists(self.unicef_path):
                return {"error": "UNICEF Hazards data not found."}

            with open(self.unicef_path, 'r') as f:
                hazards = json.load(f)

            # Match the hazard from our new JSON
            match = next((h for h in hazards if h['hazard'].lower() in hazard_type.lower()), hazards[0])

            return {
                "vulnerability_index": match['vulnerability_score_increase'],
                "priority_action": match['action_plan'],
                "indicators_to_monitor": match['indicators'],
                "location_id": school_or_clinic_id,
                "status": "Child-Centric Emergency Preparedness Required"
            }
        except Exception as e:
            return {"error": f"Climate assessment failed: {str(e)}"}

    def _find_matching_principle(self, text):
        """
        GATES FOUNDATION / KING V WING
        Cognitive Keyword Matcher for Governance.
        """
        try:
            if not os.path.exists(self.checklist_path):
                return {"principle": "General Governance", "details": "Checklist file not found."}

            with open(self.checklist_path, 'r') as f:
                principles = json.load(f)

            text = text.lower()
            best_match = principles[0]
            highest_count = 0

            for p in principles:
                combined_content = (p.get('name', '') + " " + p.get('description', '')).lower()
                keywords = re.findall(r'\w+', text)
                matches = sum(1 for word in keywords if word in combined_content and len(word) > 3)

                if matches > highest_count:
                    highest_count = matches
                    best_match = p

            return best_match
        except Exception as e:
            return {"error": f"Search failed: {str(e)}"}

    def assess_risk(self, title, description, impact, likelihood, control_effectiveness):
        """
        CORE RISK CALCULATION
        """
        inherent_risk = impact * likelihood
        residual_risk = inherent_risk * (1 - control_effectiveness)
        
        if residual_risk > self.risk_appetite:
            status = "🚨 CRITICAL: Board-Level Escalation"
            action = "Immediate mitigation required."
        elif residual_risk > (self.risk_appetite * 0.6):
            status = "⚠️ WARNING: Management Attention"
            action = "Active monitoring needed."
        else:
            status = "✅ ACCEPTABLE: Monitor Locally"
            action = "Risk within appetite."

        governance_mapping = self._find_matching_principle(f"{title} {description}")

        return {
            "inherent_risk": inherent_risk,
            "residual_risk": round(residual_risk, 2),
            "status": status,
            "recommended_action": action,
            "governance_mapping": governance_mapping
        }

def assess_isoc_resilience(self, infrastructure_data):
        """
        PHASE 2: INTERNET SOCIETY (ISOC) WING
        Audits network integrity and data sovereignty.
        """
        resilience_score = 100
        issues = []

        # Check for secure routing (e.g., MANRS compliance)
        if not infrastructure_data.get('secure_routing_enabled', False):
            resilience_score -= 30
            issues.append("Secure routing (MANRS) not detected.")

        # Check for Data Sovereignty (Local storage for SADC data)
        if infrastructure_data.get('data_location') != 'SADC':
            resilience_score -= 25
            issues.append("Data sovereignty risk: Data stored outside SADC region.")

        status = "RESIILIENT" if resilience_score > 70 else "VULNERABLE"
        
        return {
            "resilience_score": resilience_score,
            "status": status,
            "identified_gaps": issues,
            "ethics_alignment": "Aligned with AI_ETHICS.md"
        }
