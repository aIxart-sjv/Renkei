from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import datetime


# Base schema (shared fields)
class StudentBase(BaseModel):
    name: str
    email: EmailStr
    skills: List[str]
    interests: List[str]
    bio: Optional[str] = None


# Schema for creating a student
class StudentCreate(StudentBase):
    pass


# Schema for updating a student
class StudentUpdate(BaseModel):
    name: Optional[str] = None
    skills: Optional[List[str]] = None
    interests: Optional[List[str]] = None
    bio: Optional[str] = None


# Schema for returning student data (response model)
class StudentResponse(StudentBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True