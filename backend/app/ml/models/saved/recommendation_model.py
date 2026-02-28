"""
Recommendation model wrapper

Handles:
- Train recommendation model
- Save model
- Load model
- Predict recommendation score

Supports ML-based ranking beyond cosine similarity
"""

import os
import numpy as np
import joblib

from sklearn.ensemble import GradientBoostingRegressor
from typing import Optional

from app.config import settings
from app.core.logger import get_logger


logger = get_logger(__name__)


class RecommendationModel:
    """
    ML model for ranking recommendations
    """

    def __init__(
        self,
        model_path: Optional[str] = None
    ):

        self.model_path = model_path or settings.RECOMMENDER_MODEL_PATH

        self.model = None

        self.load_model()


    # =========================
    # LOAD MODEL
    # =========================

    def load_model(self):
        """
        Load saved model if exists
        """

        try:

            if os.path.exists(self.model_path):

                logger.info(
                    f"Loading recommendation model from {self.model_path}"
                )

                self.model = joblib.load(
                    self.model_path
                )

            else:

                logger.warning(
                    "No saved recommendation model found. Creating new model."
                )

                self.model = self.create_model()

        except Exception as e:

            logger.error(f"Model load failed: {e}")

            self.model = self.create_model()


    # =========================
    # CREATE NEW MODEL
    # =========================

    def create_model(self):
        """
        Create Gradient Boosting model
        """

        return GradientBoostingRegressor(
            n_estimators=200,
            learning_rate=0.05,
            max_depth=5,
            random_state=42
        )


    # =========================
    # TRAIN MODEL
    # =========================

    def train(
        self,
        X: np.ndarray,
        y: np.ndarray
    ):
        """
        Train recommendation model
        """

        try:

            logger.info("Training recommendation model...")

            self.model.fit(X, y)

            logger.info("Recommendation model training complete")

        except Exception as e:

            logger.error(f"Training failed: {e}")


    # =========================
    # PREDICT SCORE
    # =========================

    def predict(
        self,
        features: np.ndarray
    ) -> float:
        """
        Predict recommendation ranking score
        """

        try:

            score = self.model.predict(
                features.reshape(1, -1)
            )[0]

            return float(score)

        except Exception as e:

            logger.error(f"Prediction failed: {e}")

            return 0.0


    # =========================
    # BATCH PREDICT
    # =========================

    def predict_batch(
        self,
        feature_matrix: np.ndarray
    ) -> np.ndarray:
        """
        Predict multiple scores
        """

        try:

            scores = self.model.predict(
                feature_matrix
            )

            return scores

        except Exception as e:

            logger.error(f"Batch prediction failed: {e}")

            return np.zeros(len(feature_matrix))


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

            joblib.dump(
                self.model,
                self.model_path
            )

            logger.info(
                f"Recommendation model saved to {self.model_path}"
            )

        except Exception as e:

            logger.error(f"Model save failed: {e}")


    # =========================
    # CHECK TRAINED
    # =========================

    def is_trained(self) -> bool:

        try:

            return hasattr(
                self.model,
                "estimators_"
            )

        except Exception:

            return False


# =========================
# SINGLETON INSTANCE
# =========================

_recommendation_model_instance = None


def get_recommendation_model() -> RecommendationModel:
    """
    Global recommendation model instance
    """

    global _recommendation_model_instance

    if _recommendation_model_instance is None:

        _recommendation_model_instance = RecommendationModel()

    return _recommendation_model_instance