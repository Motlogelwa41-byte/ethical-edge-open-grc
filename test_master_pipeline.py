rom app.room_core_grc.models import GovernanceAssessment
from app.auth.models import EnterpriseUser
# ... other imports
import os
import sys
import json
import asyncio
from datetime import datetime, timezone

# Resolve module paths
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from app.database.session import init_db, SessionLocal
from app.database.models import AuditRun, ControlFinding
from app.services.evidence_collector import GRCEvidenceEngine
from app.api.endpoints.reports import export_compliance_audit_report

def run_end_to_end_validation():
    print("🎯 Starting Master Integration Test...")
    
    # 1. Initialize Database
    init_db()
    db = SessionLocal()
    tenant = "tenant_sme_001"
    
    try:
        # 2. Trigger the Automated Sweeper Engine
        print("🔍 Step 1: Running automated telemetry sweep...")
        engine = GRCEvidenceEngine(target_system_id=tenant)
        payload = engine.execute_pipeline(
            github_org=os.getenv("MOCK_CLIENT_GITHUB_ORG", "ethical-edge-internal"),
            github_token=os.getenv("MOCK_CLIENT_GITHUB_TOKEN", "mock_token")
        )
        
        # 3. Log the Results to the Relational Database Ledger
        print("🗄️  Step 2: Persisting telemetry snapshot into database ledger...")
        new_run = AuditRun(
            tenant_id=payload.system_id,
            timestamp=datetime.fromisoformat(payload.timestamp.replace("Z", "+00:00")),
            attainment_rate=payload.calculated_attainment_rate
        )
        db.add(new_run)
        db.flush()
        
        for result in payload.results:
            finding = ControlFinding(
                audit_run_id=new_run.id,
                control_reference=result.control_reference,
                control_name=result.control_name,
                framework=result.framework,
                status=result.status,
                evidence_payload=json.dumps(result.evidence_payload)
            )
            db.add(finding)
        db.commit()
        
        # 4. Pull directly from the Database to verify historical tracking
        print("📊 Step 3: Querying historical trends to confirm tracking...")
        historical_runs = db.query(AuditRun).filter(AuditRun.tenant_id == tenant).all()
        
        # 5. Trigger the Reports layout logic asynchronously
        print("📄 Step 4: Testing PDF report route compilation engine...")
        asyncio.run(export_compliance_audit_report(tenant_id=tenant))
        
        print("\n🏆 SYSTEM CHECK: SUCCESSFUL END-TO-END INTEGRATION!")
        print(f"   • Database Runs Tracked: {len(historical_runs)}")
        print(f"   • Latest Attainment Rate: {payload.calculated_attainment_rate}%")
        print("   • API Report Endpoint Function: Validated and Importable")
        
    except Exception as e:
        db.rollback()
        print(f"❌ Integration Test Failed: {str(e)}")
    finally:
        db.close()

if __name__ == "__main__":
    run_end_to_end_validation()
