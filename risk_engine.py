# This finds the directory where risk_engine.py is located
BASE_DIR = Path(__file__).resolve().parent.parent
from pathlib import Path
import json

class CognitiveGRCEngine:
    def __init__(self, context="Standard"):
        self.context = context
        self.hazards = self.load_base_hazards()
        
        if self.context == "UNICEF":
            self.activate_climate_brain()

    def activate_climate_brain(self):
        """Injects UNICEF-specific climate hazards and child-centric logic."""
        with open('data/unicef_hazards.json', 'r') as f:
            unicef_data = json.load(f)
            # Merge UNICEF hazards into the main processing engine
            self.hazards.extend(unicef_data['unicef_context']['hazards'])
            print("Climate Brain Active: UNICEF Context Applied.")

    def calculate_risk_index(self, hazard_id):
        # The logic would increase the severity if it's a UNICEF-tracked hazard
        pass

def calculate_adjusted_score(base_impact, base_likelihood, is_unicef_hazard=False, impact_score=1):
    """
    Calculates the risk score. 
    If context is UNICEF, it applies a 'Climate Brain' multiplier.
    """
    # Standard Risk Formula: Risk = Impact * Likelihood
    score = base_impact * base_likelihood
    
    if is_unicef_hazard:
        # We apply the 'Climate Brain' logic:
        # Increase score based on the specific unicef_impact_score (scale 1-10)
        multiplier = 1 + (impact_score / 10)
        score = score * multiplier
        
    return round(score, 2)
2. Implementing the JSON Integration
Here is how the engine will actually "see" and process the unicef_hazards.json file you are creating.

Python
import json

class ClimateBrain:
    def __init__(self, hazard_file='data/unicef_hazards.json'):
        with open(hazard_file, 'r') as f:
            self.data = json.load(f)
            self.hazard_map = {h['id']: h for h in self.data['unicef_context']['hazards']}

    def assess_project_hazards(self, detected_hazards):
        """
        detected_hazards: List of IDs identified in the project scope
        """
        results = []
        for h_id in detected_hazards:
            is_unicef = h_id in self.hazard_map
            impact_val = self.hazard_map[h_id]['unicef_impact_score'] if is_unicef else 1
            
            # Example: Base Likelihood and Impact from general engine
            final_score = calculate_adjusted_score(
                base_impact=5, 
                base_likelihood=4, 
                is_unicef_hazard=is_unicef, 
                impact_score=impact_val
            )
            
            results.append({
                "hazard_id": h_id,
                "context": "UNICEF" if is_unicef else "Standard",
                "final_risk_rating": final_score
            })
        return results
