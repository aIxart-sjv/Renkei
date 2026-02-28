from sqlalchemy.orm import Session
from typing import List, Dict, Any

from app.core.logger import get_logger

from app.models.student import Student
from app.models.mentor import Mentor
from app.models.startup import Startup
from app.models.alumni import Alumni

from app.services.ml_service import (
    get_entity_embedding,
    compute_entity_similarity
)

from app.services.graph_service import (
    get_graph
)

from app.ml.inference.recommender import recommend_entities


logger = get_logger(__name__)


# =========================
# GENERIC RECOMMENDATION
# =========================

def recommend(
    db: Session,
    entity_id: int,
    entity_type: str,
    target_type: str,
    top_k: int = 10
) -> List[Dict[str, Any]]:
    """
    ML-based recommendation
    """

    results = recommend_entities(
        db=db,
        entity_id=entity_id,
        entity_type=entity_type,
        target_type=target_type,
        top_k=top_k
    )

    return results


# =========================
# RECOMMEND MENTORS FOR STUDENT
# =========================

def recommend_mentors_for_student(
    db: Session,
    student_id: int,
    top_k: int = 10
) -> List[Dict[str, Any]]:

    mentors = db.query(Mentor).filter(
        Mentor.available == True
    ).all()

    results = []

    for mentor in mentors:

        similarity = compute_entity_similarity(
            db,
            student_id,
            "student",
            mentor.id,
            "mentor"
        )

        results.append({
            "entity_id": mentor.id,
            "entity_type": "mentor",
            "score": similarity
        })

    results.sort(
        key=lambda x: x["score"],
        reverse=True
    )

    return results[:top_k]


# =========================
# RECOMMEND STARTUPS FOR STUDENT
# =========================

def recommend_startups_for_student(
    db: Session,
    student_id: int,
    top_k: int = 10
) -> List[Dict[str, Any]]:

    startups = db.query(Startup).all()

    results = []

    for startup in startups:

        similarity = compute_entity_similarity(
            db,
            student_id,
            "student",
            startup.id,
            "startup"
        )

        results.append({
            "entity_id": startup.id,
            "entity_type": "startup",
            "score": similarity
        })

    results.sort(
        key=lambda x: x["score"],
        reverse=True
    )

    return results[:top_k]


# =========================
# RECOMMEND STUDENTS
# =========================

def recommend_students(
    db: Session,
    student_id: int,
    top_k: int = 10
) -> List[Dict[str, Any]]:

    students = db.query(Student).filter(
        Student.id != student_id
    ).all()

    results = []

    for student in students:

        similarity = compute_entity_similarity(
            db,
            student_id,
            "student",
            student.id,
            "student"
        )

        results.append({
            "entity_id": student.id,
            "entity_type": "student",
            "score": similarity
        })

    results.sort(
        key=lambda x: x["score"],
        reverse=True
    )

    return results[:top_k]


# =========================
# RECOMMEND ALUMNI
# =========================

def recommend_alumni(
    db: Session,
    student_id: int,
    top_k: int = 10
) -> List[Dict[str, Any]]:

    alumni_list = db.query(Alumni).all()

    results = []

    for alumni in alumni_list:

        similarity = compute_entity_similarity(
            db,
            student_id,
            "student",
            alumni.id,
            "alumni"
        )

        results.append({
            "entity_id": alumni.id,
            "entity_type": "alumni",
            "score": similarity
        })

    results.sort(
        key=lambda x: x["score"],
        reverse=True
    )

    return results[:top_k]


# =========================
# FULL RECOMMENDATION
# =========================

def full_recommendation(
    db: Session,
    student_id: int,
    top_k: int = 5
) -> Dict[str, List[Dict[str, Any]]]:
    """
    Combined ecosystem recommendations
    """

    return {
        "students": recommend_students(db, student_id, top_k),
        "mentors": recommend_mentors_for_student(db, student_id, top_k),
        "startups": recommend_startups_for_student(db, student_id, top_k),
        "alumni": recommend_alumni(db, student_id, top_k)
    }