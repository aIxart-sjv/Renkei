from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    ForeignKey,
    DateTime,
    Text,
    Boolean
)
from sqlalchemy.orm import relationship, foreign
from sqlalchemy import and_, or_
from datetime import datetime
from app.models.connection import Connection
from app.models.embedding import Embedding
from app.models.base import BaseModel


class Student(BaseModel):
    """
    Student model

    Core entity of Renkei.

    Represents innovators in the ecosystem.

    Used in:
    - Innovation scoring
    - Graph intelligence
    - Recommendation engine
    - ML training and inference
    """

    __tablename__ = "students"


    # =========================
    # USER REFERENCE
    # =========================

    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        unique=True,
        index=True
    )


    # =========================
    # ACADEMIC INFO
    # =========================

    university = Column(
        String(255),
        nullable=True
    )

    degree = Column(
        String(255),
        nullable=True
    )

    field_of_study = Column(
        String(255),
        nullable=True
    )

    graduation_year = Column(
        Integer,
        nullable=True
    )


    # =========================
    # SKILLS & PROFILE
    # =========================

    skills = Column(
        Text,
        nullable=True
        # example: "Python, Machine Learning, React"
    )

    interests = Column(
        Text,
        nullable=True
        # example: "AI, Robotics, Startups"
    )

    bio = Column(
        Text,
        nullable=True
    )


    # =========================
    # INNOVATION METRICS (ML TARGET)
    # =========================

    innovation_score = Column(
        Float,
        default=0.0,
        nullable=False,
        index=True
    )

    collaboration_score = Column(
        Float,
        default=0.0,
        nullable=False
    )

    influence_score = Column(
        Float,
        default=0.0,
        nullable=False
    )


    # =========================
    # ACTIVITY METRICS
    # =========================

    is_active = Column(
        Boolean,
        default=True,
        nullable=False
    )


    # =========================
    # PROFILE LINKS
    # =========================

    linkedin_url = Column(
        String(500),
        nullable=True
    )

    github_url = Column(
        String(500),
        nullable=True
    )

    portfolio_url = Column(
        String(500),
        nullable=True
    )


    # =========================
    # METADATA
    # =========================

    created_at = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False
    )


    # =========================
    # RELATIONSHIPS
    # =========================

    user = relationship(
        "User",
        back_populates="student"
    )


    # Achievements
    achievements = relationship(
        "Achievement",
        back_populates="student",
        cascade="all, delete-orphan"
    )


    # Startups founded by student
    startups = relationship(
        "Startup",
        back_populates="founder"
    )






    # =========================
    # HELPER METHODS
    # =========================

    def __repr__(self):

        return (
            f"<Student id={self.id} "
            f"innovation_score={self.innovation_score}>"
        )