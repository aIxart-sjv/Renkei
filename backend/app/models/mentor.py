from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    Boolean,
    DateTime,
    Text,
    Float
)
from sqlalchemy.orm import relationship
from datetime import datetime

from app.models.base import BaseModel


class Mentor(BaseModel):
    """
    Mentor model

    Represents industry experts, alumni, or professionals who guide students.

    Used in:
    - mentor recommendations
    - graph intelligence
    - influence scoring
    - ML recommendation model
    """

    __tablename__ = "mentors"


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
    # PROFESSIONAL INFO
    # =========================

    current_company = Column(
        String(255),
        nullable=True
    )

    current_role = Column(
        String(255),
        nullable=True
    )

    industry = Column(
        String(255),
        nullable=True
    )

    years_of_experience = Column(
        Integer,
        default=0,
        nullable=False
    )


    # =========================
    # EXPERTISE & PROFILE
    # =========================

    expertise = Column(
        Text,
        nullable=True
        # example:
        # "Machine Learning, AI, Python"
    )

    skills = Column(
        Text,
        nullable=True
    )

    bio = Column(
        Text,
        nullable=True
    )


    # =========================
    # MENTORSHIP METRICS (ML FEATURES)
    # =========================

    mentorship_score = Column(
        Float,
        default=0.0,
        nullable=False
    )

    total_mentees = Column(
        Integer,
        default=0,
        nullable=False
    )


    # =========================
    # AVAILABILITY
    # =========================

    available = Column(
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
        back_populates="mentor"
    )


    # Graph connections



    # =========================
    # HELPER METHODS
    # =========================

    def __repr__(self):

        return (
            f"<Mentor id={self.id} "
            f"company={self.current_company} "
            f"role={self.current_role}>"
        )