"""
Innovation prediction model wrapper

Handles:
- Load trained innovation model
- Save trained model
- Train model
- Predict innovation scores
"""

import os
import numpy as np
import joblib

from sklearn.ensemble import RandomForestRegressor
from typing import Optional

from app.config import settings
from app.core.logger import get_logger


logger = get_logger(__name__)


class InnovationModel:
    """
    ML model for predicting innovation score
    """

    def __init__(
        self,
        model_path: Optional[str] = None
    ):

        self.model_path = model_path or settings.INNOVATION_MODEL_PATH

        self.model = None

        self.load_model()


    # =========================
    # LOAD MODEL
    # =========================

    def load_model(self):
        """
        Load model from disk if exists
        """

        try:

            if os.path.exists(self.model_path):

                logger.info(
                    f"Loading innovation model from {self.model_path}"
                )

                self.model = joblib.load(
                    self.model_path
                )

            else:

                logger.warning(
                    "No saved innovation model found. Creating new model."
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
        Create new Random Forest model
        """

        return RandomForestRegressor(
            n_estimators=200,
            max_depth=10,
            random_state=42,
            n_jobs=-1
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
        Train innovation prediction model
        """

        try:

            logger.info("Training innovation model...")

            self.model.fit(X, y)

            logger.info("Innovation model training complete")

        except Exception as e:

            logger.error(f"Training failed: {e}")


    # =========================
    # PREDICT
    # =========================

    def predict(
        self,
        features: np.ndarray
    ) -> float:
        """
        Predict innovation score
        """

        try:

            prediction = self.model.predict(
                features.reshape(1, -1)
            )[0]

            return float(prediction)

        except Exception as e:

            logger.error(f"Prediction failed: {e}")

            return 0.0


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
                f"Innovation model saved to {self.model_path}"
            )

        except Exception as e:

            logger.error(f"Model save failed: {e}")


    # =========================
    # CHECK IF TRAINED
    # =========================

    def is_trained(self) -> bool:
        """
        Check if model is trained
        """

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

_innovation_model_instance = None


def get_innovation_model() -> InnovationModel:
    """
    Global innovation model instance
    """

    global _innovation_model_instance

    if _innovation_model_instance is None:

        _innovation_model_instance = InnovationModel()

    return _innovation_model_instance