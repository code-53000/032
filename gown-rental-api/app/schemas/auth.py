from typing import Optional
from datetime import datetime

from pydantic import BaseModel

from app.models import UserRole


class LoginRequest(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    user_id: Optional[int] = None


class UserCreate(BaseModel):
    username: str
    password: str
    name: str
    phone: Optional[str] = ""
    role: UserRole = UserRole.BRIDE


class UserOut(BaseModel):
    id: int
    username: str
    name: str
    phone: str
    role: UserRole
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True
