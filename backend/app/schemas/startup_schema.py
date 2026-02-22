from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


# Base schema (shared fields)
class StartupBase(BaseModel):
    name: str
    domain: str                     # e.g., AI, FinTech, EdTech
    description: Optional[str] = None
    tech_stack: List[str]
    founders: List[int]             # list of student IDs
    funding_received: Optional[float] = 0.0
    stage: Optional[str] = "Ideation"   # Ideation, MVP, Early Revenue, etc.


# Schema for creating a startup
class StartupCreate(StartupBase):
    pass


# Schema for updating a startup
class StartupUpdate(BaseModel):
    name: Optional[str] = None
    domain: Optional[str] = None
    description: Optional[str] = None
    tech_stack: Optional[List[str]] = None
    funding_received: Optional[float] = None
    stage: Optional[str] = None


# Schema for returning startup data
class StartupResponse(StartupBase):
    id: int
    created_at: datetime
    innovation_score: Optional[float] = None   # calculated by graph/AI engine

    class Config:
        orm_mode = True