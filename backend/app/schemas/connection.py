from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


# =========================
# BASE SCHEMA
# =========================

class ConnectionBase(BaseModel):
    """
    Shared connection fields
    """

    source_id: int = Field(
        ...,
        description="Source entity ID"
    )

    source_type: str = Field(
        ...,
        max_length=50,
        description="student, mentor, alumni, startup"
    )

    target_id: int = Field(
        ...,
        description="Target entity ID"
    )

    target_type: str = Field(
        ...,
        max_length=50
    )

    connection_type: str = Field(
        ...,
        max_length=50,
        description="mentorship, collaboration, founder, advisor"
    )

    strength: float = Field(
        default=1.0,
        ge=0.0,
        le=1.0,
        description="Connection strength used in ML and graph weights"
    )

    description: Optional[str] = None


# =========================
# CREATE SCHEMA
# =========================

class ConnectionCreate(ConnectionBase):
    """
    Schema for creating connection
    """

    pass


# =========================
# UPDATE SCHEMA
# =========================

class ConnectionUpdate(BaseModel):
    """
    Schema for updating connection
    """

    strength: Optional[float] = Field(
        default=None,
        ge=0.0,
        le=1.0
    )

    description: Optional[str] = None

    connection_type: Optional[str] = None


# =========================
# RESPONSE SCHEMA
# =========================

class ConnectionResponse(ConnectionBase):
    """
    Schema returned by API
    """

    id: int

    created_at: datetime

    updated_at: datetime


    class Config:
        from_attributes = True


# =========================
# SIMPLE LIST RESPONSE
# =========================

class ConnectionListResponse(BaseModel):

    id: int

    source_id: int
    source_type: str

    target_id: int
    target_type: str

    connection_type: str
    strength: float


    class Config:
        from_attributes = True