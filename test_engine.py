from src.risk_engine import CognitiveGRCEngine

def run_test():
    print("--- Starting Cognitive GRC Test ---")
    
    # Scenario A: Standard Engine
    standard_engine = CognitiveGRCEngine(context="Standard")
    # Using a dummy ID; since it's not UNICEF context, no multiplier applies
    std_score = standard_engine.calculate_risk_index("CLIM-001", base_impact=5, base_likelihood=4)
    print(f"Standard Score for CLIM-001: {std_score}")

    print("\n--- Switching to UNICEF Context ---")
    
    # Scenario B: UNICEF Engine (The Climate Brain)
    unicef_engine = CognitiveGRCEngine(context="UNICEF")
    # CLIM-001 is in our JSON with a unicef_impact_score of 9
    climate_score = unicef_engine.calculate_risk_index("CLIM-001", base_impact=5, base_likelihood=4)
    print(f"UNICEF Climate Brain Score for CLIM-001: {climate_score}")

    if climate_score > std_score:
        print("\nSUCCESS: The Climate Brain correctly weighted the hazard!")
    else:
        print("\nCHECK: The score did not change. Verify your JSON ID matches 'CLIM-001'.")

if __name__ == "__main__":
    run_test()
