"""
Compute Scores Script

Usage:
    python scripts/compute_scores.py

This script:
- Loads graph from database
- Computes innovation scores
- Computes collaboration scores
- Computes influence scores
- Updates database
"""

from app.db.session import SessionLocal

from app.models.student import Student
from app.models.mentor import Mentor
from app.models.alumni import Alumni
from app.models.startup import Startup

from app.services.scoring_service import (
    update_student_innovation_score,
    update_student_collaboration_score,
    update_student_influence_score
)

from app.graph.builder import build_graph
from app.graph.centrality import composite_centrality_score
from app.graph.pagerank import compute_pagerank, normalize_pagerank

from app.core.logger import get_logger
import app.db.model_registry

logger = get_logger(__name__)


# =========================
# UPDATE STUDENT SCORES
# =========================

def update_students(db):

    students = db.query(Student).all()

    print(f"Updating {len(students)} students...")

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

        print(
            f"Student {student.id}: "
            f"innovation={innovation}, "
            f"collaboration={collaboration}, "
            f"influence={influence}"
        )


# =========================
# UPDATE MENTOR SCORES
# =========================

def update_mentors(db):

    mentors = db.query(Mentor).all()

    graph = build_graph(db)

    pagerank = normalize_pagerank(
        compute_pagerank(graph)
    )

    print(f"Updating {len(mentors)} mentors...")

    for mentor in mentors:

        score = pagerank.get(mentor.id, 0.0)

        mentor.mentorship_score = score

        db.commit()

        print(
            f"Mentor {mentor.id}: mentorship_score={score}"
        )


# =========================
# UPDATE STARTUP SCORES
# =========================

def update_startups(db):

    startups = db.query(Startup).all()

    graph = build_graph(db)

    pagerank = normalize_pagerank(
        compute_pagerank(graph)
    )

    print(f"Updating {len(startups)} startups...")

    for startup in startups:

        score = pagerank.get(startup.id, 0.0)

        startup.innovation_score = score

        db.commit()

        print(
            f"Startup {startup.id}: innovation_score={score}"
        )


# =========================
# UPDATE ALUMNI SCORES
# =========================

def update_alumni(db):

    alumni_list = db.query(Alumni).all()

    graph = build_graph(db)

    pagerank = normalize_pagerank(
        compute_pagerank(graph)
    )

    print(f"Updating {len(alumni_list)} alumni...")

    for alumni in alumni_list:

        score = pagerank.get(alumni.id, 0.0)

        db.commit()

        print(
            f"Alumni {alumni.id}: influence_score={score}"
        )


# =========================
# PRINT SUMMARY
# =========================

def print_summary(db):

    students = db.query(Student).count()
    mentors = db.query(Mentor).count()
    alumni = db.query(Alumni).count()
    startups = db.query(Startup).count()

    print("\nScore computation complete:")
    print(f"Students: {students}")
    print(f"Mentors: {mentors}")
    print(f"Alumni: {alumni}")
    print(f"Startups: {startups}")


# =========================
# MAIN
# =========================

def main():

    print("Computing innovation scores...")

    db = SessionLocal()

    update_students(db)
    update_mentors(db)
    update_startups(db)
    update_alumni(db)

    print_summary(db)

    db.close()

    print("Done.")


if __name__ == "__main__":
    main()