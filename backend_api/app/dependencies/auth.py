from fastapi import Depends, HTTPException, status, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
from app.schemas.auth import User
#from app.dependencies.auth_base import get_current_user  # assumes you have a user system
from typing import List
import os
from dotenv import load_dotenv

load_dotenv()

# Use Clerk's RS256 public key to verify tokens
CLERK_JWT_PUBLIC_KEY = os.getenv("CLERK_JWT_PUBLIC_KEY")
JWT_ALGORITHM = "RS256"

security = HTTPBearer()

def decode_clerk_jwt_token(token: str) -> dict:
    if not CLERK_JWT_PUBLIC_KEY:
        raise RuntimeError("Missing CLERK_JWT_PUBLIC_KEY in .env")

    try:
        payload = jwt.decode(
            token,
            CLERK_JWT_PUBLIC_KEY,
            algorithms=[JWT_ALGORITHM],
            options={"verify_aud": False}  # Optional: disable audience verification
        )
        return payload
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> User:
    token = credentials.credentials
    payload = decode_clerk_jwt_token(token)

    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials"
        )

    return User(
        id=payload.get("sub"),
        email=payload.get("email"),
        username=payload.get("username", None),
        is_active=payload.get("is_active", True),
        role=payload.get("public_metadata", {}).get("role", "user")
    )

def get_current_admin_user(
    current_user: User = Depends(get_current_user)
) -> User:
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin privileges required"
        )

def require_roles(allowed_roles: List[str]):
    def role_checker(current_user: User = Depends(get_current_user)) -> User:
        if current_user.role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Access denied. Required roles: {allowed_roles}"
            )
        return current_user
    return role_checker

# Predefined roles for convenience
get_current_admin_user = require_roles(["admin"])
get_current_superuser = require_roles(["superuser", "admin"])
get_current_viewer = require_roles(["viewer", "admin", "superuser"])






