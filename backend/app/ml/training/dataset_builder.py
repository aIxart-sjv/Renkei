"""
Dataset builder for ML training

Builds training datasets for:

1. Innovation prediction model
2. Recommendation ranking model

Extracts features from:
- Graph metrics
- Embeddings
- Achievements
- Connections
"""

import numpy as np
from sqlalchemy.orm import Session
from typing import Tuple, List

from app.core.logger import get_logger

from app.models.student import Student
from app.models.mentor import Mentor
from app.models.startup import Startup
from app.models.connection import Connection
from app.models.achievement import Achievement

from app.graph.builder import build_graph
from app.graph.centrality import composite_centrality_score
from app.graph.pagerank import compute_pagerank, normalize_pagerank
from app.graph.algorithms import compute_collaboration_score
from app.graph.similarity import structural_similarity_score

from app.ml.inference.embedder import (
    student_embedding,
    mentor_embedding,
    startup_embedding,
    cosine_similarity
)


logger = get_logger(__name__)


# =========================
# BUILD INNOVATION DATASET
# =========================

def build_innovation_dataset(
    db: Session
) -> Tuple[np.ndarray, np.ndarray]:
    """
    Build dataset for innovation prediction model

    Returns:
        X: feature matrix
        y: innovation scores (labels)
    """

    logger.info("Building innovation dataset...")

    graph = build_graph(db)

    centrality_scores = composite_centrality_score(graph)
    pagerank_scores = normalize_pagerank(
        compute_pagerank(graph)
    )

    students = db.query(Student).all()

    X = []
    y = []

    for student in students:

        centrality = centrality_scores.get(student.id, 0)
        pagerank = pagerank_scores.get(student.id, 0)

        collaboration = compute_collaboration_score(
            graph,
            student.id
        )

        achievements = db.query(Achievement).filter(
            Achievement.student_id == student.id
        ).all()

        achievement_count = len(achievements)

        avg_achievement_score = (
            sum(a.score for a in achievements) / achievement_count
            if achievement_count > 0 else 0
        )

        embedding = student_embedding(student)

        embedding_mean = float(np.mean(embedding))
        embedding_std = float(np.std(embedding))

        features = [
            centrality,
            pagerank,
            collaboration,
            achievement_count,
            avg_achievement_score,
            embedding_mean,
            embedding_std
        ]

        X.append(features)

        # Label = existing innovation score
        y.append(student.innovation_score or 0)

    logger.info(f"Innovation dataset built: {len(X)} samples")

    return np.array(X), np.array(y)


# =========================
# BUILD RECOMMENDATION DATASET
# =========================

def build_recommendation_dataset(
    db: Session
) -> Tuple[np.ndarray, np.ndarray]:
    """
    Build dataset for recommendation model

    Returns:
        X: feature matrix
        y: labels (connection strength)
    """

    logger.info("Building recommendation dataset...")

    graph = build_graph(db)

    students = db.query(Student).all()
    mentors = db.query(Mentor).all()

    X = []
    y = []

    for student in students:

        student_emb = student_embedding(student)

        for mentor in mentors:

            mentor_emb = mentor_embedding(mentor)

            emb_similarity = cosine_similarity(
                student_emb,
                mentor_emb
            )

            graph_similarity = structural_similarity_score(
                graph,
                student.id,
                mentor.id
            )

            collaboration = compute_collaboration_score(
                graph,
                mentor.id
            )

            features = [
                emb_similarity,
                graph_similarity,
                collaboration
            ]

            X.append(features)

            # Label = connection strength if exists
            connection = db.query(Connection).filter(
                Connection.source_id == student.id,
                Connection.target_id == mentor.id
            ).first()

            label = connection.strength if connection else 0

            y.append(label)

    logger.info(f"Recommendation dataset built: {len(X)} samples")

    return np.array(X), np.array(y)


# =========================
# BUILD STARTUP MATCH DATASET
# =========================

def build_startup_dataset(
    db: Session
) -> Tuple[np.ndarray, np.ndarray]:
    """
    Build dataset for student-startup matching
    """

    logger.info("Building startup matching dataset...")

    graph = build_graph(db)

    students = db.query(Student).all()
    startups = db.query(Startup).all()

    X = []
    y = []

    for student in students:

        student_emb = student_embedding(student)

        for startup in startups:

            startup_emb = startup_embedding(startup)

            emb_similarity = cosine_similarity(
                student_emb,
                startup_emb
            )

            graph_similarity = structural_similarity_score(
                graph,
                student.id,
                startup.id
            )

            features = [
                emb_similarity,
                graph_similarity
            ]

            X.append(features)

            # Label heuristic
            y.append(emb_similarity)

    logger.info(f"Startup dataset built: {len(X)} samples")

    return np.array(X), np.array(y)