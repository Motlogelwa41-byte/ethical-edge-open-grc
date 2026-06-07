from fastapi import APIRouter, Depends, HTTPException
from app.services.remediation_engine import RemediationEngine
from app.database.connection import get_db
from sqlalchemy.orm import Session

remediation_router = APIRouter()

@remediation_router.post("/remediate/{control_reference}")
async def apply_remediation(
    control_reference: str,
    db: Session = Depends(get_db),
    tenant: TenantProfile = Depends(verify_account_tier)
):
    # Initialize Engine
    engine = RemediationEngine(tenant_id=tenant.token)
    
    # Execute fix
    result = engine.execute_fix(control_reference)
    
    if result["status"] == "SUCCESS":
        return {"message": f"Remediation for {control_reference} applied.", "status": "fixed"}
    else:
        raise HTTPException(status_code=500, detail="Remediation failed.")
