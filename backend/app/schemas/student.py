from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


# =========================
# BASE SCHEMA
# =========================

class StudentBase(BaseModel):
    """
    Shared student fields
    """

    university: Optional[str] = Field(
        default=None,
        max_length=255
    )

    degree: Optional[str] = Field(
        default=None,
        max_length=255
    )

    field_of_study: Optional[str] = Field(
        default=None,
        max_length=255
    )

    graduation_year: Optional[int] = None

    skills: Optional[str] = None

    interests: Optional[str] = None

    bio: Optional[str] = None

    innovation_score: Optional[float] = Field(
        default=0.0,
        ge=0
    )

    collaboration_score: Optional[float] = Field(
        default=0.0,
        ge=0
    )

    influence_score: Optional[float] = Field(
        default=0.0,
        ge=0
    )

    linkedin_url: Optional[str] = None

    github_url: Optional[str] = None

    portfolio_url: Optional[str] = None

    is_active: Optional[bool] = True


# =========================
# CREATE SCHEMA
# =========================

class StudentCreate(StudentBase):
    """
    Schema for creating student profile
    """

    user_id: int


# =========================
# UPDATE SCHEMA
# =========================

class StudentUpdate(BaseModel):
    """
    Schema for updating student profile
    """

    university: Optional[str] = None
    degree: Optional[str] = None
    field_of_study: Optional[str] = None
    graduation_year: Optional[int] = None
    skills: Optional[str] = None
    interests: Optional[str] = None
    bio: Optional[str] = None

    innovation_score: Optional[float] = Field(
        default=None,
        ge=0
    )

    collaboration_score: Optional[float] = Field(
        default=None,
        ge=0
    )

    influence_score: Optional[float] = Field(
        default=None,
        ge=0
    )

    linkedin_url: Optional[str] = None
    github_url: Optional[str] = None
    portfolio_url: Optional[str] = None

    is_active: Optional[bool] = None


# =========================
# RESPONSE SCHEMA
# =========================

class StudentResponse(StudentBase):
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
# LIST RESPONSE SCHEMA
# =========================

class StudentListResponse(BaseModel):

    id: int

    innovation_score: float

    collaboration_score: float

    influence_score: float

    university: Optional[str]


    class Config:
        from_attributes = True


# =========================
# STUDENT SUMMARY (FOR RECOMMENDATIONS)
# =========================

class StudentSummary(BaseModel):

    id: int

    innovation_score: float

    skills: Optional[str]

    interests: Optional[str]


    class Config:
        from_attributes = True