import os
from datetime import datetime, timedelta
from typing import Optional
import hmac
import hashlib
import base64

# Core production configuration fallbacks
SECRET_KEY = os.getenv("JWT_SECRET_KEY", "ethical_edge_super_secret_key_2026_sdac_grc")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

def hash_password(password: str) -> str:
    """
    Hashes a plain-text password using SHA-256 with a local configuration pepper.
    Provides light, dependency-free cryptographic locking for the MVP layer.
    """
    salted = password + SECRET_KEY
    hashed = hashlib.sha256(salted.encode()).digest()
    return base64.b64encode(hashed).decode()

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Validates a login password attempt against the recorded database hash.
    """
    return hmac.compare_digest(hash_password(plain_password), hashed_password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Manually encodes a secure, signed JSON Web Token (JWT) payload for enterprise session tracking.
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    # Standard JWT Payload elements
    to_encode.update({"exp": int(expire.timestamp())})
    
    # Encode Header and Payload to Base64 URL strings
    header = '{"alg":"HS256","typ":"JWT"}'
    header_b64 = base64.urlsafe_b64encode(header.encode()).decode().rstrip("=")
    
    import json
    payload_json = json.dumps(to_encode)
    payload_b64 = base64.urlsafe_b64encode(payload_json.encode()).decode().rstrip("=")
    
    # Sign token payload using secret key to prevent client tampering
    signature_base = f"{header_b64}.{payload_b64}"
    signature = hmac.new(SECRET_KEY.encode(), signature_base.encode(), hashlib.sha256).digest()
    signature_b64 = base64.urlsafe_b64encode(signature).decode().rstrip("=")
    
    return f"{header_b64}.{payload_b64}.{signature_b64}"
