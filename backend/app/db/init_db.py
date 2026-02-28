"""
Database initialization

Creates all tables and optionally seeds initial data.
"""

from sqlalchemy.orm import Session

from app.db.session import engine, SessionLocal
from app.db.base import Base
from app.db import model_registry

from app.core.logger import get_logger
from app.core.security import hash_password
from app.core.constants import ROLE_ADMIN

from app.models.user import User


logger = get_logger(__name__)


# =========================
# CREATE ALL TABLES
# =========================

def create_tables():
    """
    Create database tables from SQLAlchemy models
    """

    logger.info("Creating database tables...")

    Base.metadata.create_all(bind=engine)

    logger.info("Database tables created successfully")


# =========================
# CREATE DEFAULT ADMIN USER
# =========================

def create_default_admin(db: Session):
    """
    Create default admin account if not exists
    """

    logger.info("Checking for default admin user...")

    admin_email = "admin@renkei.com"

    existing_admin = db.query(User).filter(
        User.email == admin_email
    ).first()

    if existing_admin:
        logger.info("Admin user already exists")
        return

    admin_user = User(
        email=admin_email,
        username="admin",
        full_name="System Admin",
        hashed_password=hash_password("admin123"),
        role=ROLE_ADMIN,
        is_active=True,
        is_superuser=True,
        is_verified=True
    )

    db.add(admin_user)
    db.commit()

    logger.info("Default admin user created")


# =========================
# FULL DATABASE INIT
# =========================

def init_db():
    """
    Initialize database completely
    """

    logger.info("Initializing database...")

    # Create tables
    create_tables()

    # Create session
    db = SessionLocal()

    try:

        # Seed admin user
        create_default_admin(db)

    finally:
        db.close()

    logger.info("Database initialization complete")
if __name__ == "__main__":
    init_db()