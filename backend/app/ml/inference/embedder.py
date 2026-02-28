"""
Embedding engine using Sentence Transformers

Converts text into dense vector embeddings for:
- Students (skills, interests, bio)
- Mentors (expertise, industry, bio)
- Startups (description, tech stack, domain)

These embeddings power ML recommendations.
"""

from sentence_transformers import SentenceTransformer
import numpy as np
from typing import List, Union

from app.core.logger import get_logger


logger = get_logger(__name__)


# =========================
# LOAD MODEL (Singleton)
# =========================

_model = None


def get_model() -> SentenceTransformer:
    """
    Lazy load embedding model
    """

    global _model

    if _model is None:

        logger.info("Loading embedding model...")

        _model = SentenceTransformer(
            "all-MiniLM-L6-v2"
        )

        logger.info("Embedding model loaded")

    return _model


# =========================
# GENERATE SINGLE EMBEDDING
# =========================

def generate_embedding(
    text: str
) -> np.ndarray:
    """
    Convert text to embedding vector
    """

    try:

        model = get_model()

        embedding = model.encode(
            text,
            normalize_embeddings=True
        )

        return embedding

    except Exception as e:

        logger.error(f"Embedding generation failed: {e}")

        return np.zeros(384)


# =========================
# GENERATE MULTIPLE EMBEDDINGS
# =========================

def generate_embeddings(
    texts: List[str]
) -> np.ndarray:
    """
    Batch embedding generation
    """

    try:

        model = get_model()

        embeddings = model.encode(
            texts,
            normalize_embeddings=True
        )

        return embeddings

    except Exception as e:

        logger.error(f"Batch embedding failed: {e}")

        return np.zeros((len(texts), 384))


# =========================
# BUILD STUDENT EMBEDDING
# =========================

def student_embedding(student) -> np.ndarray:
    """
    Create embedding from student profile
    """

    text = f"""
    Skills: {student.skills}
    Interests: {student.interests}
    Bio: {student.bio}
    """

    return generate_embedding(text)


# =========================
# BUILD MENTOR EMBEDDING
# =========================

def mentor_embedding(mentor) -> np.ndarray:
    """
    Create embedding from mentor profile
    """

    text = f"""
    Expertise: {mentor.expertise}
    Industry: {mentor.industry}
    Bio: {mentor.bio}
    """

    return generate_embedding(text)


# =========================
# BUILD STARTUP EMBEDDING
# =========================

def startup_embedding(startup) -> np.ndarray:
    """
    Create embedding from startup profile
    """

    text = f"""
    Name: {startup.name}
    Description: {startup.description}
    Domain: {startup.domain}
    Tech stack: {startup.tech_stack}
    """

    return generate_embedding(text)


# =========================
# COSINE SIMILARITY
# =========================

def cosine_similarity(
    emb1: np.ndarray,
    emb2: np.ndarray
) -> float:
    """
    Compute cosine similarity between embeddings
    """

    try:

        similarity = np.dot(emb1, emb2)

        return float(similarity)

    except Exception as e:

        logger.error(f"Similarity computation failed: {e}")

        return 0.0


# =========================
# FIND MOST SIMILAR
# =========================

def find_most_similar(
    query_embedding: np.ndarray,
    candidate_embeddings: List[np.ndarray],
    top_k: int = 10
):
    """
    Find top similar embeddings
    """

    try:

        similarities = []

        for i, emb in enumerate(candidate_embeddings):

            score = cosine_similarity(
                query_embedding,
                emb
            )

            similarities.append((i, score))

        similarities.sort(
            key=lambda x: x[1],
            reverse=True
        )

        return similarities[:top_k]

    except Exception as e:

        logger.error(f"Similarity search failed: {e}")

        return []