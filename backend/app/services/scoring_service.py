from sqlalchemy.orm import Session
from typing import Dict, Any

from app.core.logger import get_logger

from app.models.student import Student
from app.models.mentor import Mentor
from app.models.startup import Startup
from app.models.alumni import Alumni

from app.services.achievement_service import (
    calculate_student_achievement_score
)

from app.services.graph_service import (
    get_graph
)

from app.graph.centrality import composite_centrality_score
from app.graph.pagerank import compute_pagerank, normalize_pagerank


logger = get_logger(__name__)


# =========================
# CALCULATE STUDENT INNOVATION SCORE
# =========================

def calculate_student_innovation_score(
    db: Session,
    student_id: int
) -> float:
    """
    Combine graph intelligence + achievements
    """

    student = db.query(Student).filter(
        Student.id == student_id
    ).first()

    if not student:
        return 0.0


    graph = get_graph(db)

    pagerank = normalize_pagerank(
        compute_pagerank(graph)
    )

    centrality = composite_centrality_score(
        graph
    )

    achievement_score = calculate_student_achievement_score(
        db,
        student_id
    )


    pagerank_score = pagerank.get(student_id, 0.0)
    centrality_score = centrality.get(student_id, 0.0)


    # Weighted innovation score formula
    innovation_score = (
        0.4 * achievement_score +
        0.3 * pagerank_score +
        0.3 * centrality_score
    )


    return round(innovation_score, 4)


# =========================
# UPDATE STUDENT INNOVATION SCORE
# =========================

def update_student_innovation_score(
    db: Session,
    student_id: int
) -> float:

    score = calculate_student_innovation_score(
        db,
        student_id
    )

    student = db.query(Student).filter(
        Student.id == student_id
    ).first()

    if not student:
        return 0.0


    student.innovation_score = score

    db.commit()

    logger.info(
        f"Student innovation score updated: {student_id} = {score}"
    )

    return score


# =========================
# UPDATE ALL STUDENTS SCORES
# =========================

def update_all_student_scores(
    db: Session
) -> Dict[int, float]:

    students = db.query(Student).all()

    results = {}

    for student in students:

        score = calculate_student_innovation_score(
            db,
            student.id
        )

        student.innovation_score = score

        results[student.id] = score


    db.commit()

    logger.info(
        "All student innovation scores updated"
    )

    return results


# =========================
# CALCULATE COLLABORATION SCORE
# =========================

def calculate_collaboration_score(
    db: Session,
    entity_id: int
) -> float:

    graph = get_graph(db)

    if entity_id not in graph:
        return 0.0


    degree = graph.degree(entity_id)

    total_nodes = graph.number_of_nodes()

    if total_nodes == 0:
        return 0.0


    score = degree / total_nodes

    return round(score, 4)


# =========================
# UPDATE STUDENT COLLABORATION SCORE
# =========================

def update_student_collaboration_score(
    db: Session,
    student_id: int
) -> float:

    score = calculate_collaboration_score(
        db,
        student_id
    )

    student = db.query(Student).filter(
        Student.id == student_id
    ).first()

    if not student:
        return 0.0


    student.collaboration_score = score

    db.commit()

    return score


# =========================
# CALCULATE INFLUENCE SCORE
# =========================

def calculate_influence_score(
    db: Session,
    entity_id: int
) -> float:

    graph = get_graph(db)

    pagerank = normalize_pagerank(
        compute_pagerank(graph)
    )

    return round(
        pagerank.get(entity_id, 0.0),
        4
    )


# =========================
# UPDATE STUDENT INFLUENCE SCORE
# =========================

def update_student_influence_score(
    db: Session,
    student_id: int
) -> float:

    score = calculate_influence_score(
        db,
        student_id
    )

    student = db.query(Student).filter(
        Student.id == student_id
    ).first()

    if not student:
        return 0.0


    student.influence_score = score

    db.commit()

    return score


# =========================
# UPDATE ALL SCORING METRICS
# =========================

def update_all_scores(
    db: Session
) -> Dict[str, Any]:
    """
    Update innovation, collaboration, influence scores
    """

    students = db.query(Student).all()

    results = {}

    for student in students:

        innovation = update_student_innovation_score(
            db,
            student.id
        )

        collaboration = update_student_collaboration_score(
            db,
            student.id
        )

        influence = update_student_influence_score(
            db,
            student.id
        )

        results[student.id] = {
            "innovation_score": innovation,
            "collaboration_score": collaboration,
            "influence_score": influence
        }


    logger.info(
        "All scoring metrics updated"
    )

    return results