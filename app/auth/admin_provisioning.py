from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field
import uuid
from app.database import get_db
from app.auth.models import EnterpriseUser  # Your core relational model

router = APIRouter(
    prefix="/admin/provisioning",
    tags=["Ethical Edge Administration - Tenant Provisioning"]
)

# 1. PROVISIONING REQUEST SCHEMAS
class TenantProvisionInput(BaseModel):
    company_name: str = Field(..., example="SADC Commercial Bank")
    contact_email: str = Field(..., example="compliance@sadcbank.com")
    subscription_tier: str = Field(..., description="Tiers: STANDARD, PROFESSIONAL, ENTERPRISE")

class TierUpgradeInput(BaseModel):
    tenant_id: str
    target_tier: str

# 2. AUTOMATED PROVISIONING ENDPOINT
@router.post("/create-tenant", status_code=status.HTTP_201_CREATED)
async def provision_new_enterprise_tenant(tenant: TenantProvisionInput, db: Session = Depends(get_db)):
    """
    Creates a new corporate client in the PostgreSQL database and activates feature flags
    corresponding to their purchased SaaS subscription tier. Generates a master API key.
    """
    # Check for duplicate corporate records
    existing_tenant = db.query(EnterpriseUser).filter(EnterpriseUser.email == tenant.contact_email).first()
    if existing_tenant:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Registration Conflict: An enterprise tenant with this email already exists."
        )

    # Initialize all monetization privilege flags to False by default
    king_v = False
    nist_cyber = False
    safeguard = False

    # Apply tier logic matrix
    tier_upper = tenant.subscription_tier.upper()
    if tier_upper == "STANDARD":
        king_v = True
    elif tier_upper == "PROFESSIONAL":
        king_v = True
        nist_cyber = True
    elif tier_upper == "ENTERPRISE":
        king_v = True
        nist_cyber = True
        safeguard = True
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid Tier Selection. Use: STANDARD, PROFESSIONAL, or ENTERPRISE."
        )

    # Instantiate the secure persistent database tenant record
    new_client = EnterpriseUser(
        id=str(uuid.uuid4()), # Generate secure unique master tenant token
        company_name=tenant.company_name,
        email=tenant.contact_email,
        is_active=True,
        can_access_king_v=king_v,
        can_access_nist_cyber=nist_cyber,
        can_access_safeguard=safeguard
    )

    db.add(new_client)
    db.commit()
    db.refresh(new_client)

    return {
        "provisioning_status": "SUCCESSFUL_TENANT_ACTIVATION",
        "tenant_id": new_client.id,
        "company_name": new_client.company_name,
        "assigned_tier": tier_upper,
        "active_privilege_matrix": {
            "room_1_king_v_core": new_client.can_access_king_v,
            "room_2_4_professional_modules": new_client.can_access_nist_cyber,
            "room_3_5_6_enterprise_premium": new_client.can_access_safeguard
        },
        "instruction": "Provide this tenant_id token to the client. It must be passed with all API payload headers to clear the SubscriptionGuard."
    }

# 3. DYNAMIC TIER UPGRADE/DOWNGRADE ENDPOINT
@router.post("/modify-tier", status_code=status.HTTP_200_OK)
async def modify_tenant_subscription_tier(update: TierUpgradeInput, db: Session = Depends(get_db)):
    """
    Dynamically adjusts a client's monetization feature flags in the database pool,
    instantly elevating or restricting their real-time room access.
    """
    tenant = db.query(EnterpriseUser).filter(EnterpriseUser.id == update.tenant_id).first()
    if not tenant:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tenant modification failed: Target enterprise token not found."
        )

    tier_upper = update.target_tier.upper()
    if tier_upper == "STANDARD":
        tenant.can_access_king_v = True
        tenant.can_access_nist_cyber = False
        tenant.can_access_safeguard = False
    elif tier_upper == "PROFESSIONAL":
        tenant.can_access_king_v = True
        tenant.can_access_nist_cyber = True
        tenant.can_access_safeguard = False
    elif tier_upper == "ENTERPRISE":
        tenant.can_access_king_v = True
        tenant.can_access_nist_cyber = True
        tenant.can_access_safeguard = True
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid Tier Selection. Use: STANDARD, PROFESSIONAL, or ENTERPRISE."
        )

    db.commit()
    db.refresh(tenant)

    return {
        "modification_status": "SUBSCRIPTION_TIER_UPDATED",
        "tenant_id": tenant.id,
        "company_name": tenant.company_name,
        "new_tier": tier_upper,
        "updated_privilege_matrix": {
            "room_1_king_v_core": tenant.can_access_king_v,
            "room_2_4_professional_modules": tenant.can_access_nist_cyber,
            "room_3_5_6_enterprise_premium": tenant.can_access_safeguard
        }
    }
