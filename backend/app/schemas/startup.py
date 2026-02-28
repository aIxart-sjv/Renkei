from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


# =========================
# BASE SCHEMA
# =========================

class StartupBase(BaseModel):
    """
    Shared startup fields
    """

    name: str = Field(
        ...,
        max_length=255
    )

    description: Optional[str] = None

    domain: Optional[str] = Field(
        default=None,
        max_length=255
    )

    industry: Optional[str] = None

    tech_stack: Optional[str] = None

    product_stage: Optional[str] = Field(
        default=None,
        description="idea, prototype, MVP, growth, scaling"
    )

    innovation_score: Optional[float] = Field(
        default=0.0,
        ge=0
    )

    team_size: Optional[int] = Field(
        default=1,
        ge=1
    )

    website: Optional[str] = None

    github_url: Optional[str] = None

    linkedin_url: Optional[str] = None

    location: Optional[str] = None


# =========================
# CREATE SCHEMA
# =========================

class StartupCreate(StartupBase):
    """
    Schema for creating startup
    """

    founder_id: Optional[int] = None


# =========================
# UPDATE SCHEMA
# =========================

class StartupUpdate(BaseModel):
    """
    Schema for updating startup
    """

    name: Optional[str] = None
    description: Optional[str] = None
    domain: Optional[str] = None
    industry: Optional[str] = None
    tech_stack: Optional[str] = None
    product_stage: Optional[str] = None
    innovation_score: Optional[float] = Field(default=None, ge=0)
    team_size: Optional[int] = Field(default=None, ge=1)
    website: Optional[str] = None
    github_url: Optional[str] = None
    linkedin_url: Optional[str] = None
    location: Optional[str] = None
    founder_id: Optional[int] = None


# =========================
# RESPONSE SCHEMA
# =========================

class StartupResponse(StartupBase):
    """
    Schema returned by API
    """

    id: int

    founder_id: Optional[int]

    created_at: datetime

    updated_at: datetime


    class Config:
        from_attributes = True


# =========================
# SIMPLE LIST RESPONSE
# =========================

class StartupListResponse(BaseModel):

    id: int

    name: str

    domain: Optional[str]

    innovation_score: float


    class Config:
        from_attributes = True