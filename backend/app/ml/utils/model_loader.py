"""
Centralized ML model loader

Loads and manages:
- Embedding model
- Innovation prediction model
- Recommendation model

Provides singleton instances for efficiency
"""

import os
from typing import Optional

from app.config import settings
from app.core.logger import get_logger

from app.ml.models.saved.embedding_model import (
    EmbeddingModel
)

from app.ml.models.saved.innovation_model import (
    InnovationModel
)

from app.ml.models.saved.recommendation_model import (
    RecommendationModel
)


logger = get_logger(__name__)


# =========================
# SINGLETON INSTANCES
# =========================

_embedding_model: Optional[EmbeddingModel] = None
_innovation_model: Optional[InnovationModel] = None
_recommendation_model: Optional[RecommendationModel] = None


# =========================
# LOAD EMBEDDING MODEL
# =========================

def load_embedding_model() -> EmbeddingModel:
    """
    Load embedding model singleton
    """

    global _embedding_model

    if _embedding_model is None:

        try:

            logger.info("Loading embedding model...")

            _embedding_model = EmbeddingModel(
                model_path=settings.EMBEDDING_MODEL_PATH
            )

            logger.info("Embedding model loaded")

        except Exception as e:

            logger.error(f"Embedding model load failed: {e}")

            raise

    return _embedding_model


# =========================
# LOAD INNOVATION MODEL
# =========================

def load_innovation_model() -> InnovationModel:
    """
    Load innovation prediction model singleton
    """

    global _innovation_model

    if _innovation_model is None:

        try:

            logger.info("Loading innovation model...")

            _innovation_model = InnovationModel(
                model_path=settings.INNOVATION_MODEL_PATH
            )

            logger.info("Innovation model loaded")

        except Exception as e:

            logger.error(f"Innovation model load failed: {e}")

            raise

    return _innovation_model


# =========================
# LOAD RECOMMENDATION MODEL
# =========================

def load_recommendation_model() -> RecommendationModel:
    """
    Load recommendation model singleton
    """

    global _recommendation_model

    if _recommendation_model is None:

        try:

            logger.info("Loading recommendation model...")

            _recommendation_model = RecommendationModel(
                model_path=settings.RECOMMENDER_MODEL_PATH
            )

            logger.info("Recommendation model loaded")

        except Exception as e:

            logger.error(f"Recommendation model load failed: {e}")

            raise

    return _recommendation_model


# =========================
# LOAD ALL MODELS
# =========================

def load_all_models():
    """
    Load all ML models at startup
    """

    logger.info("Loading all ML models...")

    load_embedding_model()
    load_innovation_model()
    load_recommendation_model()

    logger.info("All ML models loaded")


# =========================
# CHECK MODEL EXISTS
# =========================

def model_exists(model_path: str) -> bool:
    """
    Check if trained model exists
    """

    return os.path.exists(model_path)


# =========================
# CHECK ALL MODELS STATUS
# =========================

def models_status():
    """
    Returns availability of models
    """

    return {
        "embedding_model": model_exists(
            settings.EMBEDDING_MODEL_PATH
        ),

        "innovation_model": model_exists(
            settings.INNOVATION_MODEL_PATH
        ),

        "recommendation_model": model_exists(
            settings.RECOMMENDER_MODEL_PATH
        )
    }