from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    DateTime,
    Enum
)
from sqlalchemy.orm import relationship
from datetime import datetime
import enum

from app.models.base import BaseModel


# =========================
# USER ROLE ENUM
# =========================

class UserRole(str, enum.Enum):
    student = "student"
    mentor = "mentor"
    alumni = "alumni"
    admin = "admin"


class User(BaseModel):
    """
    User model

    Root identity model for authentication and authorization.

    Each user can be:
    - student
    - mentor
    - alumni
    - admin

    Linked to profile-specific tables.
    """

    __tablename__ = "users"


    # =========================
    # AUTHENTICATION
    # =========================

    email = Column(
        String(255),
        unique=True,
        nullable=False,
        index=True
    )

    username = Column(
        String(100),
        unique=True,
        nullable=False,
        index=True
    )

    hashed_password = Column(
        String(255),
        nullable=False
    )


    # =========================
    # ROLE
    # =========================

    role = Column(
        Enum(UserRole),
        nullable=False,
        index=True
    )


    # =========================
    # ACCOUNT STATUS
    # =========================

    is_active = Column(
        Boolean,
        default=True,
        nullable=False
    )

    is_superuser = Column(
        Boolean,
        default=False,
        nullable=False
    )

    is_verified = Column(
        Boolean,
        default=False,
        nullable=False
    )


    # =========================
    # PROFILE INFO
    # =========================

    full_name = Column(
        String(255),
        nullable=True
    )

    profile_image = Column(
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

    student = relationship(
        "Student",
        back_populates="user",
        uselist=False,
        cascade="all, delete-orphan"
    )

    mentor = relationship(
        "Mentor",
        back_populates="user",
        uselist=False,
        cascade="all, delete-orphan"
    )

    alumni = relationship(
        "Alumni",
        back_populates="user",
        uselist=False,
        cascade="all, delete-orphan"
    )


    # =========================
    # HELPER METHODS
    # =========================

    def __repr__(self):

        return (
            f"<User id={self.id} "
            f"email={self.email} "
            f"role={self.role}>"
        )