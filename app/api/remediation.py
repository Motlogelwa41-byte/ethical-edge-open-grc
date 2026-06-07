from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.connection import get_db
from app.middleware.tier_guard import verify_account_tier, TenantProfile
from app.services.remediation_engine import RemediationEngine

# Consolidated Router with prefix for better API organization
remediation_router = APIRouter(prefix="/api/v1", tags=["Remediation"])

@remediation_router.post("/remediate/{control_reference}")
async def apply_remediation(
    control_reference: str,
    db: Session = Depends(get_db),
    tenant: TenantProfile = Depends(verify_account_tier)
):
    """
    Triggers an automated remediation action for a specific compliance control.
    """
    # 1. Initialize the engine with the tenant's context
    engine = RemediationEngine(tenant_id=tenant.token)
    
    # 2. Attempt to execute the fix with robust error handling
    try:
        result = engine.execute_fix(control_reference)
        
        if result.get("status") == "SUCCESS":
            return {
                "message": f"Remediation for {control_reference} applied successfully.", 
                "status": "fixed"
            }
        else:
            # Handle logical failures reported by the engine
            error_msg = result.get("error", "An unknown error occurred during remediation.")
            raise HTTPException(status_code=500, detail=error_msg)
            
    except Exception as e:
        # Handle unexpected code crashes
        raise HTTPException(status_code=500, detail=f"System Error: {str(e)}")
