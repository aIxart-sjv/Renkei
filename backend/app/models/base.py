"""
Base model class for all database models

Provides common fields:
- id
- created_at
- updated_at

All models should inherit from this class.
"""

from sqlalchemy import Column, Integer, DateTime
from datetime import datetime

from app.db.base import Base as SQLAlchemyBase


class BaseModel(SQLAlchemyBase):
    """
    Abstract base model with common fields
    """

    __abstract__ = True


    # =========================
    # PRIMARY KEY
    # =========================

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )


    # =========================
    # TIMESTAMPS
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
    # HELPER METHODS
    # =========================

    def to_dict(self):
        """
        Convert model to dictionary
        """

        return {
            column.name: getattr(self, column.name)
            for column in self.__table__.columns
        }


    def __repr__(self):
        return f"<{self.__class__.__name__} id={self.id}>"