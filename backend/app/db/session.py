"""
Database session and engine configuration

Handles:
- PostgreSQL connection
- SQLAlchemy engine
- Session factory
- Connection pooling
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

from app.config import settings
from app.core.logger import get_logger


logger = get_logger(__name__)


# =========================
# DATABASE URL
# =========================

DATABASE_URL = settings.SQLALCHEMY_DATABASE_URI

logger.info(f"Connecting to database: {settings.POSTGRES_SERVER}:{settings.POSTGRES_PORT}")


# =========================
# CREATE ENGINE
# =========================

engine = create_engine(
    DATABASE_URL,

    # Connection pool settings
    pool_size=10,
    max_overflow=20,
    pool_pre_ping=True,

    # Performance settings
    echo=False,  # set True for SQL debugging

    future=True
)


# =========================
# SESSION FACTORY
# =========================

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


# Scoped session for thread safety
ScopedSession = scoped_session(SessionLocal)


# =========================
# GET NEW SESSION
# =========================

def get_session():
    """
    Create new database session
    """

    session = SessionLocal()

    try:
        return session

    except Exception as e:

        logger.error(f"Database session error: {e}")

        session.close()

        raise


# =========================
# CLOSE SESSION
# =========================

def close_session(session):
    """
    Safely close database session
    """

    try:

        session.close()

    except Exception as e:

        logger.error(f"Error closing session: {e}")


# =========================
# TEST CONNECTION
# =========================

def test_connection():
    """
    Test database connectivity
    """

    try:

        with engine.connect() as connection:

            logger.info("Database connection successful")

            return True

    except Exception as e:

        logger.error(f"Database connection failed: {e}")

        return False