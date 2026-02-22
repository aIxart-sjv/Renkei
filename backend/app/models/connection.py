from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.database import Base


class Connection(Base):
    __tablename__ = "connections"

    # Primary Key
    id = Column(Integer, primary_key=True, index=True)

    # Source and Target entities
    source_id = Column(Integer, nullable=False)
    target_id = Column(Integer, nullable=False)

    # Connection type
    # Examples:
    # student_student
    # student_mentor
    # student_alumni
    # student_startup
    # mentor_startup
    connection_type = Column(String(50), nullable=False)

    # Optional description
    description = Column(String(255), nullable=True)

    # Timestamp
    created_at = Column(DateTime(timezone=True), server_default=func.now())