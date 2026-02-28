from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


# =========================
# BASE SCHEMA
# =========================

class MentorBase(BaseModel):
    """
    Shared mentor fields
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

    expertise: Optional[str] = None

    skills: Optional[str] = None

    bio: Optional[str] = None

    mentorship_score: Optional[float] = Field(
        default=0.0,
        ge=0
    )

    total_mentees: Optional[int] = Field(
        default=0,
        ge=0
    )

    available: Optional[bool] = True

    linkedin_url: Optional[str] = None

    portfolio_url: Optional[str] = None


# =========================
# CREATE SCHEMA
# =========================

class MentorCreate(MentorBase):
    """
    Schema for creating mentor profile
    """

    user_id: int


# =========================
# UPDATE SCHEMA
# =========================

class MentorUpdate(BaseModel):
    """
    Schema for updating mentor profile
    """

    current_company: Optional[str] = None
    current_role: Optional[str] = None
    industry: Optional[str] = None
    years_of_experience: Optional[int] = Field(default=None, ge=0)
    expertise: Optional[str] = None
    skills: Optional[str] = None
    bio: Optional[str] = None
    mentorship_score: Optional[float] = Field(default=None, ge=0)
    total_mentees: Optional[int] = Field(default=None, ge=0)
    available: Optional[bool] = None
    linkedin_url: Optional[str] = None
    portfolio_url: Optional[str] = None


# =========================
# RESPONSE SCHEMA
# =========================

class MentorResponse(MentorBase):
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

class MentorListResponse(BaseModel):

    id: int

    current_company: Optional[str]

    current_role: Optional[str]

    industry: Optional[str]

    mentorship_score: float


    class Config:
        from_attributes = True