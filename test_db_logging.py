cat << 'EOF' > test_db_logging.py
import json
import os
import sys
from datetime import datetime, timezone

# Resolve localized path layout variations
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from app.database.session import init_db, SessionLocal
from app.database.models import AuditRun, ControlFinding
from app.services.evidence_collector import GRCEvidenceEngine

def run_persisted_audit_pipeline():
    print("🗄️  Initializing Local Compliance Database Ledger...")
    init_db()
    
    db = SessionLocal()
    tenant = "tenant_sme_001"
    
    print("🚀 Firing Live GRC Evidence Engine Pipeline Scan...")
    engine = GRCEvidenceEngine(target_system_id=tenant)
    
    # Execute structural rules pulling credentials safely from your .env
    github_org = os.getenv("MOCK_CLIENT_GITHUB_ORG", "ethical-edge-internal")
    github_token = os.getenv("MOCK_CLIENT_GITHUB_TOKEN", "mock_token")
    
    payload = engine.execute_pipeline(github_org=github_org, github_token=github_token)
    
    print(f"📈 Real-time Attainment Rated at: {payload.calculated_attainment_rate}%")
    print("💾 Committing snapshot into secure historical ledger...")
    
    try:
        # 1. Store the top-level run record
        new_run = AuditRun(
            tenant_id=payload.system_id,
            timestamp=datetime.fromisoformat(payload.timestamp.replace("Z", "+00:00")),
            attainment_rate=payload.calculated_attainment_rate
        )
        db.add(new_run)
        db.flush() # Pull database-generated ID assignment safely before committing children
        
        # 2. Iteratively store the granular evidentiary proofs
        for result in payload.results:
            finding = ControlFinding(
                audit_run_id=new_run.id,
                control_reference=result.control_reference,
                control_name=result.control_name,
                framework=result.framework,
                status=result.status,
                evidence_payload=json.dumps(result.evidence_payload) # Cast dict to string
            )
            db.add(finding)
            
        db.commit()
        print("✅ Historical Snapshot Successfully Logged!")
        
        # 3. Read back records to verify tracking durability over time
        total_historical_runs = db.query(AuditRun).filter(AuditRun.tenant_id == tenant).count()
        print(f"📊 Historical Insight: Client '{tenant}' now has {total_historical_runs} total audit points on file.")
        
    except Exception as e:
        db.rollback()
        print(f"❌ Transaction Failure: {str(e)}")
    finally:
        db.close()

if __name__ == "__main__":
    run_persisted_audit_pipeline()
EOF

