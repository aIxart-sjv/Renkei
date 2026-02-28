from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


# =========================
# BASE SCHEMA
# =========================

class AlumniBase(BaseModel):
    """
    Shared alumni fields
    """

    current_company: Optional[str] = Field(
        default=None,
        max_length=255
    )

    current_role: Optional[str] = Field(
        default=None,
        max_length=255
    )

    industry: Optional[str] = Field(
        default=None,
        max_length=255
    )

    years_of_experience: Optional[int] = Field(
        default=0,
        ge=0
    )

    graduation_year: Optional[int] = None

    degree: Optional[str] = None

    field_of_study: Optional[str] = None

    bio: Optional[str] = None

    skills: Optional[str] = None

    linkedin_url: Optional[str] = None

    portfolio_url: Optional[str] = None

    available_for_mentorship: Optional[bool] = True


# =========================
# CREATE SCHEMA
# =========================

class AlumniCreate(AlumniBase):
    """
    Schema for creating alumni profile
    """

    user_id: int


# =========================
# UPDATE SCHEMA
# =========================

class AlumniUpdate(BaseModel):
    """
    Schema for updating alumni profile
    """

    current_company: Optional[str] = None
    current_role: Optional[str] = None
    industry: Optional[str] = None
    years_of_experience: Optional[int] = Field(default=None, ge=0)
    graduation_year: Optional[int] = None
    degree: Optional[str] = None
    field_of_study: Optional[str] = None
    bio: Optional[str] = None
    skills: Optional[str] = None
    linkedin_url: Optional[str] = None
    portfolio_url: Optional[str] = None
    available_for_mentorship: Optional[bool] = None


# =========================
# RESPONSE SCHEMA
# =========================

class AlumniResponse(AlumniBase):
    """
    Schema returned by API
    """

    id: int

    user_id: int

    created_at: datetime

    updated_at: datetime


    class Config:
        from_attributes = True


# =========================
# SIMPLE LIST RESPONSE
# =========================

class AlumniListResponse(BaseModel):

    id: int
    current_company: Optional[str]
    current_role: Optional[str]
    industry: Optional[str]

    class Config:
        from_attributes = True