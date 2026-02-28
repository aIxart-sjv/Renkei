from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime
from enum import Enum


# =========================
# USER ROLE ENUM
# =========================

class UserRole(str, Enum):

    student = "student"

    mentor = "mentor"

    alumni = "alumni"

    admin = "admin"


# =========================
# BASE SCHEMA
# =========================

class UserBase(BaseModel):
    """
    Shared user fields
    """

    email: EmailStr

    username: str = Field(
        ...,
        min_length=3,
        max_length=100
    )

    role: UserRole

    full_name: Optional[str] = None

    profile_image: Optional[str] = None

    is_active: Optional[bool] = True

    is_verified: Optional[bool] = False


# =========================
# CREATE SCHEMA
# =========================

class UserCreate(UserBase):
    """
    Schema for creating user
    """

    password: str = Field(
        ...,
        min_length=6,
        max_length=100
    )


# =========================
# LOGIN SCHEMA
# =========================

class UserLogin(BaseModel):

    email: EmailStr

    password: str


# =========================
# UPDATE SCHEMA
# =========================

class UserUpdate(BaseModel):

    username: Optional[str] = None

    full_name: Optional[str] = None

    profile_image: Optional[str] = None

    password: Optional[str] = Field(
        default=None,
        min_length=6
    )

    is_active: Optional[bool] = None

    is_verified: Optional[bool] = None


# =========================
# RESPONSE SCHEMA
# =========================

class UserResponse(UserBase):
    """
    Schema returned by API
    """

    id: int

    created_at: datetime

    updated_at: datetime


    class Config:
        from_attributes = True


# =========================
# SIMPLE USER RESPONSE
# =========================

class UserSummary(BaseModel):

    id: int

    email: EmailStr

    username: str

    role: UserRole


    class Config:
        from_attributes = True


# =========================
# AUTH TOKEN SCHEMA
# =========================

class Token(BaseModel):

    access_token: str

    token_type: str = "bearer"


class TokenPayload(BaseModel):

    sub: Optional[int] = None

    role: Optional[str] = None