"""
Authentication schemas for Renkei
"""

from pydantic import BaseModel, EmailStr, Field
from typing import Optional


# =========================
# REGISTER
# =========================

class UserRegister(BaseModel):
    email: EmailStr
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=6)
    full_name: Optional[str] = None


# =========================
# LOGIN
# =========================

class UserLogin(BaseModel):
    email: EmailStr
    password: str


# =========================
# TOKEN RESPONSE (USED BY ENDPOINT)
# =========================

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


# =========================
# TOKEN (internal use)
# =========================

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


# =========================
# TOKEN PAYLOAD
# =========================

class TokenPayload(BaseModel):
    sub: Optional[int] = None


# =========================
# AUTH RESPONSE
# =========================

class AuthResponse(BaseModel):
    user_id: int
    email: EmailStr
    access_token: str
    token_type: str = "bearer"


# =========================
# USER RESPONSE
# =========================

class UserResponse(BaseModel):
    id: int
    email: EmailStr
    username: str
    full_name: Optional[str] = None