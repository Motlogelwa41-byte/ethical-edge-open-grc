import sys
import os
from pathlib import Path

# Force Python to look inside the 'app' folder
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'app')))

try:
    # This imports CognitiveGRCEngine from your app/risk.py file
    from risk import CognitiveGRCEngine
    print("✅ System: Successfully linked to app/risk.py")
except ImportError as e:
    print(f"❌ System Error: {e}")
    print("Action: Ensure 'class CognitiveGRCEngine' exists inside app/risk.py")
    sys.exit(1)

def run_test():
    print("\n--- 🧠 CLIMATE BRAIN: IMPACT VERIFICATION ---")
    
    # Initialize in UNICEF context
    engine = CognitiveGRCEngine(context="UNICEF")
    
    # Test CLIM-001 (Hazard ID from your JSON)
    # Expected Score: 38.0 (20 + 90% multiplier)
    score = engine.calculate_risk_index("CLIM-001", 5, 4)
    
    print(f"Hazard ID: CLIM-001")
    print(f"Context Setting: {engine.context}")
    print(f"Calculated Risk Priority: {score}")

    if score > 20:
        print("\n✅ SUCCESS: The Climate Brain is active and prioritizing hazards correctly!")
    else:
        print("\n⚠️  NOTICE: Engine loaded, but check the impact_score in data/unicef_hazards.json")

if __name__ == "__main__":
    run_test()
