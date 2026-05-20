from fastapi import HTTPException, Depends, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.auth.models import EnterpriseUser  # Your existing user database model

class SubscriptionGuard:
    def __init__(self, required_room: str):
        """
        Validates access based on the 6 commercialized rooms.
        Tiers:
        - 'core_grc': Standard Tier (King V basic)
        - 'google', 'unicef': Professional Tier (NIST Cyber, Climate Risk)
        - 'gates', 'isoc', 'safeguard': Enterprise Premium Tier
        """
        self.required_room = required_room

    async def __call__(self, tenant_id: str, db: Session = Depends(get_db)):
        # Fetch the enterprise tenant from your active database pool
        tenant = db.query(EnterpriseUser).filter(EnterpriseUser.id == tenant_id).first()
        
        if not tenant:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Access Denied: Invalid Enterprise Tenant ID."
            )

        # Room 1: King V Core (Standard Access)
        if self.required_room == "core_grc" and not tenant.can_access_king_v:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Tier Upgrade Required: Standard Tier subscription needed for King V Core RegTech rules."
            )

        # Room 2 & 4: NIST Cyber & UNICEF Climate (Professional Access)
        if self.required_room in ["google", "unicef"] and not tenant.can_access_nist_cyber:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Tier Upgrade Required: Professional Tier subscription needed for AI Cybersecurity and Climate Risk rooms."
            )

        # Room 3, 5 & 6: Gates, ISOC, & Safeguard (Enterprise Premium Access)
        if self.required_room in ["gates", "isoc", "safeguard"] and not tenant.can_access_safeguard:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Tier Upgrade Required: Enterprise Premium Tier subscription needed for high-ticket integrity and biosecurity tracking."
            )

        return tenant
