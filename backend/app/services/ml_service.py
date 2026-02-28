from sqlalchemy.orm import Session
from typing import List, Dict, Any

from app.core.logger import get_logger

from app.ml.inference.embedder import generate_embedding
from app.ml.inference.innovation_predictor import predict_innovation_score
from app.ml.inference.recommender import recommend_entities
from app.ml.inference.similarity import compute_similarity

from app.ml.utils.model_loader import (
    load_embedding_model,
    load_innovation_model,
    load_recommendation_model
)

from app.models.embedding import Embedding


logger = get_logger(__name__)


# =========================
# MODEL STATUS
# =========================

def get_model_status() -> Dict[str, bool]:
    """
    Check if ML models are loaded
    """

    embedding_model = load_embedding_model()
    innovation_model = load_innovation_model()
    recommendation_model = load_recommendation_model()

    return {
        "embedding_model_loaded": embedding_model is not None,
        "innovation_model_loaded": innovation_model is not None,
        "recommendation_model_loaded": recommendation_model is not None
    }


# =========================
# GENERATE EMBEDDING
# =========================

def generate_entity_embedding(
    db: Session,
    entity_id: int,
    entity_type: str,
    text: str
) -> List[float]:
    """
    Generate and store embedding
    """

    vector = generate_embedding(text)

    # Save to DB
    embedding = db.query(Embedding).filter(
        Embedding.entity_id == entity_id,
        Embedding.entity_type == entity_type
    ).first()

    if not embedding:

        embedding = Embedding(
            entity_id=entity_id,
            entity_type=entity_type
        )

    embedding.set_vector(vector)

    db.add(embedding)
    db.commit()

    logger.info(
        f"Embedding generated for {entity_type}:{entity_id}"
    )

    return vector


# =========================
# GET EMBEDDING FROM DB
# =========================

def get_entity_embedding(
    db: Session,
    entity_id: int,
    entity_type: str
) -> List[float]:

    embedding = db.query(Embedding).filter(
        Embedding.entity_id == entity_id,
        Embedding.entity_type == entity_type
    ).first()

    if not embedding:
        return []

    return embedding.get_vector()


# =========================
# PREDICT INNOVATION SCORE
# =========================

def predict_entity_innovation(
    db: Session,
    entity_id: int,
    entity_type: str,
    features: List[float]
) -> float:
    """
    Predict innovation score using ML model
    """

    score = predict_innovation_score(features)

    logger.info(
        f"Innovation score predicted: {entity_type}:{entity_id} = {score}"
    )

    return score


# =========================
# GET RECOMMENDATIONS
# =========================

def get_ml_recommendations(
    db: Session,
    entity_id: int,
    entity_type: str,
    target_type: str,
    top_k: int = 10
) -> List[Dict[str, Any]]:
    """
    ML-based recommendation inference
    """

    recommendations = recommend_entities(
        db=db,
        entity_id=entity_id,
        entity_type=entity_type,
        target_type=target_type,
        top_k=top_k
    )

    logger.info(
        f"Recommendations generated for {entity_type}:{entity_id}"
    )

    return recommendations


# =========================
# COMPUTE SIMILARITY
# =========================

def compute_entity_similarity(
    db: Session,
    entity1_id: int,
    entity1_type: str,
    entity2_id: int,
    entity2_type: str
) -> float:
    """
    Compute similarity between two entities
    """

    vec1 = get_entity_embedding(
        db,
        entity1_id,
        entity1_type
    )

    vec2 = get_entity_embedding(
        db,
        entity2_id,
        entity2_type
    )

    if not vec1 or not vec2:
        return 0.0

    similarity = compute_similarity(
        vec1,
        vec2
    )

    return similarity


# =========================
# VECTOR SEARCH
# =========================

def vector_search(
    db: Session,
    query_vector: List[float],
    entity_type: str,
    top_k: int = 10
) -> List[Dict[str, Any]]:
    """
    Find similar entities using embeddings
    """

    embeddings = db.query(Embedding).filter(
        Embedding.entity_type == entity_type
    ).all()

    results = []

    for embedding in embeddings:

        vector = embedding.get_vector()

        score = compute_similarity(
            query_vector,
            vector
        )

        results.append({
            "entity_id": embedding.entity_id,
            "entity_type": entity_type,
            "similarity_score": score
        })


    results.sort(
        key=lambda x: x["similarity_score"],
        reverse=True
    )

    return results[:top_k]