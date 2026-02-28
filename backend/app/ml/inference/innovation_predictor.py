"""
Innovation score prediction engine

Uses:
- Graph intelligence
- Achievement metrics
- Embedding features
- Optional trained ML model

Outputs predicted innovation score (0–100)
"""

import numpy as np
import joblib
from sqlalchemy.orm import Session

from app.core.logger import get_logger
from app.config import settings

from app.graph.builder import build_graph
from app.graph.centrality import composite_centrality_score
from app.graph.pagerank import compute_pagerank, normalize_pagerank
from app.graph.algorithms import compute_collaboration_score

from app.models.achievement import Achievement
from app.ml.inference.embedder import student_embedding


logger = get_logger(__name__)


# =========================
# LOAD TRAINED MODEL
# =========================

_model = None


def get_model():
    """
    Load trained ML model if available
    """

    global _model

    if _model is not None:
        return _model

    try:

        _model = joblib.load(
            settings.INNOVATION_MODEL_PATH
        )

        logger.info("Innovation model loaded")

    except Exception:

        logger.warning(
            "No trained innovation model found, using hybrid scoring"
        )

        _model = None

    return _model


# =========================
# FEATURE EXTRACTION
# =========================

def extract_features(
    student,
    db: Session,
    graph
) -> np.ndarray:
    """
    Build feature vector for ML model
    """

    try:

        # Graph features
        centrality_scores = composite_centrality_score(graph)
        pagerank_scores = normalize_pagerank(
            compute_pagerank(graph)
        )

        centrality = centrality_scores.get(student.id, 0)
        pagerank = pagerank_scores.get(student.id, 0)

        collaboration = compute_collaboration_score(
            graph,
            student.id
        )


        # Achievement features
        achievements = db.query(Achievement).filter(
            Achievement.student_id == student.id
        ).all()

        achievement_count = len(achievements)

        avg_achievement_score = (
            sum(a.score for a in achievements) / achievement_count
            if achievement_count > 0 else 0
        )


        # Embedding feature
        embedding = student_embedding(student)

        embedding_mean = float(np.mean(embedding))
        embedding_std = float(np.std(embedding))


        # Feature vector
        features = np.array([
            centrality,
            pagerank,
            collaboration,
            achievement_count,
            avg_achievement_score,
            embedding_mean,
            embedding_std
        ])

        return features

    except Exception as e:

        logger.error(f"Feature extraction failed: {e}")

        return np.zeros(7)


# =========================
# PREDICT USING ML MODEL
# =========================

def predict_with_model(
    features: np.ndarray
) -> float:
    """
    Predict innovation score using trained model
    """

    model = get_model()

    if model is None:
        return None

    try:

        prediction = model.predict(
            features.reshape(1, -1)
        )[0]

        return float(prediction)

    except Exception as e:

        logger.error(f"Model prediction failed: {e}")

        return None


# =========================
# FALLBACK HYBRID SCORING
# =========================

def hybrid_score(
    student,
    db: Session,
    graph
) -> float:
    """
    Graph + achievement scoring fallback
    """

    centrality_scores = composite_centrality_score(graph)
    pagerank_scores = normalize_pagerank(
        compute_pagerank(graph)
    )

    centrality = centrality_scores.get(student.id, 0)
    pagerank = pagerank_scores.get(student.id, 0)

    collaboration = compute_collaboration_score(
        graph,
        student.id
    )

    achievements = db.query(Achievement).filter(
        Achievement.student_id == student.id
    ).all()

    achievement_score = sum(
        a.score for a in achievements
    )

    score = (
        pagerank * 0.3 +
        centrality * 100 * 0.3 +
        collaboration * 10 * 0.2 +
        achievement_score * 0.2
    )

    return min(score, 100.0)


# =========================
# MAIN PREDICTION FUNCTION
# =========================

def predict_innovation_score(
    student,
    db: Session
) -> float:
    """
    Predict innovation score using ML or hybrid model
    """

    try:

        graph = build_graph(db)

        features = extract_features(
            student,
            db,
            graph
        )

        ml_score = predict_with_model(features)

        if ml_score is not None:

            return min(max(ml_score, 0), 100)

        # fallback
        return hybrid_score(
            student,
            db,
            graph
        )

    except Exception as e:

        logger.error(f"Innovation prediction failed: {e}")

        return 0.0