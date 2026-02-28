"""
Authentication Tests

Run with:
    pytest tests/test_auth.py
"""

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.db.base import Base
from app.models.user import User, UserRole

from app.services.auth_service import (
    register_user,
    authenticate_user,
    login_user
)

from app.schemas.user import (
    UserCreate,
    UserLogin
)


# =========================
# TEST DATABASE SETUP
# =========================

SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}
)

TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


@pytest.fixture(scope="function")
def db():

    Base.metadata.create_all(bind=engine)

    session = TestingSessionLocal()

    yield session

    session.close()

    Base.metadata.drop_all(bind=engine)


# =========================
# TEST USER REGISTRATION
# =========================

def test_register_user(db):

    user_data = UserCreate(
        email="test@example.com",
        username="testuser",
        password="password123",
        full_name="Test User",
        role=UserRole.student
    )

    user = register_user(
        db,
        user_data
    )

    assert user is not None
    assert user.email == "test@example.com"
    assert user.username == "testuser"
    assert user.hashed_password != "password123"
    assert user.role == UserRole.student


# =========================
# TEST AUTHENTICATE USER
# =========================

def test_authenticate_user_success(db):

    user_data = UserCreate(
        email="auth@test.com",
        username="authuser",
        password="password123",
        full_name="Auth User",
        role=UserRole.student
    )

    register_user(db, user_data)

    login_data = UserLogin(
        email="auth@test.com",
        password="password123"
    )

    user = authenticate_user(
        db,
        login_data
    )

    assert user is not None
    assert user.email == "auth@test.com"


def test_authenticate_user_wrong_password(db):

    user_data = UserCreate(
        email="wrong@test.com",
        username="wronguser",
        password="password123",
        full_name="Wrong User",
        role=UserRole.student
    )

    register_user(db, user_data)

    login_data = UserLogin(
        email="wrong@test.com",
        password="wrongpassword"
    )

    user = authenticate_user(
        db,
        login_data
    )

    assert user is None


# =========================
# TEST LOGIN TOKEN GENERATION
# =========================

def test_login_user_returns_token(db):

    user_data = UserCreate(
        email="token@test.com",
        username="tokenuser",
        password="password123",
        full_name="Token User",
        role=UserRole.student
    )

    register_user(db, user_data)

    login_data = UserLogin(
        email="token@test.com",
        password="password123"
    )

    result = login_user(
        db,
        login_data
    )

    assert result is not None
    assert "access_token" in result
    assert result["token_type"] == "bearer"
    assert result["role"] == UserRole.student.value


# =========================
# TEST DUPLICATE REGISTRATION
# =========================

def test_register_duplicate_email(db):

    user_data = UserCreate(
        email="dup@test.com",
        username="dupuser",
        password="password123",
        full_name="Dup User",
        role=UserRole.student
    )

    register_user(db, user_data)

    with pytest.raises(Exception):

        register_user(db, user_data)