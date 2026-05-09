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
