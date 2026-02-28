"""
Embedding similarity engine

Provides:
- Cosine similarity
- Batch similarity
- Top-K similarity search
- Similarity matrix

Used in recommendation engine and ML ranking
"""

import numpy as np
from typing import List, Tuple, Dict

from app.core.logger import get_logger


logger = get_logger(__name__)


# =========================
# COSINE SIMILARITY
# =========================

def cosine_similarity(
    vector_a: np.ndarray,
    vector_b: np.ndarray
) -> float:
    """
    Compute cosine similarity between two vectors
    """

    try:

        if vector_a is None or vector_b is None:
            return 0.0

        similarity = np.dot(vector_a, vector_b)

        return float(similarity)

    except Exception as e:

        logger.error(f"Cosine similarity error: {e}")

        return 0.0


# =========================
# BATCH SIMILARITY
# =========================

def batch_similarity(
    query_vector: np.ndarray,
    candidate_vectors: List[np.ndarray]
) -> List[float]:
    """
    Compute similarity between query and multiple candidates
    """

    try:

        similarities = []

        for vec in candidate_vectors:

            sim = cosine_similarity(
                query_vector,
                vec
            )

            similarities.append(sim)

        return similarities

    except Exception as e:

        logger.error(f"Batch similarity error: {e}")

        return []


# =========================
# FIND TOP-K SIMILAR
# =========================

def top_k_similar(
    query_vector: np.ndarray,
    candidate_vectors: List[np.ndarray],
    candidate_ids: List[int],
    top_k: int = 10
) -> List[Tuple[int, float]]:
    """
    Return top-k most similar entities
    """

    try:

        scores = []

        for idx, vec in enumerate(candidate_vectors):

            score = cosine_similarity(
                query_vector,
                vec
            )

            scores.append(
                (candidate_ids[idx], score)
            )

        scores.sort(
            key=lambda x: x[1],
            reverse=True
        )

        return scores[:top_k]

    except Exception as e:

        logger.error(f"Top-K similarity error: {e}")

        return []


# =========================
# SIMILARITY MATRIX
# =========================

def similarity_matrix(
    vectors: List[np.ndarray],
    ids: List[int]
) -> Dict[int, Dict[int, float]]:
    """
    Compute similarity matrix between all entities
    """

    try:

        matrix = {}

        for i, vec_a in enumerate(vectors):

            matrix[ids[i]] = {}

            for j, vec_b in enumerate(vectors):

                if i == j:
                    continue

                score = cosine_similarity(
                    vec_a,
                    vec_b
                )

                matrix[ids[i]][ids[j]] = score

        return matrix

    except Exception as e:

        logger.error(f"Similarity matrix error: {e}")

        return {}


# =========================
# THRESHOLD FILTER
# =========================

def filter_by_threshold(
    similarity_scores: List[Tuple[int, float]],
    threshold: float = 0.6
) -> List[Tuple[int, float]]:
    """
    Filter similarity results above threshold
    """

    try:

        filtered = [
            (entity_id, score)
            for entity_id, score in similarity_scores
            if score >= threshold
        ]

        return filtered

    except Exception as e:

        logger.error(f"Threshold filter error: {e}")

        return []


# =========================
# NORMALIZE SIMILARITY SCORES
# =========================

def normalize_scores(
    similarity_scores: List[Tuple[int, float]]
) -> List[Tuple[int, float]]:
    """
    Normalize similarity scores to 0–100
    """

    try:

        if not similarity_scores:
            return []

        max_score = max(
            score for _, score in similarity_scores
        )

        if max_score == 0:
            return similarity_scores

        normalized = [
            (
                entity_id,
                (score / max_score) * 100
            )
            for entity_id, score in similarity_scores
        ]

        return normalized

    except Exception as e:

        logger.error(f"Score normalization error: {e}")

        return []