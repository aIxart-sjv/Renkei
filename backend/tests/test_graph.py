"""
Graph Intelligence Tests

Run with:
    pytest tests/test_graph.py -v
"""

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.db.base import Base

from app.models.user import User, UserRole
from app.models.student import Student
from app.models.mentor import Mentor
from app.models.connection import Connection

from app.graph.builder import build_graph
from app.graph.centrality import composite_centrality_score
from app.graph.pagerank import compute_pagerank, normalize_pagerank

from app.services.graph_service import (
    get_graph_data,
    get_innovation_scores,
    get_top_innovators,
    get_collaboration_score
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
# CREATE TEST DATA
# =========================

def create_test_data(db):

    user1 = User(
        email="student@test.com",
        username="student",
        hashed_password=hash_password("password"),
        role=UserRole.student
    )

    user2 = User(
        email="mentor@test.com",
        username="mentor",
        hashed_password=hash_password("password"),
        role=UserRole.mentor
    )

    db.add_all([user1, user2])
    db.commit()

    student = Student(
        user_id=user1.id,
        skills="Python, AI",
        innovation_score=50
    )

    mentor = Mentor(
        user_id=user2.id,
        skills="Python, ML",
        mentorship_score=80,
        available=True
    )

    db.add_all([student, mentor])
    db.commit()

    connection = Connection(
        source_id=student.id,
        source_type="student",
        target_id=mentor.id,
        target_type="mentor",
        connection_type="mentorship",
        strength=0.9
    )

    db.add(connection)
    db.commit()

    return student, mentor


# =========================
# TEST GRAPH BUILDING
# =========================

def test_build_graph(db):

    student, mentor = create_test_data(db)

    graph = build_graph(db)

    assert graph is not None
    assert graph.number_of_nodes() >= 2
    assert graph.number_of_edges() >= 1


# =========================
# TEST CENTRALITY
# =========================

def test_centrality_score(db):

    student, mentor = create_test_data(db)

    graph = build_graph(db)

    scores = composite_centrality_score(graph)

    assert scores is not None
    assert student.id in scores


# =========================
# TEST PAGERANK
# =========================

def test_pagerank(db):

    student, mentor = create_test_data(db)

    graph = build_graph(db)

    pagerank = normalize_pagerank(
        compute_pagerank(graph)
    )

    assert pagerank is not None
    assert student.id in pagerank


# =========================
# TEST GRAPH SERVICE DATA
# =========================

def test_graph_service_data(db):

    create_test_data(db)

    data = get_graph_data(db)

    assert "nodes" in data
    assert "edges" in data
    assert len(data["nodes"]) > 0


# =========================
# TEST INNOVATION SCORES
# =========================

def test_innovation_scores(db):

    student, mentor = create_test_data(db)

    scores = get_innovation_scores(db)

    assert len(scores) > 0

    entity_ids = [
        s["entity_id"]
        for s in scores
    ]

    assert student.id in entity_ids


# =========================
# TEST TOP INNOVATORS
# =========================

def test_top_innovators(db):

    create_test_data(db)

    innovators = get_top_innovators(db)

    assert innovators is not None
    assert len(innovators) > 0


# =========================
# TEST COLLABORATION SCORE
# =========================

def test_collaboration_score(db):

    student, mentor = create_test_data(db)

    score = get_collaboration_score(
        db,
        student.id
    )

    assert score >= 0