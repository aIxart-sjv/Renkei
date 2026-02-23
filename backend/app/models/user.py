from sqlalchemy import Column, Integer, String, Boolean, DateTime, func
from sqlalchemy.orm import relationship
from datetime import datetime

from app.database import Base


class User(Base):
    __tablename__ = "users"

    # Primary Key
    id = Column(Integer, primary_key=True, index=True)

    # Basic Info
    name = Column(String(255), nullable=False)

    email = Column(String(255), unique=True, nullable=False, index=True)

    # Hashed password (never store plain password)
    password = Column(String(255), nullable=False)

    # Role system
    # Examples: student, mentor, alumni, admin, investor
    role = Column(String(50), nullable=False, default="student")

    # Account status
    status = Column(String(50), nullable=False, default="active")

    # Timestamp
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    alumni_profile = relationship("Alumni", back_populates="user", uselist=False)