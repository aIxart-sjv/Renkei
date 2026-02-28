"""
Embedding model wrapper

Provides:
- Load embedding model
- Save embedding model
- Generate embeddings
- Model persistence

Supports future fine-tuning and versioning
"""

import os
import numpy as np
from sentence_transformers import SentenceTransformer
from typing import List

from app.config import settings
from app.core.logger import get_logger


logger = get_logger(__name__)


class EmbeddingModel:
    """
    Wrapper around SentenceTransformer
    """

    def __init__(
        self,
        model_name: str = "all-MiniLM-L6-v2",
        model_path: str = None
    ):

        self.model_name = model_name
        self.model_path = model_path or settings.EMBEDDING_MODEL_PATH

        self.model = None

        self.load_model()


    # =========================
    # LOAD MODEL
    # =========================

    def load_model(self):
        """
        Load model from disk or pretrained source
        """

        try:

            if os.path.exists(self.model_path):

                logger.info(
                    f"Loading embedding model from {self.model_path}"
                )

                self.model = SentenceTransformer(
                    self.model_path
                )

            else:

                logger.info(
                    f"Loading pretrained model {self.model_name}"
                )

                self.model = SentenceTransformer(
                    self.model_name
                )

        except Exception as e:

            logger.error(f"Model loading failed: {e}")

            raise


    # =========================
    # SAVE MODEL
    # =========================

    def save_model(self):
        """
        Save model to disk
        """

        try:

            save_dir = os.path.dirname(
                self.model_path
            )

            os.makedirs(save_dir, exist_ok=True)

            self.model.save(self.model_path)

            logger.info(
                f"Embedding model saved to {self.model_path}"
            )

        except Exception as e:

            logger.error(f"Model save failed: {e}")


    # =========================
    # GENERATE EMBEDDING
    # =========================

    def encode(
        self,
        text: str
    ) -> np.ndarray:
        """
        Generate embedding vector
        """

        try:

            embedding = self.model.encode(
                text,
                normalize_embeddings=True
            )

            return embedding

        except Exception as e:

            logger.error(f"Encoding failed: {e}")

            return np.zeros(384)


    # =========================
    # BATCH ENCODE
    # =========================

    def batch_encode(
        self,
        texts: List[str]
    ) -> np.ndarray:
        """
        Generate embeddings for multiple texts
        """

        try:

            embeddings = self.model.encode(
                texts,
                normalize_embeddings=True
            )

            return embeddings

        except Exception as e:

            logger.error(f"Batch encoding failed: {e}")

            return np.zeros((len(texts), 384))


    # =========================
    # GET EMBEDDING DIMENSION
    # =========================

    def embedding_dimension(self) -> int:
        """
        Get embedding vector size
        """

        try:

            return self.model.get_sentence_embedding_dimension()

        except Exception:

            return 384


# =========================
# SINGLETON INSTANCE
# =========================

_embedding_model_instance = None


def get_embedding_model() -> EmbeddingModel:
    """
    Get global embedding model instance
    """

    global _embedding_model_instance

    if _embedding_model_instance is None:

        _embedding_model_instance = EmbeddingModel()

    return _embedding_model_instance