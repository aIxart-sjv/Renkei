from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


# =========================
# BASE SCHEMA
# =========================

class AchievementBase(BaseModel):
    """
    Shared achievement fields
    """

    title: str = Field(..., max_length=255)

    description: Optional[str] = None

    category: str = Field(
        ...,
        max_length=100,
        description="hackathon, project, certification, competition"
    )

    score: float = Field(
        default=0.0,
        ge=0,
        le=100
    )

    rank: Optional[int] = None

    position: Optional[str] = None

    organization: Optional[str] = None

    achievement_date: Optional[datetime] = None


# =========================
# CREATE SCHEMA
# =========================

class AchievementCreate(AchievementBase):
    """
    Schema for creating achievement
    """

    student_id: int


# =========================
# UPDATE SCHEMA
# =========================

class AchievementUpdate(BaseModel):
    """
    Schema for updating achievement
    """

    title: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None
    score: Optional[float] = Field(default=None, ge=0, le=100)
    rank: Optional[int] = None
    position: Optional[str] = None
    organization: Optional[str] = None
    achievement_date: Optional[datetime] = None


# =========================
# RESPONSE SCHEMA
# =========================

class AchievementResponse(AchievementBase):
    """
    Schema returned by API
    """

    id: int

    student_id: int

    created_at: datetime

    updated_at: datetime


    class Config:
        from_attributes = True


# =========================
# SIMPLE LIST SCHEMA
# =========================

class AchievementListResponse(BaseModel):

    id: int
    title: str
    category: str
    score: float

    class Config:
        from_attributes = True