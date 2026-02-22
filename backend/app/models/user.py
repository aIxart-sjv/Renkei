from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func

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