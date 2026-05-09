import sys
import os
from pathlib import Path

# This ensures Python can see the 'src' folder
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))

try:
    from risk_engine import CognitiveGRCEngine
except ImportError:
    print("Error: Could not find risk_engine.py inside the src folder.")
    sys.exit(1)

def run_test():
    print("--- 🧠 CLIMATE BRAIN: INTEGRITY TEST ---")
    
    # 1. Test the Standard Context
    std_engine = CognitiveGRCEngine(context="Standard")
    # Base calculation: 5 (Impact) * 4 (Likelihood) = 20
    std_score = std_engine.calculate_risk_index("CLIM-001", 5, 4)
    print(f"Standard Risk Score: {std_score}")

    # 2. Test the UNICEF Context
    print("\n--- 🛡️ SWITCHING TO UNICEF CONTEXT ---")
    unicef_engine = CognitiveGRCEngine(context="UNICEF")
    
    # This should be higher because CLIM-001 is a UNICEF hazard
    unicef_score = unicef_engine.calculate_risk_index("CLIM-001", 5, 4)
    print(f"UNICEF Adjusted Score: {unicef_score}")

    # 3. Final Verdict
    if unicef_score > std_score:
        print("\n✅ SUCCESS: The Climate Brain is active and weighting risks correctly!")
    else:
        print("\n❌ FAIL: The score didn't change. Check if CLIM-001 exists in data/unicef_hazards.json")

if __name__ == "__main__":
    run_test()
