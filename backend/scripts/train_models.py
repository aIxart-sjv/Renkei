"""
Train ML Models Script

Usage:
    python scripts/train_models.py

This script trains and saves:

1. Innovation score prediction model
2. Recommendation model
3. Embedding index

Saved to:
app/ml/models/saved/
"""

import os
import numpy as np

from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error

import joblib

from app.db.session import SessionLocal
import app.db.model_registry
from app.models.student import Student
from app.models.connection import Connection
from app.models.embedding import Embedding

from app.ml.utils.feature_engineering import (
    build_student_features
)

from app.core.logger import get_logger


logger = get_logger(__name__)


# =========================
# PATHS
# =========================

MODEL_DIR = "app/ml/models/saved"

INNOVATION_MODEL_PATH = os.path.join(
    MODEL_DIR,
    "innovation_model.pkl"
)

RECOMMENDATION_MODEL_PATH = os.path.join(
    MODEL_DIR,
    "recommendation_model.pkl"
)

EMBEDDING_INDEX_PATH = os.path.join(
    MODEL_DIR,
    "embedding_index.pkl"
)


os.makedirs(MODEL_DIR, exist_ok=True)


# =========================
# LOAD DATASET
# =========================

def load_student_dataset(db):

    students = db.query(Student).all()

    X = []
    y = []

    for student in students:

        features = build_student_features(
            student
        )

        if features is None:
            continue

        X.append(features)

        y.append(student.innovation_score or 0)

    return np.array(X), np.array(y)


# =========================
# TRAIN INNOVATION MODEL
# =========================

def train_innovation_model(db):

    print("Training innovation model...")

    X, y = load_student_dataset(db)

    if len(X) < 5:
        print("Not enough data to train innovation model")
        return None


    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42
    )


    model = RandomForestRegressor(
        n_estimators=100,
        max_depth=10,
        random_state=42
    )

    model.fit(X_train, y_train)

    predictions = model.predict(X_test)

    mse = mean_squared_error(y_test, predictions)

    print(f"Innovation Model MSE: {mse:.4f}")


    joblib.dump(
        model,
        INNOVATION_MODEL_PATH
    )

    print(f"Innovation model saved to {INNOVATION_MODEL_PATH}")

    return model


# =========================
# BUILD EMBEDDING INDEX
# =========================

def build_embedding_index(db):

    print("Building embedding index...")

    embeddings = db.query(Embedding).all()

    index = {}

    for emb in embeddings:

        vector = emb.get_vector()

        index[f"{emb.entity_type}:{emb.entity_id}"] = vector


    joblib.dump(
        index,
        EMBEDDING_INDEX_PATH
    )

    print(f"Embedding index saved to {EMBEDDING_INDEX_PATH}")

    return index


# =========================
# TRAIN RECOMMENDATION MODEL
# =========================

def train_recommendation_model(db):

    print("Training recommendation model...")

    connections = db.query(Connection).all()

    X = []
    y = []

    for conn in connections:

        X.append([
            conn.source_id,
            conn.target_id
        ])

        y.append(conn.strength)


    if len(X) < 5:
        print("Not enough data to train recommendation model")
        return None


    X = np.array(X)
    y = np.array(y)


    model = RandomForestRegressor(
        n_estimators=100,
        random_state=42
    )

    model.fit(X, y)


    joblib.dump(
        model,
        RECOMMENDATION_MODEL_PATH
    )

    print(f"Recommendation model saved to {RECOMMENDATION_MODEL_PATH}")

    return model


# =========================
# MAIN
# =========================

def main():

    print("Starting ML training pipeline...")

    db = SessionLocal()

    train_innovation_model(db)

    build_embedding_index(db)

    train_recommendation_model(db)

    db.close()

    print("ML training complete.")


if __name__ == "__main__":
    main()