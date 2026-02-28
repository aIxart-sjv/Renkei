from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Dict

from app.dependencies import get_db, get_current_user
from app.models.student import Student
from app.models.mentor import Mentor
from app.models.startup import Startup
from app.models.user import User

from app.ml.inference.recommender import recommend_entities
from app.ml.inference.embedder import generate_embedding
from app.ml.inference.innovation_predictor import predict_innovation_score

from app.graph.builder import build_graph
from app.graph.algorithms import compute_centrality


router = APIRouter()


# =========================
# FULL RECOMMENDATION PIPELINE
# =========================

@router.get("/student/{student_id}")
def recommend_for_student(
    student_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Core ML + Graph recommendation endpoint
    """

    student = db.query(Student).filter(
        Student.id == student_id
    ).first()

    if not student:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )


    # =========================
    # ML RECOMMENDATIONS
    # =========================

    ml_recommendations = recommend_entities(
        student_id=student_id,
        db=db
    )


    # =========================
    # GRAPH CENTRALITY
    # =========================

    graph = build_graph(db)

    centrality_scores = compute_centrality(graph)

    student_centrality = centrality_scores.get(student_id, 0)


    # =========================
    # INNOVATION SCORE
    # =========================

    innovation_score = predict_innovation_score(
        student=student,
        db=db
    )


    return {
        "student_id": student_id,

        "innovation_score": innovation_score,

        "graph_centrality": student_centrality,

        "recommendations": ml_recommendations
    }


# =========================
# RECOMMEND MENTORS ONLY
# =========================

@router.get("/student/{student_id}/mentors")
def recommend_mentors(
    student_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    recommendations = recommend_entities(
        student_id=student_id,
        db=db,
        entity_type="mentor"
    )

    return recommendations


# =========================
# RECOMMEND STARTUPS ONLY
# =========================

@router.get("/student/{student_id}/startups")
def recommend_startups(
    student_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    recommendations = recommend_entities(
        student_id=student_id,
        db=db,
        entity_type="startup"
    )

    return recommendations


# =========================
# RECOMMEND COLLABORATORS
# =========================

@router.get("/student/{student_id}/collaborators")
def recommend_collaborators(
    student_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    recommendations = recommend_entities(
        student_id=student_id,
        db=db,
        entity_type="student"
    )

    return recommendations


# =========================
# TOP INNOVATORS
# =========================

@router.get("/top-innovators")
def get_top_innovators(
    limit: int = 10,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Uses ML innovation prediction to rank students
    """

    students = db.query(Student).all()

    scored_students = []

    for student in students:

        score = predict_innovation_score(
            student=student,
            db=db
        )

        scored_students.append({
            "student_id": student.id,
            "innovation_score": score
        })


    scored_students.sort(
        key=lambda x: x["innovation_score"],
        reverse=True
    )

    return scored_students[:limit]