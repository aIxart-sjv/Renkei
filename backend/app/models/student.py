from sqlalchemy import Column, Integer, String, Text, DateTime, JSON
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.database import Base


class Student(Base):
    __tablename__ = "students"

    # Primary Key
    id = Column(Integer, primary_key=True, index=True)

    # Basic Info
    name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False, index=True)

    # Skills and Interests stored as JSON arrays
    # Example: ["Python", "Machine Learning", "Cybersecurity"]
    skills = Column(JSON, nullable=False)

    # Example: ["AI", "Startups", "Robotics"]
    interests = Column(JSON, nullable=False)

    # Optional bio
    bio = Column(Text, nullable=True)

    # Optional links
    linkedin_url = Column(String(500), nullable=True)
    github_url = Column(String(500), nullable=True)
    portfolio_url = Column(String(500), nullable=True)

    # Innovation score (calculated by graph analytics)
    innovation_score = Column(Integer, nullable=True)

    # Timestamp
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # -----------------------------
    # Relationships
    # -----------------------------

    # Student achievements
    achievements = relationship(
        "Achievement",
        back_populates="student",
        cascade="all, delete-orphan"
    )

    # Future expansion: connections graph
    # connections = relationship("Connection", backref="student")

    # Future expansion: startup participation (if normalized later)
    # startups = relationship("Startup", backref="founder")