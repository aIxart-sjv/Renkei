from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


# Base schema
class AchievementBase(BaseModel):
    title: str
    description: Optional[str] = None
    category: str                     # Hackathon, Project, Certification, Startup, etc.
    outcome: Optional[str] = None     # Won, Runner-up, Participated, Failed, etc.
    technologies_used: List[str]
    event_name: Optional[str] = None
    date: Optional[datetime] = None


# Create schema
class AchievementCreate(AchievementBase):
    student_id: int                   # Link to student


# Update schema
class AchievementUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None
    outcome: Optional[str] = None
    technologies_used: Optional[List[str]] = None
    event_name: Optional[str] = None
    date: Optional[datetime] = None


# Response schema
class AchievementResponse(AchievementBase):
    id: int
    student_id: int
    created_at: datetime
    analysis_score: Optional[float] = None   # for AI-based performance analysis

    class Config:
        orm_mode = True