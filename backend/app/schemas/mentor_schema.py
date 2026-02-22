from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import datetime


# Base schema (shared fields)
class MentorBase(BaseModel):
    name: str
    email: EmailStr
    expertise: List[str]          # domains/skills mentor is strong in
    organization: Optional[str] = None
    designation: Optional[str] = None
    bio: Optional[str] = None


# Schema for creating a mentor
class MentorCreate(MentorBase):
    pass


# Schema for updating a mentor
class MentorUpdate(BaseModel):
    name: Optional[str] = None
    expertise: Optional[List[str]] = None
    organization: Optional[str] = None
    designation: Optional[str] = None
    bio: Optional[str] = None


# Schema for returning mentor data (response model)
class MentorResponse(MentorBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True