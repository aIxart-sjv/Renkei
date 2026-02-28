from sqlalchemy.orm import Session
from typing import List, Optional

from app.models.student import Student
from app.schemas.student import (
    StudentCreate,
    StudentUpdate
)

from app.core.logger import get_logger

from app.services.scoring_service import (
    update_student_innovation_score,
    update_student_collaboration_score,
    update_student_influence_score
)

from app.services.ml_service import (
    generate_entity_embedding
)


logger = get_logger(__name__)


# =========================
# CREATE STUDENT
# =========================

def create_student(
    db: Session,
    student_data: StudentCreate
) -> Student:
    """
    Create student profile
    """

    try:

        student = Student(
            user_id=student_data.user_id,
            university=student_data.university,
            degree=student_data.degree,
            field_of_study=student_data.field_of_study,
            graduation_year=student_data.graduation_year,
            skills=student_data.skills,
            interests=student_data.interests,
            bio=student_data.bio,
            linkedin_url=student_data.linkedin_url,
            github_url=student_data.github_url,
            portfolio_url=student_data.portfolio_url,
            is_active=student_data.is_active
        )

        db.add(student)
        db.commit()
        db.refresh(student)

        logger.info(f"Student created: {student.id}")


        # Generate embedding for ML
        embedding_text = build_student_embedding_text(student)

        generate_entity_embedding(
            db,
            student.id,
            "student",
            embedding_text
        )


        # Initialize scores
        update_student_innovation_score(db, student.id)
        update_student_collaboration_score(db, student.id)
        update_student_influence_score(db, student.id)


        return student


    except Exception as e:

        db.rollback()

        logger.error(f"Student creation failed: {e}")

        raise


# =========================
# GET STUDENT BY ID
# =========================

def get_student(
    db: Session,
    student_id: int
) -> Optional[Student]:

    return db.query(Student).filter(
        Student.id == student_id
    ).first()


# =========================
# GET STUDENT BY USER ID
# =========================

def get_student_by_user(
    db: Session,
    user_id: int
) -> Optional[Student]:

    return db.query(Student).filter(
        Student.user_id == user_id
    ).first()


# =========================
# GET ALL STUDENTS
# =========================

def get_all_students(
    db: Session,
    skip: int = 0,
    limit: int = 100
) -> List[Student]:

    return db.query(Student)\
        .offset(skip)\
        .limit(limit)\
        .all()


# =========================
# UPDATE STUDENT
# =========================

def update_student(
    db: Session,
    student_id: int,
    update_data: StudentUpdate
) -> Optional[Student]:

    student = get_student(
        db,
        student_id
    )

    if not student:
        return None


    try:

        update_fields = update_data.dict(
            exclude_unset=True
        )

        for field, value in update_fields.items():

            setattr(student, field, value)


        db.commit()
        db.refresh(student)

        logger.info(f"Student updated: {student.id}")


        # Regenerate embedding
        embedding_text = build_student_embedding_text(student)

        generate_entity_embedding(
            db,
            student.id,
            "student",
            embedding_text
        )


        # Recalculate scores
        update_student_innovation_score(db, student.id)
        update_student_collaboration_score(db, student.id)
        update_student_influence_score(db, student.id)


        return student


    except Exception as e:

        db.rollback()

        logger.error(f"Student update failed: {e}")

        raise


# =========================
# DELETE STUDENT
# =========================

def delete_student(
    db: Session,
    student_id: int
) -> bool:

    student = get_student(db, student_id)

    if not student:
        return False


    try:

        db.delete(student)
        db.commit()

        logger.info(f"Student deleted: {student_id}")

        return True

    except Exception as e:

        db.rollback()

        logger.error(f"Student deletion failed: {e}")

        raise


# =========================
# GET TOP STUDENTS
# =========================

def get_top_students(
    db: Session,
    limit: int = 10
) -> List[Student]:
    """
    Ranked by innovation score
    """

    return db.query(Student)\
        .order_by(Student.innovation_score.desc())\
        .limit(limit)\
        .all()


# =========================
# SEARCH STUDENTS BY SKILLS
# =========================

def search_students_by_skill(
    db: Session,
    skill: str
) -> List[Student]:

    return db.query(Student).filter(
        Student.skills.ilike(f"%{skill}%")
    ).all()


# =========================
# BUILD EMBEDDING TEXT
# =========================

def build_student_embedding_text(
    student: Student
) -> str:
    """
    Build text representation for embedding model
    """

    parts = [
        student.skills or "",
        student.interests or "",
        student.university or "",
        student.degree or "",
        student.field_of_study or "",
        student.bio or ""
    ]

    return " ".join(parts)