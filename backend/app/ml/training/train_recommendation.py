"""
Train Recommendation Ranking Model

Uses dataset built from:
- Embedding similarity
- Graph similarity
- Collaboration score
- Connection strength labels

Trains and saves recommendation model
"""

import numpy as np
from sqlalchemy.orm import Session
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score

from app.db.session import SessionLocal
from app.core.logger import get_logger

from app.ml.training.dataset_builder import (
    build_recommendation_dataset
)

from app.ml.models.saved.recommendation_model import (
    get_recommendation_model
)


logger = get_logger(__name__)


# =========================
# TRAIN RECOMMENDATION MODEL
# =========================

def train_recommendation_model():

    logger.info("Starting recommendation model training...")

    db: Session = SessionLocal()

    try:

        # =========================
        # BUILD DATASET
        # =========================

        X, y = build_recommendation_dataset(db)

        if len(X) == 0:

            logger.error("No recommendation training data")

            return


        logger.info(f"Dataset size: {len(X)} samples")


        # =========================
        # TRAIN TEST SPLIT
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

        model = get_recommendation_model()


        # =========================
        # TRAIN MODEL
        # =========================

        model.train(X_train, y_train)


        # =========================
        # EVALUATE MODEL
        # =========================

        predictions = model.predict_batch(X_test)

        mse = mean_squared_error(y_test, predictions)

        r2 = r2_score(y_test, predictions)


        logger.info(f"Recommendation Model MSE: {mse:.4f}")
        logger.info(f"Recommendation Model R2: {r2:.4f}")


        # =========================
        # SAVE MODEL
        # =========================

        model.save_model()


        logger.info("Recommendation model training complete")


    finally:

        db.close()


# =========================
# CLI ENTRY POINT
# =========================

if __name__ == "__main__":

    train_recommendation_model()