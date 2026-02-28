from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    ForeignKey,
    DateTime,
    Text
)
from sqlalchemy.orm import relationship
from datetime import datetime

from app.db.base import Base


class Achievement(Base):
    """
    Achievement model

    Represents:
    - Hackathons
    - Projects
    - Certifications
    - Competitions
    - Startup milestones

    Used in:
    - Innovation score prediction
    - ML feature engineering
    - Recommendation ranking
    """

    __tablename__ = "achievements"


    # =========================
    # PRIMARY KEY
    # =========================

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )


    # =========================
    # FOREIGN KEYS
    # =========================

    student_id = Column(
        Integer,
        ForeignKey("students.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )


    # =========================
    # ACHIEVEMENT INFO
    # =========================

    title = Column(
        String(255),
        nullable=False
    )

    description = Column(
        Text,
        nullable=True
    )

    category = Column(
        String(100),
        nullable=False
        # example:
        # hackathon
        # project
        # certification
        # competition
        # startup
    )


    # =========================
    # PERFORMANCE METRICS
    # =========================

    score = Column(
        Float,
        default=0.0,
        nullable=False
        # Used by ML model
    )

    rank = Column(
        Integer,
        nullable=True
    )

    position = Column(
        String(50),
        nullable=True
        # example:
        # winner
        # runner-up
        # finalist
    )


    # =========================
    # ORGANIZATION INFO
    # =========================

    organization = Column(
        String(255),
        nullable=True
    )

    achievement_date = Column(
        DateTime,
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

    student = relationship(
        "Student",
        back_populates="achievements"
    )


    # =========================
    # HELPER METHODS
    # =========================

    def __repr__(self):
        return (
            f"<Achievement id={self.id} "
            f"title={self.title} "
            f"score={self.score}>"
        )