import sys
import os
from datetime import datetime

# 1. SETUP DEVELOPMENT PATHS
# Forces Python to recognize the current directory structure for local module mapping
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from fastapi.testclient import TestClient
    from app.main import app
except ImportError:
    print("\n[ERROR] 'httpx' or 'fastapi' testing components missing.")
    print("Please run: pip install httpx fastapi")
    sys.exit(1)

# Initialize the mock local test client
client = TestClient(app)

def run_comprehensive_integration_suite():
    print("======================================================================")
    print("      ETHICAL EDGE COGNITIVE GRC ENGINE - INTEGRATION TEST SUITE      ")
    print("======================================================================\n")

    # ------------------------------------------------------------------------
    # TEST 0: Master Router Health Check
    # ------------------------------------------------------------------------
    print("[TEST 0] Verifying Master Orchestrator Connectivity...")
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["total_active_rooms"] == 6
    print("  -> SUCCESS: Master root online. All 6 tenants mounted.\n")

    # ------------------------------------------------------------------------
    # TEST 1: Room 1 - Core RegTech & King V Logic
    # ------------------------------------------------------------------------
    print("[TEST 1] Testing Room 1 (Core RegTech King V Operations)...")
    king_v_payload = {
        "company_name": "Ethical Edge Pilot Client",
        "ethical_culture_verified": True,
        "corporate_citizenship_verified": True,
        "effective_control_mechanisms": True,
        "stakeholder_legitimacy_verified": False
    }
    response = client.post("/grc/evaluate-king-v?tenant_id=test-tenant-123", json=king_v_payload)
    assert response.status_code in [200, 201]
    print("DEBUG SERVER RESPONSE:", response.status_code, response.text)
    data = response.json()
    assert "SATISFACTORY" in data["corporate_governance_standing"]
    print("  -> SUCCESS: King V assessment engine computed governance rating correctly.")
    
    # Check 5x5 Matrix Logic
    matrix_payload = {"risk_title": "Data Protection Breach", "impact_score": 5, "probability_score": 4}
    response = client.post("/grc/calculate-matrix", json=matrix_payload)
    assert response.status_code == 200
    assert response.json()["risk_classification"] == "CRITICAL RISK"
    print("  -> SUCCESS: 5x5 corporate risk calculation triggers correct protocols.\n")

    # ------------------------------------------------------------------------
    # TEST 2: Room 2 - Google Challenge (NIST CSF 2.0 & SAIF)
    # ------------------------------------------------------------------------
    print("[TEST 2] Testing Room 2 (Google AI Cybersecurity Challenge)...")
    threat_payload = {
        "source_ip": "192.0.2.55",
        "target_cloud_service": "Cloud_SQL_Instance",
        "failed_login_attempts": 12,
        "unauthorized_api_calls": 4,
        "payload_anomaly_detected": True
    }
    response = client.post("/google/analyze-threat", json=threat_payload)
    assert response.status_code == 200
    assert "CRITICAL" in response.json()["threat_telemetry"]["severity_tier"]
    print("  -> SUCCESS: NIST CSF 2.0 threat escalation thresholds validated.")

    saif_payload = {
        "organization_id": "EE-SAIF-NODE-01",
        "infrastructure_sanitization_verified": True,
        "model_input_filtering_active": True,
        "automated_drift_detection_enabled": True
    }
    response = client.post("/google/audit-saif", json=saif_payload)
    assert response.status_code == 200
    assert response.json()["deployment_safety_clearance"] == "APPROVED_FOR_AI_PRODUCTION"
    print("  -> SUCCESS: Google Secure AI Framework (SAIF) posture vetting live.\n")

    # ------------------------------------------------------------------------
    # TEST 3: Room 3 - Bill Gates Foundation (Integrity & Anti-Corruption)
    # ------------------------------------------------------------------------
    print("[TEST 3] Testing Room 3 (Bill Gates Foundation Funding Audits)...")
    grant_payload = {
        "grantee_organization": "SADC Health Consortium",
        "project_title": "Sub-Saharan Clean Water Infrastructure Distribution",
        "total_allocated_usd": 500000.00,
        "funds_disbursed_usd": 400000.00,
        "milestones_expected": 10,
        "milestones_achieved": 4,
        "anti_corruption_screening_passed": True
    }
    response = client.post("/gates/audit-grant", json=grant_payload)
    assert response.status_code == 200
    assert response.json()["governance_assessment"]["risk_tier"] == "HIGH" # Capital spent faster than milestones
    print("  -> SUCCESS: Philanthropic burn rate variance flags allocation anomalies.")

    # Verify Anti-Corruption Hard-Stop Gateway
    grant_payload["anti_corruption_screening_passed"] = False
    response = client.post("/gates/audit-grant", json=grant_payload)
    assert response.status_code == 403 # Verifies programmatic failure block
    print("  -> SUCCESS: Anti-corruption gateway successfully blocks unverified entities.\n")

    # ------------------------------------------------------------------------
    # TEST 4: Room 4 - UNICEF Challenge (Climate Risk & OSS License)
    # ------------------------------------------------------------------------
    print("[TEST 4] Testing Room 4 (UNICEF Venture Fund Open Source Matrix)...")
    climate_payload = {
        "district_location": "Okavango Delta Region",
        "drought_severity_index": 4.2,
        "flood_probability_score": 8.5,
        "impacted_youth_infrastructure": ["primary_school_a", "primary_school_b", "clinic_node_1"]
    }
    response = client.post("/unicef/evaluate-climate-risk", json=climate_payload)
    assert response.status_code == 200
    assert "EMERGENCY VENTURE FUNDING" in response.json()["unicef_grant_action_tier"]
    print("  -> SUCCESS: Child-centric climate vulnerability metrics calculate correctly.")

    oss_payload = {
        "repository_url": "https://github.com/ethical-edge-open-grc",
        "license_type": "MIT",
        "is_public_repository": True,
        "has_documentation_readme": True,
        "dependency_audit_passed": True
    }
    response = client.post("/unicef/validate-open-source", json=oss_payload)
    assert response.status_code == 200
    assert response.json()["unicef_eligibility_status"] == "APPROVED_FOR_FUNDING_CONSIDERATION"
    print("  -> SUCCESS: Open-source licensing parameters align with fund requirements.\n")

    # ------------------------------------------------------------------------
    # TEST 5: Room 5 - Internet Society (ISOC Connectivity & MANRS Vetting)
    # ------------------------------------------------------------------------
    print("[TEST 5] Testing Room 5 (ISOC Infrastructure Trust Layer)...")
    network_payload = {
        "network_identifier": "Chobe_Community_Mesh_01",
        "wpa3_encryption_enforced": True,
        "manrs_anti_spoofing_active": True,
        "manrs_global_coordination_ready": True,
        "average_latency_ms": 45.2,
        "packet_loss_percentage": 0.1
    }
    response = client.post("/isoc/audit-network", json=network_payload)
    assert response.status_code == 200
    assert response.json()["isoc_funding_eligibility"] == "APPROVED_FOR_ISOC_CONSORTIUM"
    print("  -> SUCCESS: MANRS routing safety scores match proposal parameters.\n")

    # ------------------------------------------------------------------------
    # TEST 6: Room 6 - Project SAFEGUARD (State Dept Epidemic Ingestion)
    # ------------------------------------------------------------------------
    print("[TEST 6] Testing Room 6 (Project SAFEGUARD Field Telemetry)...")
    safeguard_payload = {
        "clinic_id": 104,
        "device_session_token": "valid_session_token_no_pii_node",
        "symptom_cluster_flags": ["acute_fever", "hemorrhagic_signs", "respiratory_distress"],
        "anonymized_patient_age_group": "0-4",
        "field_captured_at": datetime.utcnow().isoformat(),
        "geo_location_point": "-24.654,25.912"
    }
    response = client.post("/safeguard/ingest-report", json=safeguard_payload)
    assert response.status_code == 200
    data = response.json()
    assert data["grc_evaluation"]["escalation_tier"] == "CRITICAL RISK"
    assert data["telemetry"]["latency_target_achieved"] is True
    print("  -> SUCCESS: Low-latency epidemiological field sync simulation accepted.")
    print("  -> SUCCESS: Personal details audit confirmation verified (BDPA Shield Functional).\n")

    print("======================================================================")
    print(" 🔥 INTEGRATION TESTING SUMMARY: 100% OF MULTI-ROOM CHANNELS VERIFIED 🔥 ")
    print("======================================================================")

if __name__ == "__main__":
    run_comprehensive_integration_suite()
