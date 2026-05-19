from fastapi import APIRouter, HTTPException, Depends, status
from pydantic import BaseModel, EmailStr, Field
from typing import Dict, Any
from app.auth.security import hash_password, verify_password, create_access_token

router = APIRouter(
    prefix="/auth",
    tags=["Commercial Gatekeeper - Authentication Layer"]
)

# 1. AUTHENTICATION INTAKE SCHEMAS
class UserRegistrationInput(BaseModel):
    full_name: str = Field(..., example="Boitshwarelo Motlogelwa")
    email: EmailStr = Field(..., example="managing_director@ethicaledge.co.bw")
    password: str = Field(..., min_length=6, example="SuperSecurePass123!")
    company_name: str = Field(..., description="Used to bind the account to a specific multi-tenant ID", example="Ethical Edge Corporate Client")
    target_subscription_tier: str = Field(default="STANDARD_FREE", example="PROFESSIONAL")

class UserLoginInput(BaseModel):
    email: EmailStr = Field(..., example="managing_director@ethicaledge.co.bw")
    password: str = Field(..., example="SuperSecurePass123!")

# MOCK LOCAL IN-MEMORY DATABASE FOR IMMEDIACY & MVP TESTING
# This allows you to run validation routines prior to spinning up full SQL connections
MOCK_USER_DB: Dict[str, Dict[str, Any]] = {}

# 2. ONBOARDING & SESSION ENDPOINTS
@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register_enterprise_tenant(user_data: UserRegistrationInput):
    """
    Registers a new corporate tenant, securely hashes credentials, and provisions permission matrices.
    """
    if user_data.email in MOCK_USER_DB:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="ACCOUNT_EXISTS: Email is already registered to a multi-tenant node."
        )

    # Clean tenant string formatting to prevent spaces from muddying database separation queries
    tenant_id = f"EE_TENANT_{user_data.company_name.upper().replace(' ', '_')}"
    
    # Map tier-based premium feature access flags directly at registration (Monetization Engine)
    tier = user_data.target_subscription_tier.upper()
    can_access_nist = True if tier in ["PROFESSIONAL", "ENTERPRISE"] else False
    can_access_safeguard = True if tier == "ENTERPRISE" else False

    # Store the account record matching our SQLAlchemy structure
    hashed = hash_password(user_data.password)
    new_user = {
        "full_name": user_data.full_name,
        "email": user_data.email,
        "hashed_password": hashed,
        "company_tenant_id": tenant_id,
        "subscription_tier": tier,
        "permissions": {
            "can_access_king_v": True,       # Standard Tier Core Feature
            "can_access_nist_cyber": can_access_nist,
            "can_access_safeguard": can_access_safeguard
        }
    }
    
    MOCK_USER_DB[user_data.email] = new_user

    return {
        "status": "REGISTRATION_SUCCESSFUL",
        "message": f"Enterprise account mapped to secure tenant ID: {tenant_id}",
        "tier_assigned": tier,
        "authorized_modules": new_user["permissions"]
    }

@router.post("/login")
async def login_and_issue_jwt(credentials: UserLoginInput):
    """
    Validates company credentials and returns a secure, signed JWT access token for dashboard sessions.
    """
    user_record = MOCK_USER_DB.get(credentials.email)
    
    if not user_record or not verify_password(credentials.password, user_record["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="INVALID_CREDENTIALS: Authentication failed.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Embed multi-tenant variables and permission keys directly into the signed token body
    token_payload = {
        "sub": user_record["email"],
        "tenant_id": user_record["company_tenant_id"],
        "tier": user_record["subscription_tier"],
        "permissions": user_record["permissions"]
    }
    
    access_token = create_access_token(data=token_payload)

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "expires_in_minutes": 60,
        "session_context": {
            "user_identity": user_record["full_name"],
            "tenant_id": user_record["company_tenant_id"]
        }
    }
