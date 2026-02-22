from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, JSON
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.database import Base


class Achievement(Base):
    __tablename__ = "achievements"

    # Primary Key
    id = Column(Integer, primary_key=True, index=True)

    # Achievement basic info
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    category = Column(String(100), nullable=False)  
    # Examples: Hackathon, Project, Certification, Startup

    outcome = Column(String(100), nullable=True)  
    # Examples: Won, Runner-up, Participated, Lost

    # Technologies used (stored as JSON array)
    technologies_used = Column(JSON, nullable=False)

    # Event info
    event_name = Column(String(255), nullable=True)
    date = Column(DateTime(timezone=True), nullable=True)

    # Foreign key linking to Student
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)

    # Auto timestamp
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationship with Student model
    student = relationship(
        "Student",
        back_populates="achievements"
    )