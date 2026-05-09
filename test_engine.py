import sys
import os
from pathlib import Path

# Fix the path so Python sees the 'src' folder
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))

try:
    from risk_engine import CognitiveGRCEngine
except ImportError as e:
    print(f"Import Error: {e}")
    print("Ensure risk_engine.py is inside the 'src' folder.")
    sys.exit(1)

def run_test():
    print("\n--- 🧠 CLIMATE BRAIN: INTEGRITY TEST ---")
    
    # 1. Standard Context
    std_engine = CognitiveGRCEngine(context="Standard")
    std_score = std_engine.calculate_risk_index("CLIM-001", 5, 4)
    print(f"Standard Risk Score: {std_score}")

    # 2. UNICEF Context
    print("--- 🛡️ SWITCHING TO UNICEF CONTEXT ---")
    unicef_engine = CognitiveGRCEngine(context="UNICEF")
    unicef_score = unicef_engine.calculate_risk_index("CLIM-001", 5, 4)
    print(f"UNICEF Adjusted Score: {unicef_score}")

    # 3. Final Verdict
    if unicef_score > std_score:
        print("\n✅ SUCCESS: The Climate Brain is weighting risks correctly!")
    else:
        print("\n⚠️  CHECK: The score stayed the same. Is CLIM-001 in your JSON?")

# THIS IS THE PART PYTHON IS LOOKING FOR
if __name__ == "__main__":
    run_test()
