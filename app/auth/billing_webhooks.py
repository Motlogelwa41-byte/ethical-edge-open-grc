from fastapi import APIRouter, Depends, HTTPException, status, Header
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field
from app.database import get_db
from app.auth.models import EnterpriseUser

router = APIRouter(
    prefix="/billing/webhooks",
    tags=["Ethical Edge Billing - Automated Lifecycle Integration"]
)

# 1. PAYLOAD SCHEMAS FOR INCOMING BILLING EVENTS
class BillingWebhookPayload(BaseModel):
    event_type: str = Field(..., example="subscription.updated")
    tenant_id: str = Field(..., example="8a7b6c5d-4e3f-2a1b-0c9d-8e7f6a5b4c3d")
    purchased_tier: str = Field(..., example="PROFESSIONAL")
    payment_status: str = Field(..., example="paid")

# 2. AUTOMATED WEBHOOK LISTENER
@router.post("/listener", status_code=status.HTTP_200_OK)
async def handle_billing_webhook_event(
    payload: BillingWebhookPayload, 
    db: Session = Depends(get_db),
    x_webhook_signature: str = Header(None) # Place for securing the webhook route later
):
    """
    Listens to payment gateway events. Automatically provision or strip features 
    in the database based on real-time transaction states.
    """
    # Look up the target enterprise account
    tenant = db.query(EnterpriseUser).filter(EnterpriseUser.id == payload.tenant_id).first()
    if not tenant:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Billing Error: Target enterprise tenant token not found."
        )

    # Event Handle Route A: Successful Payment or Tier Upgrade
    if payload.event_type in ["subscription.created", "subscription.updated", "payment.succeeded"]:
        if payload.payment_status == "paid":
            tier = payload.purchased_tier.upper()
            if tier == "STANDARD":
                tenant.can_access_king_v = True
                tenant.can_access_nist_cyber = False
                tenant.can_access_safeguard = False
            elif tier == "PROFESSIONAL":
                tenant.can_access_king_v = True
                tenant.can_access_nist_cyber = True
                tenant.can_access_safeguard = False
            elif tier == "ENTERPRISE":
                tenant.can_access_king_v = True
                tenant.can_access_nist_cyber = True
                tenant.can_access_safeguard = True
            
            db.commit()
            return {"status": "TRANSACTION_PROCESSED", "detail": f"Tenant account sync complete. Tier set to {tier}."}

    # Event Handle Route B: Payment Failure, Dispute, or Cancellation
    elif payload.event_type in ["subscription.cancelled", "payment.failed", "subscription.past_due"]:
        # Immediately strip access back to baseline, protecting premium routes
        tenant.can_access_king_v = True # Keep baseline standard active if desired
        tenant.can_access_nist_cyber = False
        tenant.can_access_safeguard = False
        
        db.commit()
        return {
            "status": "ACCOUNT_RESTRICTED", 
            "detail": "Payment failure or cancellation processed. Premium features revoked automatically."
        }

    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Billing Error: Unhandled webhook event type."
    )
