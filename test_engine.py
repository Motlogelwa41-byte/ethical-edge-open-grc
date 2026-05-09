import sys
import os
from pathlib import Path

# 1. Add the 'app' folder to the search path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'app')))

try:
    # 2. This now looks for risk.py inside the app/ folder
    from risk import CognitiveGRCEngine
    print("✅ Success: Linked to app/risk.py")
except ImportError as e:
    print(f"❌ Error: {e}")
    print("Check if 'class CognitiveGRCEngine' is defined inside app/risk.py")
    sys.exit(1)

def run_test():
    print("\n--- 🧠 CLIMATE BRAIN: UNICEF IMPACT TEST ---")
    
    # Initialize in UNICEF context
    engine = CognitiveGRCEngine(context="UNICEF")
    
    # Test CLIM-001 (Hazard ID from your JSON)
    # Expected Score: 38.0
    score = engine.calculate_risk_index("CLIM-001", 5, 4)
    
    print(f"Hazard: CLIM-001")
    print(f"Context: {engine.context}")
    print(f"Final Priority Score: {score}")

    if score > 20:
        print("\n✅ VERIFIED: The Climate Brain is active.")
    else:
        print("\n⚠️  NOTICE: Engine loaded, but no multiplier detected.")

if __name__ == "__main__":
    run_test()
