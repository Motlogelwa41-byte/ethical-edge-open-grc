from fastapi import APIRouter, HTTPException, Depends, status
from pydantic import BaseModel, EmailStr, Field
from typing import Dict, Any
from sqlalchemy.orm import Session

# Import our secure connection dependencies and schemas
from app.database import get_db
from app.auth.models import EnterpriseUser
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

# 2. DATABASE-DRIVEN ONBOARDING & SESSION ENDPOINTS
@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register_enterprise_tenant(user_data: UserRegistrationInput, db: Session = Depends(get_db)):
    """
    Registers a new corporate tenant, checks for database collisions, securely hashes 
    credentials, and commits the records directly to PostgreSQL.
    """
    # Query the live database to check if the user email already exists
    existing_user = db.query(EnterpriseUser).filter(EnterpriseUser.email == user_data.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="ACCOUNT_EXISTS: Email is already registered to a database node."
        )

    # Standardize tenant naming formatting for robust multitenant data separation queries
    tenant_id = f"EE_TENANT_{user_data.company_name.upper().replace(' ', '_')}"
    
    # Establish tier-based feature flag controls (Our monetization gateway)
    tier = user_data.target_subscription_tier.upper()
    can_access_nist = True if tier in ["PROFESSIONAL", "ENTERPRISE"] else False
    can_access_safeguard = True if tier == "ENTERPRISE" else False

    # Instantiate the database record using our SQLAlchemy model mapping
    db_user = EnterpriseUser(
        full_name=user_data.full_name,
        email=user_data.email,
        hashed_password=hash_password(user_data.password),
        company_tenant_id=tenant_id,
        subscription_tier=tier,
        can_access_king_v=True, # Base product access
        can_access_nist_cyber=can_access_nist,
        can_access_safeguard=can_access_safeguard
    )
    
    # Commit transaction to the PostgreSQL instance safely
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return {
        "status": "REGISTRATION_SUCCESSFUL",
        "message": f"Enterprise database record committed to tenant ID: {tenant_id}",
        "tier_assigned": db_user.subscription_tier,
        "authorized_modules": {
            "can_access_king_v": db_user.can_access_king_v,
            "can_access_nist_cyber": db_user.can_access_nist_cyber,
            "can_access_safeguard": db_user.can_access_safeguard
        }
    }

@router.post("/login")
async def login_and_issue_jwt(credentials: UserLoginInput, db: Session = Depends(get_db)):
    """
    Queries the PostgreSQL user database, verifies cryptographic hashes, 
    and returns a signed multi-tenant JWT session token.
    """
    # Fetch the user profile by unique indexed email
    db_user = db.query(EnterpriseUser).filter(EnterpriseUser.email == credentials.email).first()
    
    # Cryptographically verify the plain password against the stored database hash
    if not db_user or not verify_password(credentials.password, db_user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="INVALID_CREDENTIALS: Authentication failed.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Inject data segregation contexts and feature flags inside the cryptographically signed token
    token_payload = {
        "sub": db_user.email,
        "tenant_id": db_user.company_tenant_id,
        "tier": db_user.subscription_tier,
        "permissions": {
            "can_access_king_v": db_user.can_access_king_v,
            "can_access_nist_cyber": db_user.can_access_nist_cyber,
            "can_access_safeguard": db_user.can_access_safeguard
        }
    }
    
    access_token = create_access_token(data=token_payload)

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "expires_in_minutes": 60,
        "session_context": {
            "user_identity": db_user.full_name,
            "tenant_id": db_user.company_tenant_id
        }
    }
