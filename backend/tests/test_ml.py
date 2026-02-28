"""
ML Pipeline Tests

Run with:
    pytest tests/test_ml.py -v
"""

import pytest
import numpy as np

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.db.base import Base

from app.models.user import User, UserRole
from app.models.student import Student
from app.models.embedding import Embedding

from app.ml.inference.embedder import generate_embedding
from app.ml.inference.similarity import compute_similarity

from app.services.ml_service import (
    generate_entity_embedding,
    get_entity_embedding,
    compute_entity_similarity,
    get_model_status
)

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
# CREATE TEST STUDENT
# =========================

def create_test_student(db):

    user = User(
        email="ml@test.com",
        username="mluser",
        hashed_password=hash_password("password"),
        role=UserRole.student
    )

    db.add(user)
    db.commit()

    student = Student(
        user_id=user.id,
        skills="Python, Machine Learning, AI",
        interests="Deep Learning, NLP",
        innovation_score=50
    )

    db.add(student)
    db.commit()

    return student


# =========================
# TEST EMBEDDING GENERATION
# =========================

def test_generate_embedding():

    text = "Python Machine Learning AI"

    vector = generate_embedding(text)

    assert vector is not None
    assert isinstance(vector, list)
    assert len(vector) > 0


# =========================
# TEST ENTITY EMBEDDING STORAGE
# =========================

def test_generate_entity_embedding(db):

    student = create_test_student(db)

    text = "Python AI ML"

    vector = generate_entity_embedding(
        db,
        student.id,
        "student",
        text
    )

    assert vector is not None

    stored_vector = get_entity_embedding(
        db,
        student.id,
        "student"
    )

    assert stored_vector is not None
    assert len(stored_vector) > 0


# =========================
# TEST SIMILARITY FUNCTION
# =========================

def test_similarity_function():

    vec1 = generate_embedding("Python Machine Learning")
    vec2 = generate_embedding("Machine Learning AI")

    similarity = compute_similarity(
        vec1,
        vec2
    )

    assert similarity >= 0
    assert similarity <= 1


# =========================
# TEST ENTITY SIMILARITY
# =========================

def test_entity_similarity(db):

    student1 = create_test_student(db)

    user2 = User(
        email="ml2@test.com",
        username="mluser2",
        hashed_password=hash_password("password"),
        role=UserRole.student
    )

    db.add(user2)
    db.commit()

    student2 = Student(
        user_id=user2.id,
        skills="Python, AI",
        interests="Deep Learning",
        innovation_score=60
    )

    db.add(student2)
    db.commit()


    generate_entity_embedding(
        db,
        student1.id,
        "student",
        "Python Machine Learning"
    )

    generate_entity_embedding(
        db,
        student2.id,
        "student",
        "Machine Learning AI"
    )

    similarity = compute_entity_similarity(
        db,
        student1.id,
        "student",
        student2.id,
        "student"
    )

    assert similarity >= 0


# =========================
# TEST MODEL STATUS
# =========================

def test_model_status():

    status = get_model_status()

    assert "embedding_model_loaded" in status
    assert "innovation_model_loaded" in status
    assert "recommendation_model_loaded" in status


# =========================
# TEST EMBEDDING DATABASE STORAGE
# =========================

def test_embedding_storage(db):

    student = create_test_student(db)

    generate_entity_embedding(
        db,
        student.id,
        "student",
        "Python AI"
    )

    embedding = db.query(Embedding).filter(
        Embedding.entity_id == student.id
    ).first()

    assert embedding is not None

    vector = embedding.get_vector()

    assert isinstance(vector, list)
    assert len(vector) > 0