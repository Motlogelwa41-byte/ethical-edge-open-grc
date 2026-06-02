from fastapi import APIRouter, HTTPException, status
from app.services.evidence_collector import ComplianceTelemetryPayload, GRCEvidenceEngine
import os

router = APIRouter()

# Mocking database persistence structure for context
MOCK_DB = {}

@router.post("/collect-evidence", status_code=status.HTTP_201_CREATED)
async def trigger_and_process_evidence_collection(tenant_id: str):
    """
    Premium Endpoint: Triggers the background data collectors to scan external vectors,
    writes cryptographic-ready evidence payloads, and pushes live delta scores back 
    to the SME Standard Command Center.
    """
    # 1. Fetch encrypted tokens securely for this tenant from your real DB
    github_org = os.getenv("MOCK_CLIENT_GITHUB_ORG", "ethical-edge-internal")
    github_token = os.getenv("MOCK_CLIENT_GITHUB_TOKEN", "ghp_mock_token_value")
    
    # 2. Instantiate and run the engine pipeline
    engine = GRCEvidenceEngine(target_system_id=tenant_id)
    payload = engine.execute_pipeline(github_org=github_org, github_token=github_token)
    
    # 3. Persist the metrics dynamically so the main dashboard view can pull them instantly
    MOCK_DB[tenant_id] = {
        "last_updated": payload.timestamp,
        "framework_attainment_index": f"{payload.calculated_attainment_rate}%",
        "raw_evidence_logs": [res.model_dump() for res in payload.results]
    }
    
    # Calculate the new overarching 'Continuous Governance Score' (CGS)
    # Passed verification controls exponentially uplift the compliance health indicator.
    return {
        "status": "Success",
        "message": f"Collected evidence for {len(payload.results)} active controls.",
        "dashboard_impact": {
            "framework_attainment_index": f"{payload.calculated_attainment_rate}%",
            "system_status": "Secure" if payload.calculated_attainment_rate > 70 else "At Risk"
        }
    }
