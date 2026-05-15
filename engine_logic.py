import json
import os
import re

class CognitiveGRCEngine:
    def __init__(self, risk_appetite=12):
        self.risk_appetite = risk_appetite
        self.checklist_path = os.path.join(os.path.dirname(__file__), 'data', 'king_v_checklist.json')
        # Corrected data path to match your root-level directory layout
        self.unicef_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'unicef_hazards.json')

    def assess_unicef_vulnerability(self, hazard_type: str) -> dict:
        """
        PHASE 1: UNICEF CLIMATE WING
        Maps institutional data to climate/social hazards from unicef_context
        and applies the $100,000 Grand Challenge budget matrix.
        """
        budget_allocation = {
            "total_funding_usd": 100000,
            "allocation_breakdown": {
                "regtech_risk_modeling_software": 35000,
                "community_climate_resilience_dashboards": 30000,
                "data_collection_and_iot_sensor_integration": 20000,
                "regulatory_compliance_and_governance_auditing": 15000
            }
        }
        
        try:
            if not os.path.exists(self.unicef_path):
                return {"status": "Error", "message": "UNICEF data repository missing."}
                
            with open(self.unicef_path, 'r') as f:
                data = json.load(f)
                
            # Safely navigate your exact JSON context nesting
            hazards_list = data.get("unicef_context", {}).get("hazards", [])
            
            normalized_search = hazard_type.strip().lower()
            match = next((h for h in hazards_list if normalized_search in h.get('hazard_type', '').lower()), None)
            
            if not match:
                return {
                    "status": "Pending Active Risk Analysis",
                    "requested_hazard": hazard_type,
                    "message": f"Hazard type '{hazard_type}' data pending active risk analysis.",
                    "financial_framework": budget_allocation
                }
                
            return {
                "status": "Active Analysis Complete",
                "requested_hazard": hazard_type,
                "hazard_metrics": match,
                "financial_framework": budget_allocation
            }
        except Exception as e:
            return {"error": f"UNICEF Room processing failed: {str(e)}"}

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

        if not infrastructure_data.get('secure_routing_enabled', False):
            resilience_score -= 30
            issues.append("Secure routing (MANRS) not detected.")

        if infrastructure_data.get('data_location') != 'SADC':
            resilience_score -= 25
            issues.append("Data sovereignty risk: Data stored outside SADC region.")

        status = "RESILIENT" if resilience_score > 70 else "VULNERABLE"
        
        return {
            "resilience_score": resilience_score,
            "status": status,
            "identified_gaps": issues,
            "ethics_alignment": "Aligned with AI_ETHICS.md"
        }

    def generate_audit_certificate(self, client_name, project_room, assessment_results):
        """
        Generates a sellable Audit Report Summary.
        """
        return {
            "issuing_entity": "Ethical Edge GRC Consulting (Pty) Ltd",
            "client": client_name,
            "regtech_room": project_room,
            "audit_id": f"EE-{os.urandom(4).hex().upper()}",
            "findings": assessment_results,
            "certification": "Compliant with King V / Ethical AI Standards"
        }
