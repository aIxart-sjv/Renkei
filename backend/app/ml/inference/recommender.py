"""
ML + Graph hybrid recommendation engine

Combines:
- Embedding similarity
- Graph similarity
- Innovation score
- Influence score

Outputs ranked recommendations
"""

import numpy as np
from sqlalchemy.orm import Session
from typing import List, Dict

from app.core.logger import get_logger

from app.models.student import Student
from app.models.mentor import Mentor
from app.models.startup import Startup

from app.graph.builder import build_graph
from app.graph.similarity import structural_similarity_score
from app.graph.scorer import compute_recommendation_score

from app.ml.inference.embedder import (
    student_embedding,
    mentor_embedding,
    startup_embedding,
    cosine_similarity
)

from app.ml.inference.innovation_predictor import predict_innovation_score


logger = get_logger(__name__)


# =========================
# GET ENTITY EMBEDDING
# =========================

def get_embedding(entity):

    if isinstance(entity, Student):
        return student_embedding(entity)

    elif isinstance(entity, Mentor):
        return mentor_embedding(entity)

    elif isinstance(entity, Startup):
        return startup_embedding(entity)

    return None


# =========================
# RECOMMEND MENTORS
# =========================

def recommend_mentors(
    student: Student,
    mentors: List[Mentor],
    graph,
    db: Session,
    top_k: int = 10
):

    student_emb = student_embedding(student)

    recommendations = []

    for mentor in mentors:

        mentor_emb = mentor_embedding(mentor)

        emb_similarity = cosine_similarity(
            student_emb,
            mentor_emb
        )

        graph_similarity = structural_similarity_score(
            graph,
            student.id,
            mentor.id
        )

        innovation_score = predict_innovation_score(
            student,
            db
        )

        final_score = compute_recommendation_score(
            graph,
            student.id,
            mentor.id,
            emb_similarity
        )

        recommendations.append({
            "mentor_id": mentor.id,
            "score": final_score,
            "embedding_similarity": emb_similarity,
            "graph_similarity": graph_similarity,
            "innovation_score": innovation_score
        })


    recommendations.sort(
        key=lambda x: x["score"],
        reverse=True
    )

    return recommendations[:top_k]


# =========================
# RECOMMEND STARTUPS
# =========================

def recommend_startups(
    student: Student,
    startups: List[Startup],
    graph,
    db: Session,
    top_k: int = 10
):

    student_emb = student_embedding(student)

    recommendations = []

    for startup in startups:

        startup_emb = startup_embedding(startup)

        emb_similarity = cosine_similarity(
            student_emb,
            startup_emb
        )

        graph_similarity = structural_similarity_score(
            graph,
            student.id,
            startup.id
        )

        final_score = compute_recommendation_score(
            graph,
            student.id,
            startup.id,
            emb_similarity
        )

        recommendations.append({
            "startup_id": startup.id,
            "score": final_score,
            "embedding_similarity": emb_similarity,
            "graph_similarity": graph_similarity
        })


    recommendations.sort(
        key=lambda x: x["score"],
        reverse=True
    )

    return recommendations[:top_k]


# =========================
# RECOMMEND STUDENT COLLABORATORS
# =========================

def recommend_students(
    student: Student,
    students: List[Student],
    graph,
    db: Session,
    top_k: int = 10
):

    student_emb = student_embedding(student)

    recommendations = []

    for other in students:

        if other.id == student.id:
            continue

        other_emb = student_embedding(other)

        emb_similarity = cosine_similarity(
            student_emb,
            other_emb
        )

        graph_similarity = structural_similarity_score(
            graph,
            student.id,
            other.id
        )

        final_score = compute_recommendation_score(
            graph,
            student.id,
            other.id,
            emb_similarity
        )

        recommendations.append({
            "student_id": other.id,
            "score": final_score,
            "embedding_similarity": emb_similarity,
            "graph_similarity": graph_similarity
        })


    recommendations.sort(
        key=lambda x: x["score"],
        reverse=True
    )

    return recommendations[:top_k]


# =========================
# MAIN RECOMMEND FUNCTION
# =========================

def recommend_entities(
    student_id: int,
    db: Session,
    entity_type: str = None,
    top_k: int = 10
) -> Dict:
    """
    Main recommendation pipeline
    """

    student = db.query(Student).filter(
        Student.id == student_id
    ).first()

    if not student:

        logger.error("Student not found")

        return {}


    graph = build_graph(db)

    result = {}

    if entity_type is None or entity_type == "mentor":

        mentors = db.query(Mentor).all()

        result["mentors"] = recommend_mentors(
            student,
            mentors,
            graph,
            db,
            top_k
        )


    if entity_type is None or entity_type == "startup":

        startups = db.query(Startup).all()

        result["startups"] = recommend_startups(
            student,
            startups,
            graph,
            db,
            top_k
        )


    if entity_type is None or entity_type == "student":

        students = db.query(Student).all()

        result["students"] = recommend_students(
            student,
            students,
            graph,
            db,
            top_k
        )


    logger.info(f"Recommendations generated for student {student_id}")

    return result