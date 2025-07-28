from fastapi import APIRouter, Depends
from dependencies.auth import get_current_user
from schemas.auth import User

router = APIRouter()

@router.get("/me", response_model=User)
async def get_me(user: User = Depends(get_current_user)):
    return user
