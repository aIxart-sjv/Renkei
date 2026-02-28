"""
Compute Embeddings Script

Usage:
    python scripts/compute_embeddings.py

This script:
- Loads all entities from database
- Generates embeddings using embedding model
- Stores embeddings in database
"""

from app.db.session import SessionLocal

from app.models.student import Student
from app.models.mentor import Mentor
from app.models.alumni import Alumni
from app.models.startup import Startup
from app.models.embedding import Embedding

from app.ml.inference.embedder import generate_embedding

from app.utils.helpers import combine_text_fields

from app.core.logger import get_logger
import app.db.model_registry

logger = get_logger(__name__)


# =========================
# BUILD STUDENT TEXT
# =========================

def build_student_text(student):

    return combine_text_fields(
        student.skills,
        student.interests,
        student.university,
        student.degree,
        student.field_of_study,
        student.bio
    )


# =========================
# BUILD MENTOR TEXT
# =========================

def build_mentor_text(mentor):

    return combine_text_fields(
        mentor.skills,
        mentor.expertise,
        mentor.industry,
        mentor.current_company,
        mentor.current_role,
        mentor.bio
    )


# =========================
# BUILD ALUMNI TEXT
# =========================

def build_alumni_text(alumni):

    return combine_text_fields(
        alumni.skills,
        alumni.industry,
        alumni.current_company,
        alumni.current_role,
        alumni.bio
    )


# =========================
# BUILD STARTUP TEXT
# =========================

def build_startup_text(startup):

    return combine_text_fields(
        startup.name,
        startup.description,
        startup.domain,
        startup.industry,
        startup.tech_stack,
        startup.product_stage
    )


# =========================
# SAVE EMBEDDING
# =========================

def save_embedding(db, entity_id, entity_type, vector):

    embedding = db.query(Embedding).filter(
        Embedding.entity_id == entity_id,
        Embedding.entity_type == entity_type
    ).first()

    if not embedding:

        embedding = Embedding(
            entity_id=entity_id,
            entity_type=entity_type
        )

    embedding.set_vector(vector)

    db.add(embedding)
    db.commit()


# =========================
# PROCESS STUDENTS
# =========================

def process_students(db):

    students = db.query(Student).all()

    print(f"Processing {len(students)} students...")

    for student in students:

        text = build_student_text(student)

        if not text:
            continue

        vector = generate_embedding(text)

        save_embedding(
            db,
            student.id,
            "student",
            vector
        )


# =========================
# PROCESS MENTORS
# =========================

def process_mentors(db):

    mentors = db.query(Mentor).all()

    print(f"Processing {len(mentors)} mentors...")

    for mentor in mentors:

        text = build_mentor_text(mentor)

        if not text:
            continue

        vector = generate_embedding(text)

        save_embedding(
            db,
            mentor.id,
            "mentor",
            vector
        )


# =========================
# PROCESS ALUMNI
# =========================

def process_alumni(db):

    alumni_list = db.query(Alumni).all()

    print(f"Processing {len(alumni_list)} alumni...")

    for alumni in alumni_list:

        text = build_alumni_text(alumni)

        if not text:
            continue

        vector = generate_embedding(text)

        save_embedding(
            db,
            alumni.id,
            "alumni",
            vector
        )


# =========================
# PROCESS STARTUPS
# =========================

def process_startups(db):

    startups = db.query(Startup).all()

    print(f"Processing {len(startups)} startups...")

    for startup in startups:

        text = build_startup_text(startup)

        if not text:
            continue

        vector = generate_embedding(text)

        save_embedding(
            db,
            startup.id,
            "startup",
            vector
        )


# =========================
# MAIN
# =========================

def main():

    print("Computing embeddings...")

    db = SessionLocal()

    process_students(db)
    process_mentors(db)
    process_alumni(db)
    process_startups(db)

    db.close()

    print("Embeddings computed successfully.")


if __name__ == "__main__":
    main()