from sqlalchemy import Column, Integer, String, Text, DateTime, Float, JSON
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.database import Base


class Startup(Base):
    __tablename__ = "startups"

    # Primary Key
    id = Column(Integer, primary_key=True, index=True)

    # Basic Info
    name = Column(String(255), nullable=False, index=True)
    domain = Column(String(255), nullable=False)  # AI, FinTech, EdTech, etc.
    description = Column(Text, nullable=True)

    # Tech stack (stored as JSON array)
    # Example: ["FastAPI", "React", "PostgreSQL", "Docker"]
    tech_stack = Column(JSON, nullable=False)

    # Founders (list of student IDs stored as JSON array)
    founders = Column(JSON, nullable=False)

    # Startup stage
    # Examples: Ideation, MVP, Early Revenue, Scaling
    stage = Column(String(100), nullable=False, default="Ideation")

    # Funding received
    funding_received = Column(Float, nullable=True, default=0.0)

    # Optional links
    website_url = Column(String(500), nullable=True)
    github_url = Column(String(500), nullable=True)
    pitch_deck_url = Column(String(500), nullable=True)

    # Innovation score (can be calculated by GraphService)
    innovation_score = Column(Float, nullable=True)

    # Timestamp
    created_at = Column(DateTime(timezone=True), server_default=func.now())