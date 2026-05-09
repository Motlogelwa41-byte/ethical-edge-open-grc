import json
from pathlib import Path

# Resolve the project root (up one level from 'src')
BASE_DIR = Path(__file__).resolve().parent.parent 

class CognitiveGRCEngine:
    def __init__(self, context="Standard"):
        self.context = context
        # 1. Start with an empty list or your standard hazards
        self.hazards = [] 
        
        # 2. If UNICEF context is active, trigger the Climate Brain
        if self.context == "UNICEF":
            self.activate_climate_brain()

    def activate_climate_brain(self):
        """Injects UNICEF-specific climate hazards using absolute pathing."""
        hazards_path = BASE_DIR / "data" / "unicef_hazards.json"
        
        try:
            with open(hazards_path, 'r') as f:
                unicef_data = json.load(f)
                new_hazards = unicef_data.get('unicef_context', {}).get('hazards', [])
                self.hazards.extend(new_hazards)
                print(f"Climate Brain Active: Loaded {len(new_hazards)} hazards from {hazards_path}")
        except FileNotFoundError:
            print(f"Error: Could not find the hazards file at {hazards_path}")
        except json.JSONDecodeError:
            print(f"Error: The file at {hazards_path} is not valid JSON.")

    def calculate_risk_index(self, hazard_id, base_impact, base_likelihood):
        """
        The core math for the Trust Dividend. 
        Adjusts scores based on the UNICEF 'Climate Brain' logic.
        """
        # Search for the hazard in our loaded list
        hazard = next((h for h in self.hazards if h.get('id') == hazard_id), None)
        
        # Calculate standard score
        score = base_impact * base_likelihood
        
        # Apply UNICEF multiplier if applicable
        if hazard and self.context == "UNICEF":
            impact_val = hazard.get('unicef_impact_score', 1)
            multiplier = 1 + (impact_val / 10)
            score = score * multiplier
            
        return round(score, 2)

# Global Helper Function
def calculate_adjusted_score(base_impact, base_likelihood, is_unicef_hazard=False, impact_score=1):
    score = base_impact * base_likelihood
    if is_unicef_hazard:
        multiplier = 1 + (impact_score / 10)
        score = score * multiplier
    return round(score, 2)
