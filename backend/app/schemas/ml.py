from pydantic import BaseModel, Field
from typing import List, Optional


# =========================
# EMBEDDING SCHEMA
# =========================

class EmbeddingRequest(BaseModel):
    """
    Request to generate embedding
    """

    text: str = Field(
        ...,
        description="Text to embed"
    )


class EmbeddingResponse(BaseModel):
    """
    Embedding result
    """

    vector: List[float]

    dimension: int


# =========================
# INNOVATION SCORE PREDICTION
# =========================

class InnovationPredictionRequest(BaseModel):
    """
    Request to predict innovation score
    """

    entity_id: int

    entity_type: str = Field(
        ...,
        description="student, mentor, alumni, startup"
    )


class InnovationPredictionResponse(BaseModel):
    """
    Innovation score prediction result
    """

    entity_id: int

    entity_type: str

    predicted_score: float


# =========================
# RECOMMENDATION SCHEMA
# =========================

class RecommendationRequest(BaseModel):
    """
    Request recommendations
    """

    entity_id: int

    entity_type: str

    target_type: str = Field(
        ...,
        description="student, mentor, startup"
    )

    top_k: Optional[int] = Field(
        default=10,
        ge=1,
        le=100
    )


class RecommendationItem(BaseModel):
    """
    Single recommendation item
    """

    entity_id: int

    entity_type: str

    score: float


class RecommendationResponse(BaseModel):
    """
    Recommendation results
    """

    source_id: int

    source_type: str

    recommendations: List[RecommendationItem]


# =========================
# SIMILARITY RESPONSE
# =========================

class SimilarityResponse(BaseModel):

    source_id: int

    target_id: int

    similarity_score: float


# =========================
# MODEL STATUS RESPONSE
# =========================

class ModelStatus(BaseModel):

    embedding_model_loaded: bool

    innovation_model_loaded: bool

    recommendation_model_loaded: bool


# =========================
# TRAINING RESPONSE
# =========================

class TrainingResponse(BaseModel):

    message: str

    success: bool


# =========================
# VECTOR SEARCH RESPONSE
# =========================

class VectorSearchResult(BaseModel):

    entity_id: int

    entity_type: str

    similarity_score: float


class VectorSearchResponse(BaseModel):

    results: List[VectorSearchResult]