# 📂 backend_api/app/api/routes/user.py

from fastapi import APIRouter, Depends, HTTPException, status
from backend_api.app.dependencies.auth import get_current_user
from backend_api.app.schemas.auth import User

router = APIRouter()

# -------------------------------
# 👤 Get Current User Info
# -------------------------------
@router.get("/me", response_model=User)
async def get_me(user: User = Depends(get_current_user)):
    """
    Get the currently authenticated user's details.
    """
    return user

# -------------------------------
# 🛡️ Admin-Only Access Verification
# -------------------------------
@router.get("/admin/verify")
async def verify_admin_access(user: User = Depends(get_current_user)):
    """
    Check if the current user has the 'admin' role.
    """
    if user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access restricted to admins"
        )
    return {"status": "authorized", "role": user.role}

# -------------------------------
# 👀 Viewer or Admin Role Access
# -------------------------------
@router.get("/viewer-or-admin")
async def verify_viewer_or_admin(user: User = Depends(get_current_user)):
    """
    Allow access to users with 'viewer' or 'admin' roles.
    """
    if user.role not in ["admin", "viewer"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access restricted to viewers or admins"
        )
    return {"status": "authorized", "role": user.role}
