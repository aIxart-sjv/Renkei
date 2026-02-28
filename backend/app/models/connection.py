from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    DateTime,
    ForeignKey,
    Text
)
from sqlalchemy.orm import relationship
from datetime import datetime

from app.models.base import BaseModel


class Connection(BaseModel):
    """
    Connection model

    Represents relationships between entities:

    Examples:
    - student ↔ mentor
    - student ↔ student
    - student ↔ startup
    - alumni ↔ student
    - mentor ↔ startup

    This is the foundation of the graph intelligence system.
    """

    __tablename__ = "connections"


    # =========================
    # SOURCE ENTITY
    # =========================

    source_id = Column(
        Integer,
        nullable=False,
        index=True
    )

    source_type = Column(
        String(50),
        nullable=False,
        index=True
        # example:
        # student
        # mentor
        # alumni
        # startup
    )


    # =========================
    # TARGET ENTITY
    # =========================

    target_id = Column(
        Integer,
        nullable=False,
        index=True
    )

    target_type = Column(
        String(50),
        nullable=False,
        index=True
    )


    # =========================
    # CONNECTION DETAILS
    # =========================

    connection_type = Column(
        String(50),
        nullable=False,
        index=True
        # examples:
        # mentorship
        # collaboration
        # startup_member
        # startup_founder
        # advisor
    )


    # =========================
    # CONNECTION STRENGTH (ML FEATURE)
    # =========================

    strength = Column(
        Float,
        default=1.0,
        nullable=False
        # Used in:
        # graph weights
        # ML recommendation training
        # influence scoring
    )


    # =========================
    # OPTIONAL METADATA
    # =========================

    description = Column(
        Text,
        nullable=True
    )


    created_at = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )


    # =========================
    # HELPER METHODS
    # =========================

    def __repr__(self):
        return (
            f"<Connection "
            f"{self.source_type}:{self.source_id} -> "
            f"{self.target_type}:{self.target_id} "
            f"type={self.connection_type} "
            f"strength={self.strength}>"
        )