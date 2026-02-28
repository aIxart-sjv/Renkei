"""
Feature engineering utilities for ML models

Converts raw entities into structured ML feature vectors.

Used by:
- innovation model
- recommendation model
- training pipeline
- inference pipeline
"""

import numpy as np
from sqlalchemy.orm import Session
from typing import Dict, List

from app.core.logger import get_logger

from app.models.student import Student
from app.models.mentor import Mentor
from app.models.startup import Startup
from app.models.achievement import Achievement

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
# GRAPH FEATURE EXTRACTION
# =========================

def graph_features(
    entity_id: int,
    graph
) -> Dict[str, float]:
    """
    Extract graph-based features
    """

    try:

        centrality_scores = composite_centrality_score(graph)

        pagerank_scores = normalize_pagerank(
            compute_pagerank(graph)
        )

        collaboration_score = compute_collaboration_score(
            graph,
            entity_id
        )

        return {
            "centrality": centrality_scores.get(entity_id, 0.0),
            "pagerank": pagerank_scores.get(entity_id, 0.0),
            "collaboration": collaboration_score
        }

    except Exception as e:

        logger.error(f"Graph feature extraction failed: {e}")

        return {
            "centrality": 0.0,
            "pagerank": 0.0,
            "collaboration": 0.0
        }


# =========================
# ACHIEVEMENT FEATURES
# =========================

def achievement_features(
    student_id: int,
    db: Session
) -> Dict[str, float]:
    """
    Extract achievement-based features
    """

    try:

        achievements = db.query(Achievement).filter(
            Achievement.student_id == student_id
        ).all()

        count = len(achievements)

        avg_score = (
            sum(a.score for a in achievements) / count
            if count > 0 else 0
        )

        max_score = (
            max(a.score for a in achievements)
            if count > 0 else 0
        )

        return {
            "achievement_count": count,
            "achievement_avg_score": avg_score,
            "achievement_max_score": max_score
        }

    except Exception as e:

        logger.error(f"Achievement feature extraction failed: {e}")

        return {
            "achievement_count": 0,
            "achievement_avg_score": 0,
            "achievement_max_score": 0
        }


# =========================
# EMBEDDING FEATURES
# =========================

def embedding_features(
    embedding: np.ndarray
) -> Dict[str, float]:
    """
    Extract statistical features from embedding vector
    """

    try:

        return {
            "embedding_mean": float(np.mean(embedding)),
            "embedding_std": float(np.std(embedding)),
            "embedding_max": float(np.max(embedding)),
            "embedding_min": float(np.min(embedding))
        }

    except Exception as e:

        logger.error(f"Embedding feature extraction failed: {e}")

        return {
            "embedding_mean": 0,
            "embedding_std": 0,
            "embedding_max": 0,
            "embedding_min": 0
        }


# =========================
# BUILD STUDENT FEATURE VECTOR
# =========================

def student_feature_vector(
    student: Student,
    graph,
    db: Session
) -> np.ndarray:
    """
    Build full student feature vector for ML model
    """

    try:

        graph_feat = graph_features(student.id, graph)

        achievement_feat = achievement_features(
            student.id,
            db
        )

        embedding = student_embedding(student)

        embedding_feat = embedding_features(embedding)

        features = [
            graph_feat["centrality"],
            graph_feat["pagerank"],
            graph_feat["collaboration"],

            achievement_feat["achievement_count"],
            achievement_feat["achievement_avg_score"],
            achievement_feat["achievement_max_score"],

            embedding_feat["embedding_mean"],
            embedding_feat["embedding_std"],
            embedding_feat["embedding_max"],
            embedding_feat["embedding_min"]
        ]

        return np.array(features)

    except Exception as e:

        logger.error(f"Student feature vector failed: {e}")

        return np.zeros(10)


# =========================
# BUILD RECOMMENDATION FEATURE VECTOR
# =========================

def recommendation_feature_vector(
    source,
    target,
    graph
) -> np.ndarray:
    """
    Feature vector for recommendation ML model
    """

    try:

        source_emb = get_embedding(source)
        target_emb = get_embedding(target)

        emb_similarity = cosine_similarity(
            source_emb,
            target_emb
        )

        graph_similarity = structural_similarity_score(
            graph,
            source.id,
            target.id
        )

        source_graph = graph_features(source.id, graph)
        target_graph = graph_features(target.id, graph)

        features = [
            emb_similarity,
            graph_similarity,

            source_graph["pagerank"],
            target_graph["pagerank"],

            source_graph["centrality"],
            target_graph["centrality"],

            target_graph["collaboration"]
        ]

        return np.array(features)

    except Exception as e:

        logger.error(f"Recommendation feature vector failed: {e}")

        return np.zeros(7)


# =========================
# GET ENTITY EMBEDDING
# =========================

def get_embedding(entity):
    """
    Get embedding for student, mentor, or startup
    """

    if isinstance(entity, Student):
        return student_embedding(entity)

    elif isinstance(entity, Mentor):
        return mentor_embedding(entity)

    elif isinstance(entity, Startup):
        return startup_embedding(entity)

    return np.zeros(384)
# =========================
# COMPATIBILITY WRAPPERS
# =========================

def build_student_features(student, graph=None, db=None):
    """
    Wrapper for training pipeline compatibility
    """

    if graph is None or db is None:
        # fallback basic features if graph/db not provided
        embedding = student_embedding(student)

        return np.array([
            float(np.mean(embedding)),
            float(np.std(embedding)),
            float(np.max(embedding)),
            float(np.min(embedding)),
            student.innovation_score,
            student.collaboration_score,
            student.influence_score,
            1 if student.is_active else 0
        ])

    return student_feature_vector(student, graph, db)


def build_recommendation_features(source, target, graph=None):
    """
    Wrapper for recommendation training compatibility
    """

    if graph is None:
        source_emb = get_embedding(source)
        target_emb = get_embedding(target)

        return np.array([
            cosine_similarity(source_emb, target_emb)
        ])

    return recommendation_feature_vector(source, target, graph)