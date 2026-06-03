from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime, timezone
import json
import os

from app.database.session import get_db
from app.database.models import AuditRun, ControlFinding
from app.services.evidence_collector import GRCEvidenceEngine

router = APIRouter(prefix="/api/v1/audit", tags=["Audit Automation"])

@router.post("/run", status_code=status.HTTP_201_CREATED)
async def trigger_compliance_scan(tenant_id: str = "tenant_sme_001", db: Session = Depends(get_db)):
    """Triggers a live telemetry sweep and logs the snapshot to the database ledger."""
    try:
        engine = GRCEvidenceEngine(target_system_id=tenant_id)
        github_org = os.getenv("MOCK_CLIENT_GITHUB_ORG", "ethical-edge-internal")
        github_token = os.getenv("MOCK_CLIENT_GITHUB_TOKEN", "mock_token")
        
        payload = engine.execute_pipeline(github_org=github_org, github_token=github_token)
        
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
        return {
            "status": "success",
            "audit_run_id": new_run.id,
            "attainment_rate": payload.calculated_attainment_rate,
            "total_findings_logged": len(payload.results)
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Scan operational failure: {str(e)}")

@router.get("/history/{tenant_id}", status_code=status.HTTP_200_OK)
async def get_compliance_history(tenant_id: str, db: Session = Depends(get_db)):
    """Queries historical compliance runs for a specific client to feed dashboard widgets."""
    runs = db.query(AuditRun).filter(AuditRun.tenant_id == tenant_id).order_by(AuditRun.timestamp.desc()).all()
    
    history_data = []
    for run in runs:
        history_data.append({
            "id": run.id,
            "timestamp": run.timestamp.isoformat(),
            "attainment_rate": run.attainment_rate
        })
    return {"tenant_id": tenant_id, "history": history_data}
