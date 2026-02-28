"""
Registers all models with SQLAlchemy Base.
This prevents circular imports.
"""

from app.models.user import User
from app.models.student import Student
from app.models.mentor import Mentor
from app.models.alumni import Alumni
from app.models.startup import Startup
from app.models.achievement import Achievement
from app.models.connection import Connection
from app.models.embedding import Embedding