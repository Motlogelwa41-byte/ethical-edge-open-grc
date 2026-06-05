from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.orm import Session
from app.database.connection import get_db
from app.middleware.tier_guard import verify_account_tier, TenantProfile
from app.room_manager import get_room_data_async, log_to_ledger
from app.context import current_tenant_id

router = APIRouter()

@router.get("/compliance/room/{room_key}")
async def get_compliance_dashboard(
    room_key: str,
    db: Session = Depends(get_db),
    tenant: TenantProfile = Depends(verify_account_tier)
):
    """
    Primary endpoint for the dashboard. 
    Uses the authenticated tenant context to fetch isolated data.
    """
    try:
        # 1. Access the tenant_id set by the middleware
        tenant_id = current_tenant_id.get()
        
        # 2. Fetch room data asynchronously
        # We pass the db session and tenant_id explicitly for the Room Manager to use
        result = await get_room_data_async(
            room_key=room_key,
            user_role="admin", # Ideally, pull this from your user/JWT logic
            session=db,
            tenant_id=tenant_id
        )

        # 3. Log the read action to the immutable ledger
        log_to_ledger(db, tenant_id, "SYSTEM_USER", "READ_ROOM_DATA", room_key, {"status": "success"})
        
        db.commit()
        return result

    except Exception as e:
        db.rollback()
        # In production, use a logger instead of print
        print(f"❌ API Error: {str(e)}")
        raise HTTPException(
            status_code=500, 
            detail="Internal engine error during compliance fetch."
        )
