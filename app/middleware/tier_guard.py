from fastapi import Header, HTTPException, status, Depends
from typing import Optional
import os

# --- Mock Tenant Database Lookup ---
# In production, this queries your init_schema.sql tenant accounts table
MOCK_TENANT_REGISTRY = {
    "test_standard_key_123": {"name": "Local SME Alpha", "tier": "Standard", "monthly_uploads_mb": 0},
    "test_professional_key_456": {"name": "Botswana FinTech Corp", "tier": "Professional", "monthly_uploads_mb": 142},
    "test_premium_key_789": {"name": "Capital SOE Group", "tier": "Premium", "monthly_uploads_mb": 1850}
}

class TenantProfile:
    def __init__(self, token: str, name: str, tier: str, current_usage_mb: int):
        self.token = token
        self.name = name
        self.tier = tier
        self.current_usage_mb = current_usage_mb

async def verify_account_tier(x_ethical_edge_token: Optional[str] = Header(None)) -> TenantProfile:
    """
    Dependency injector that checks incoming requests for a valid subscription token,
    establishing structural multi-tenancy rules before hitting room_gates math.
    """
    # If no token is provided, assume local standard open-core sandbox execution
    if not x_ethical_edge_token:
        # Check if running inside a strict sandboxed container local cluster
        if os.getenv("RUN_ENVIRONMENT") == "LOCAL_SANDBOX":
            return TenantProfile(token="local", name="Local Sandbox Engine", tier="Standard", current_usage_mb=0)
        
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing 'X-Ethical-Edge-Token' authentication header for remote operations."
        )

    tenant = MOCK_TENANT_REGISTRY.get(x_ethical_edge_token)
    if not tenant:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid or expired organization subscription token."
        )

    return TenantProfile(
        token=x_ethical_edge_token,
        name=tenant["name"],
        tier=tenant["tier"],
        current_usage_mb=tenant["monthly_uploads_mb"]
    )

class TierGuard:
    """
    Enforces processing caps and data payload volumes to safeguard 
    the engine's margin structures and token balance.
    """
    @staticmethod
    def enforce_upload_limits(tenant: TenantProfile, incoming_payload_size_mb: float):
        # 1. Professional Tier Capped Boundary (e.g., 250MB limit per month)
        if tenant.tier == "Professional":
            PROF_CEILING_MB = 250.0
            if tenant.current_usage_mb + incoming_payload_size_mb > PROF_CEILING_MB:
                raise HTTPException(
                    status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                    detail=f"Subscription Upload Cap Exceeded. Tier limit: {PROF_CEILING_MB}MB. Please upgrade to Premium."
                )
        
        # 2. Standard Open-Core Operational Limit
        elif tenant.tier == "Standard":
            # Standard tier running on cloud infrastructure cannot ingest large payloads remotely
            if incoming_payload_size_mb > 5.0:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Standard Core Cloud instances are limited to 5MB manual data uploads. Deploy run_local_engine.sh for uncapped storage."
                )

    @staticmethod
    def enforce_ai_auditor_access(tenant: TenantProfile):
        """
        Guarantees you never pay for a Standard user's LLM consumption bills.
        """
        if tenant.tier == "Standard":
            raise HTTPException(
                status_code=status.HTTP_402_PAYMENT_REQUIRED,
                detail="The AI Automated Auditor requires a Professional subscription tier or a locally configured personal LLM environment API key."
            )
