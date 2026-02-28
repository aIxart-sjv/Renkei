from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Dict

from app.dependencies import get_db, get_current_user, require_admin
from app.models.user import User
from app.models.student import Student
from app.models.mentor import Mentor

from app.ml.inference.embedder import generate_embedding
from app.ml.inference.recommender import recommend_entities
from app.ml.inference.innovation_predictor import predict_innovation_score

from app.ml.training.train_embedding import train_embedding_model
from app.ml.training.train_recommendation import train_recommendation_model
from app.ml.training.train_innovation_score import train_innovation_model


router = APIRouter()


# =========================
# GENERATE EMBEDDING
# =========================

@router.post("/embedding/student/{student_id}")
def generate_student_embedding(
    student_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Generate embedding vector for student

    Used in recommendation engine
    """

    student = db.query(Student).filter(
        Student.id == student_id
    ).first()

    if not student:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    text_data = f"{student.skills} {student.interests} {student.bio}"

    embedding = generate_embedding(text_data)

    return {
        "student_id": student_id,
        "embedding": embedding.tolist()
    }


# =========================
# PREDICT INNOVATION SCORE
# =========================

@router.get("/predict/innovation-score/{student_id}")
def predict_student_innovation_score(
    student_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    ML-based innovation score prediction
    """

    student = db.query(Student).filter(
        Student.id == student_id
    ).first()

    if not student:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    score = predict_innovation_score(student, db)

    return {
        "student_id": student_id,
        "predicted_innovation_score": score
    }


# =========================
# GET ML RECOMMENDATIONS
# =========================

@router.get("/recommend/student/{student_id}")
def get_ml_recommendations(
    student_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    ML-powered recommendation engine
    """

    student = db.query(Student).filter(
        Student.id == student_id
    ).first()

    if not student:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    recommendations = recommend_entities(
        student_id=student_id,
        db=db
    )

    return {
        "student_id": student_id,
        "recommendations": recommendations
    }


# =========================
# TRAIN EMBEDDING MODEL
# =========================

@router.post(
    "/train/embedding",
    status_code=status.HTTP_200_OK
)
def train_embedding(
    current_user: User = Depends(require_admin)
):
    """
    Train embedding model
    """

    train_embedding_model()

    return {
        "status": "embedding model trained"
    }


# =========================
# TRAIN RECOMMENDATION MODEL
# =========================

@router.post(
    "/train/recommendation",
    status_code=status.HTTP_200_OK
)
def train_recommendation(
    current_user: User = Depends(require_admin)
):
    """
    Train recommendation model
    """

    train_recommendation_model()

    return {
        "status": "recommendation model trained"
    }


# =========================
# TRAIN INNOVATION MODEL
# =========================

@router.post(
    "/train/innovation",
    status_code=status.HTTP_200_OK
)
def train_innovation(
    current_user: User = Depends(require_admin)
):
    """
    Train innovation score prediction model
    """

    train_innovation_model()

    return {
        "status": "innovation model trained"
    }