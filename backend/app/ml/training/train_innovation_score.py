"""
Train Innovation Score Prediction Model

Uses dataset built from:
- Graph metrics
- Achievements
- Embeddings

Trains and saves ML model
"""

import os
import numpy as np
from sqlalchemy.orm import Session
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score

from app.db.session import SessionLocal
from app.core.logger import get_logger
from app.config import settings

from app.ml.training.dataset_builder import (
    build_innovation_dataset
)

from app.ml.models.saved.innovation_model import (
    get_innovation_model
)


logger = get_logger(__name__)


# =========================
# TRAIN MODEL
# =========================

def train_innovation_model():

    logger.info("Starting innovation model training...")

    db: Session = SessionLocal()

    try:

        # =========================
        # BUILD DATASET
        # =========================

        X, y = build_innovation_dataset(db)

        if len(X) == 0:

            logger.error("No training data available")

            return


        logger.info(f"Dataset size: {len(X)} samples")


        # =========================
        # SPLIT DATA
        # =========================

        X_train, X_test, y_train, y_test = train_test_split(
            X,
            y,
            test_size=0.2,
            random_state=42
        )


        # =========================
        # LOAD MODEL
        # =========================

        model = get_innovation_model()


        # =========================
        # TRAIN
        # =========================

        model.train(X_train, y_train)


        # =========================
        # EVALUATE
        # =========================

        predictions = []

        for features in X_test:

            pred = model.predict(features)

            predictions.append(pred)

        predictions = np.array(predictions)


        mse = mean_squared_error(y_test, predictions)
        r2 = r2_score(y_test, predictions)


        logger.info(f"MSE: {mse:.4f}")
        logger.info(f"R2 Score: {r2:.4f}")


        # =========================
        # SAVE MODEL
        # =========================

        model.save_model()


        logger.info("Innovation model training complete")


    finally:

        db.close()


# =========================
# CLI ENTRY POINT
# =========================

if __name__ == "__main__":

    train_innovation_model()