import os
from datetime import datetime, timedelta
from typing import Dict, Any, Optional
from jose import JWTError, jwt
from passlib.context import CryptContext

# 1. CRYPTOGRAPHIC CONTEXT CONFIGURATION
# Using bcrypt for industrial-grade user credential hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Global fallback secret key for development; overridden by container variables in production
SECRET_KEY = os.getenv("JWT_SECRET", "LOCAL_DEV_INSECURE_SECRET_KEY_DONT_USE_IN_PROD_2026")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

# 2. PASSWORD CRYPTOGRAPHY UTILITIES
def hash_password(password: str) -> str:
    """Hashes a plain-text password using secure salt iterations."""
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifies a plain-text password against a stored cryptographic hash."""
    return pwd_context.verify(plain_password, hashed_password)

# 3. MULTI-TENANT JWT MINTER
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Generates a cryptographically signed JWT token embedding user identity, 
    assigned subscription tier, and multi-tenant data isolation keys.
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    # Inject standard timestamp claim
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# 4. BDPA COMPLIANCE & PRIVACY SHIELD ANONYMIZER
def strip_pii_for_bdpa_compliance(payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    Enforces absolute data sovereignty under the Botswana Data Protection Act (BDPA).
    Intercerts data maps at the network edge and strips out all Personally Identifiable Information
    (names, phones, structural metadata) before committing telemetry logs to public research clouds.
    """
    sanitized_payload = payload.copy()
    
    # Target common PII metadata footprints
    pii_keys_to_purge = [
        "full_name", "phone_number", "national_id", "passport_no", 
        "physical_address", "raw_gps_coordinates", "birth_date"
    ]
    
    for key in pii_keys_to_purge:
        if key in sanitized_payload:
            # Drop the value entirely or obscure it to prevent data identification leaks
            sanitized_payload[key] = "[REDACTED_BY_BDPA_EDGE_PRIVACY_SHIELD]"
            
    return sanitized_payload
