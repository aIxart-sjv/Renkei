from sqlalchemy import Column, Integer, String, Text, DateTime, JSON, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.database import Base


class Alumni(Base):
    __tablename__ = "alumni"

    id = Column(Integer, primary_key=True, index=True)

    # THIS IS THE FIX
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)

    name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False, index=True)

    organization = Column(String(255), nullable=True)
    designation = Column(String(255), nullable=True)

    expertise = Column(JSON, nullable=False)

    bio = Column(Text, nullable=True)

    linkedin_url = Column(String(500), nullable=True)
    github_url = Column(String(500), nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # THIS CONNECTS BACK TO USER
    user = relationship("User", back_populates="alumni_profile")