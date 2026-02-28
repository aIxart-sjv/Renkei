from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    DateTime,
    Text,
    UniqueConstraint
)
from sqlalchemy.orm import relationship
from datetime import datetime

from app.models.base import BaseModel


class Embedding(BaseModel):
    """
    Embedding model

    Stores vector embeddings for entities:

    - students
    - mentors
    - alumni
    - startups

    Used for:
    - recommendation engine
    - similarity search
    - ML training
    - vector store caching
    """

    __tablename__ = "embeddings"


    # =========================
    # ENTITY REFERENCE
    # =========================

    entity_id = Column(
        Integer,
        nullable=False,
        index=True
    )

    entity_type = Column(
        String(50),
        nullable=False,
        index=True
        # student
        # mentor
        # alumni
        # startup
    )


    # =========================
    # EMBEDDING VECTOR
    # =========================

    vector = Column(
        Text,
        nullable=False
        # stored as serialized JSON or comma-separated string
    )


    # =========================
    # MODEL INFO
    # =========================

    model_name = Column(
        String(255),
        default="all-MiniLM-L6-v2",
        nullable=False
    )

    dimension = Column(
        Integer,
        default=384,
        nullable=False
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
    # UNIQUE CONSTRAINT
    # =========================

    __table_args__ = (
        UniqueConstraint(
            "entity_id",
            "entity_type",
            name="unique_entity_embedding"
        ),
    )


    # =========================
    # HELPER METHODS
    # =========================

    def set_vector(self, vector_list):
        """
        Convert list → string for storage
        """

        self.vector = ",".join(
            map(str, vector_list)
        )


    def get_vector(self):
        """
        Convert string → list
        """

        return list(
            map(float, self.vector.split(","))
        )


    def __repr__(self):

        return (
            f"<Embedding "
            f"{self.entity_type}:{self.entity_id} "
            f"dim={self.dimension}>"
        )