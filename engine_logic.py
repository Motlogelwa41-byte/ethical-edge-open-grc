import json
import os
import re

class CognitiveGRCEngine:
    def __init__(self, risk_appetite=12):
        self.risk_appetite = risk_appetite
        self.checklist_path = os.path.join(os.path.dirname(__file__), 'data', 'king_v_checklist.json')
        
def assess_unicef_vulnerability(self, hazard_type, school_or_clinic_id):
        # 1. Load the UNICEF Hazards data
        unicef_path = os.path.join(os.path.dirname(__file__), 'data', 'unicef_hazards.json')
        with open(unicef_path, 'r') as f:
            hazards = json.load(f)

        # 2. Match the hazard
        match = next((h for h in hazards if h['hazard'] in hazard_type), hazards[0])

        # 3. Output a "UNICEF Vulnerability Score"
        return {
            "vulnerability_index": match['vulnerability_score_increase'],
            "priority_action": match['action_plan'],
            "indicators_to_monitor": match['indicators'],
            "status": "Child-Centric Emergency Preparedness Required"
        }
    def _find_matching_principle(self, text):
        """
        Cognitive Keyword Matcher:
        Scans the King V JSON to find the most relevant principle 
        based on the user's risk description.
        """
        try:
            if not os.path.exists(self.checklist_path):
                return {"principle": "General Governance", "details": "Checklist file not found."}

            with open(self.checklist_path, 'r') as f:
                principles = json.load(f)

            # Simple keyword matching logic
            text = text.lower()
            best_match = principles[0] # Default to the first one
            highest_count = 0

            for p in principles:
                # We look at the principle title and description for matches
                combined_content = (p.get('name', '') + " " + p.get('description', '')).lower()
                
                # Count how many times words from the risk appear in the principle
                keywords = re.findall(r'\w+', text)
                matches = sum(1 for word in keywords if word in combined_content and len(word) > 3)

                if matches > highest_count:
                    highest_count = matches
                    best_match = p

            return best_match
        except Exception as e:
            return {"error": f"Search failed: {str(e)}"}

    def assess_risk(self, title, description, impact, likelihood, control_effectiveness):
        # 1. Standard Risk Math
        inherent_risk = impact * likelihood
        residual_risk = inherent_risk * (1 - control_effectiveness)
        
        # 2. Status Calibration
        if residual_risk > self.risk_appetite:
            status = "🚨 CRITICAL: Board-Level Escalation"
            action = "Immediate mitigation required."
        elif residual_risk > (self.risk_appetite * 0.6):
            status = "⚠️ WARNING: Management Attention"
            action = "Active monitoring needed."
        else:
            status = "✅ ACCEPTABLE: Monitor Locally"
            action = "Risk within appetite."

        # 3. THE COGNITIVE LEAP: Find the King V mapping
        # We combine title and description for a better search
        governance_mapping = self._find_matching_principle(f"{title} {description}")

        return {
            "inherent_risk": inherent_risk,
            "residual_risk": round(residual_risk, 2),
            "status": status,
            "recommended_action": action,
            "governance_mapping": governance_mapping
        }
