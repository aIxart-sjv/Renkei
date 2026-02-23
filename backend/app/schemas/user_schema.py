from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


# -----------------------------------
# Base User Schema
# -----------------------------------
class UserBase(BaseModel):

    name: str

    email: EmailStr

    role: str


# -----------------------------------
# Create User Schema (for register)
# -----------------------------------
class UserCreate(UserBase):

    password: str


# -----------------------------------
# Login Schema
# -----------------------------------
class UserLogin(BaseModel):

    email: EmailStr

    password: str


# -----------------------------------
# Response Schema (returned to frontend)
# -----------------------------------
class UserResponse(UserBase):

    id: int

    is_active: Optional[bool] = True

    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# -----------------------------------
# Token Schema
# -----------------------------------
class Token(BaseModel):

    access_token: str

    token_type: str = "bearer"


# -----------------------------------
# Token Data Schema
# -----------------------------------
class TokenData(BaseModel):

    user_id: Optional[int] = None