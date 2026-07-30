import asyncio
from dotenv import load_dotenv
import os

# 1. Load your updated .env file variables automatically
load_dotenv()

# 2. Safely import the engine model we created
try:
    from app.services.evidence_collector import GRCEvidenceEngine
except ImportError:
    print("❌ Error: Could not find app/services/evidence_collector.py.")
    print("Ensure you created that script file before running this test.")
    import sys
    sys.exit(1)

async def test_run():
    # Instantiate engine with a client identifier
    engine = GRCEvidenceEngine(target_system_id="tenant_sme_001")
    
    print("🚀 Starting Automated GRC Evidence Collection Pipeline...")
    
    # Extract keys safely loaded from your .env
    github_org = os.getenv("MOCK_CLIENT_GITHUB_ORG", "ethical-edge-internal")
    github_token = os.getenv("MOCK_CLIENT_GITHUB_TOKEN", "ghp_mock_token_value")
    
    # Run the continuous assessment checks
    payload = engine.execute_pipeline(github_org=github_org, github_token=github_token)
    
    print("\n--- TEST SUMMARY RESULTS ---")
    print(f"Timestamp: {payload.timestamp}")
    print(f"Continuous Attainment Index: {payload.calculated_attainment_rate}%")
    
    print("\n--- AUDIT EVIDENCE VERIFICATION LOGS ---")
    for result in payload.results:
        print(f"\n[{result.status}] Control: {result.control_reference} - {result.control_name}")
        print(f"Framework Alignment: {result.framework}")
        print(f"Raw Proof Payload for Auditor: {result.evidence_payload}")

if __name__ == "__main__":
    asyncio.run(test_run())
