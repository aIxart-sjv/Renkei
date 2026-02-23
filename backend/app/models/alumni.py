from sqlalchemy import Column, Integer, String, Text, DateTime, JSON
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.database import Base


class Alumni(Base):
    __tablename__ = "alumni"

    # Primary Key
    id = Column(Integer, primary_key=True, index=True)

    # Basic Info
    name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False, index=True)

    # Professional Info
    organization = Column(String(255), nullable=True)
    designation = Column(String(255), nullable=True)

    # Expertise (stored as JSON array)
    expertise = Column(JSON, nullable=False)

    # Optional bio
    bio = Column(Text, nullable=True)

    # Optional Linked fields (future expansion)
    linkedin_url = Column(String(500), nullable=True)
    github_url = Column(String(500), nullable=True)

    # Timestamp
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Future relationship support (mentorship, startups, etc.)
    # Example:
    # mentored_startups = relationship("Startup", back_populates="mentor")