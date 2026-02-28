from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    DateTime,
    ForeignKey,
    Float
)
from sqlalchemy.orm import relationship
from datetime import datetime

from app.models.base import BaseModel


class Startup(BaseModel):
    """
    Startup model

    Represents startups in the innovation ecosystem.

    Used in:
    - startup recommendations
    - talent matching
    - graph intelligence
    - innovation scoring
    """

    __tablename__ = "startups"


    # =========================
    # BASIC INFO
    # =========================

    name = Column(
        String(255),
        nullable=False,
        index=True
    )

    description = Column(
        Text,
        nullable=True
    )

    domain = Column(
        String(255),
        nullable=True,
        index=True
        # example:
        # AI, FinTech, HealthTech
    )

    industry = Column(
        String(255),
        nullable=True
    )

    product_stage = Column(
        String(50),
        nullable=True,
        default="idea"
    )
    # =========================
    # TECH & PRODUCT INFO
    # =========================

    tech_stack = Column(
        Text,
        nullable=True
        # example:
        # Python, React, AWS, FastAPI
    )

    product_stage = Column(
        String(100),
        nullable=True
        # idea, prototype, MVP, growth, scaling
    )


    # =========================
    # FOUNDER INFO
    # =========================

    founder_id = Column(
        Integer,
        ForeignKey("students.id", ondelete="SET NULL"),
        nullable=True,
        index=True
    )


    # =========================
    # INNOVATION METRICS (ML FEATURES)
    # =========================

    innovation_score = Column(
        Float,
        default=0.0,
        nullable=False
    )

    team_size = Column(
        Integer,
        default=1,
        nullable=False
    )


    # =========================
    # EXTERNAL LINKS
    # =========================

    website = Column(
        String(500),
        nullable=True
    )

    github_url = Column(
        String(500),
        nullable=True
    )

    linkedin_url = Column(
        String(500),
        nullable=True
    )


    # =========================
    # LOCATION
    # =========================

    location = Column(
        String(255),
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

    founder = relationship(
        "Student",
        back_populates="startups"
    )




    # =========================
    # HELPER METHODS
    # =========================

    def __repr__(self):

        return (
            f"<Startup id={self.id} "
            f"name={self.name} "
            f"domain={self.domain}>"
        )