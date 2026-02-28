"""
Student Service Tests

Run with:
    pytest tests/test_students.py -v
"""

import pytest

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.db.base import Base

from app.models.user import User, UserRole
from app.models.student import Student

from app.schemas.student import (
    StudentCreate,
    StudentUpdate
)

from app.services.student_service import (
    create_student,
    get_student,
    get_student_by_user,
    update_student,
    delete_student,
    get_all_students,
    get_top_students,
    search_students_by_skill
)

from app.services.ml_service import get_entity_embedding

from app.core.security import hash_password


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
# CREATE TEST USER
# =========================

def create_test_user(db):

    user = User(
        email="student@test.com",
        username="studentuser",
        hashed_password=hash_password("password"),
        role=UserRole.student,
        full_name="Test Student"
    )

    db.add(user)
    db.commit()

    return user


# =========================
# TEST CREATE STUDENT
# =========================

def test_create_student(db):

    user = create_test_user(db)

    student_data = StudentCreate(
        user_id=user.id,
        university="Test University",
        degree="B.Tech",
        field_of_study="Computer Science",
        graduation_year=2026,
        skills="Python, AI",
        interests="Machine Learning",
        bio="AI student",
        is_active=True
    )

    student = create_student(
        db,
        student_data
    )

    assert student is not None
    assert student.user_id == user.id
    assert student.skills == "Python, AI"

    # Verify embedding created
    embedding = get_entity_embedding(
        db,
        student.id,
        "student"
    )

    assert embedding is not None
    assert len(embedding) > 0


# =========================
# TEST GET STUDENT
# =========================

def test_get_student(db):

    user = create_test_user(db)

    student_data = StudentCreate(
        user_id=user.id,
        university="Test University"
    )

    student = create_student(db, student_data)

    result = get_student(
        db,
        student.id
    )

    assert result is not None
    assert result.id == student.id


# =========================
# TEST GET STUDENT BY USER
# =========================

def test_get_student_by_user(db):

    user = create_test_user(db)

    student = create_student(
        db,
        StudentCreate(user_id=user.id)
    )

    result = get_student_by_user(
        db,
        user.id
    )

    assert result is not None
    assert result.user_id == user.id


# =========================
# TEST UPDATE STUDENT
# =========================

def test_update_student(db):

    user = create_test_user(db)

    student = create_student(
        db,
        StudentCreate(user_id=user.id)
    )

    update_data = StudentUpdate(
        skills="Python, Machine Learning"
    )

    updated = update_student(
        db,
        student.id,
        update_data
    )

    assert updated.skills == "Python, Machine Learning"


# =========================
# TEST DELETE STUDENT
# =========================

def test_delete_student(db):

    user = create_test_user(db)

    student = create_student(
        db,
        StudentCreate(user_id=user.id)
    )

    result = delete_student(
        db,
        student.id
    )

    assert result is True

    deleted = get_student(
        db,
        student.id
    )

    assert deleted is None


# =========================
# TEST GET ALL STUDENTS
# =========================

def test_get_all_students(db):

    user = create_test_user(db)

    create_student(
        db,
        StudentCreate(user_id=user.id)
    )

    students = get_all_students(db)

    assert len(students) >= 1


# =========================
# TEST GET TOP STUDENTS
# =========================

def test_get_top_students(db):

    user = create_test_user(db)

    student = create_student(
        db,
        StudentCreate(
            user_id=user.id,
            skills="Python"
        )
    )

    top_students = get_top_students(db)

    assert top_students is not None
    assert len(top_students) >= 1


# =========================
# TEST SEARCH STUDENTS
# =========================

def test_search_students_by_skill(db):

    user = create_test_user(db)

    create_student(
        db,
        StudentCreate(
            user_id=user.id,
            skills="Python"
        )
    )

    results = search_students_by_skill(
        db,
        "Python"
    )

    assert len(results) >= 1