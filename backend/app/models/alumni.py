from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    DateTime,
    Boolean,
    Text
)
from sqlalchemy.orm import relationship
from datetime import datetime

from app.db.base import Base


class Alumni(Base):
    """
    Alumni model

    Represents former students who are now:
    - Industry professionals
    - Startup founders
    - Mentors
    - Advisors

    Used in:
    - Graph intelligence
    - Mentor recommendations
    - Influence scoring
    """

    __tablename__ = "alumni"


    # =========================
    # PRIMARY KEY
    # =========================

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )


    # =========================
    # FOREIGN KEY → USER
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
        default=0
    )


    # =========================
    # EDUCATION INFO
    # =========================

    graduation_year = Column(
        Integer,
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


    # =========================
    # PROFILE INFO
    # =========================

    bio = Column(
        Text,
        nullable=True
    )

    skills = Column(
        Text,
        nullable=True
    )

    linkedin_url = Column(
        String(500),
        nullable=True
    )

    portfolio_url = Column(
        String(500),
        nullable=True
    )


    # =========================
    # AVAILABILITY
    # =========================

    available_for_mentorship = Column(
        Boolean,
        default=True
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
        back_populates="alumni"
    )


    # Alumni connections in graph



    # =========================
    # HELPER METHODS
    # =========================

    def __repr__(self):
        return (
            f"<Alumni id={self.id} "
            f"company={self.current_company} "
            f"role={self.current_role}>"
        )