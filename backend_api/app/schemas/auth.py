from pydantic import BaseModel, EmailStr
from typing import Optional

class User(BaseModel):
    id: str
    email: EmailStr
    username: Optional[str] = None
    is_active: bool = True
    role: Optional[str] = "user"

    class Config:
        schema_extra = {
            "example": {
                "id": "user_abc123",
                "email": "trader@example.com",
                "username": "trader42",
                "is_active": True,
                "role": "user"
            }
        }
