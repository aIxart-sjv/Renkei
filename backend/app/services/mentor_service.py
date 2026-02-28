from sqlalchemy.orm import Session
from typing import List, Optional

from app.models.mentor import Mentor
from app.schemas.mentor import MentorCreate, MentorUpdate

from app.core.logger import get_logger


logger = get_logger(__name__)


# =========================
# CREATE MENTOR
# =========================

def create_mentor(
    db: Session,
    mentor_data: MentorCreate
) -> Mentor:
    """
    Create mentor profile
    """

    try:

        mentor = Mentor(
            user_id=mentor_data.user_id,
            current_company=mentor_data.current_company,
            current_role=mentor_data.current_role,
            industry=mentor_data.industry,
            years_of_experience=mentor_data.years_of_experience,
            expertise=mentor_data.expertise,
            skills=mentor_data.skills,
            bio=mentor_data.bio,
            mentorship_score=mentor_data.mentorship_score,
            total_mentees=mentor_data.total_mentees,
            available=mentor_data.available,
            linkedin_url=mentor_data.linkedin_url,
            portfolio_url=mentor_data.portfolio_url
        )

        db.add(mentor)
        db.commit()
        db.refresh(mentor)

        logger.info(f"Mentor created: {mentor.id}")

        return mentor

    except Exception as e:

        db.rollback()

        logger.error(f"Mentor creation failed: {e}")

        raise


# =========================
# GET MENTOR BY ID
# =========================

def get_mentor(
    db: Session,
    mentor_id: int
) -> Optional[Mentor]:

    return db.query(Mentor).filter(
        Mentor.id == mentor_id
    ).first()


# =========================
# GET MENTOR BY USER ID
# =========================

def get_mentor_by_user(
    db: Session,
    user_id: int
) -> Optional[Mentor]:

    return db.query(Mentor).filter(
        Mentor.user_id == user_id
    ).first()


# =========================
# GET ALL MENTORS
# =========================

def get_all_mentors(
    db: Session,
    skip: int = 0,
    limit: int = 100
) -> List[Mentor]:

    return db.query(Mentor)\
        .offset(skip)\
        .limit(limit)\
        .all()


# =========================
# GET AVAILABLE MENTORS
# =========================

def get_available_mentors(
    db: Session
) -> List[Mentor]:
    """
    Used by recommendation engine
    """

    return db.query(Mentor).filter(
        Mentor.available == True
    ).all()


# =========================
# UPDATE MENTOR
# =========================

def update_mentor(
    db: Session,
    mentor_id: int,
    update_data: MentorUpdate
) -> Optional[Mentor]:

    mentor = get_mentor(
        db,
        mentor_id
    )

    if not mentor:
        return None


    try:

        update_fields = update_data.dict(
            exclude_unset=True
        )

        for field, value in update_fields.items():

            setattr(mentor, field, value)

        db.commit()
        db.refresh(mentor)

        logger.info(f"Mentor updated: {mentor.id}")

        return mentor

    except Exception as e:

        db.rollback()

        logger.error(f"Mentor update failed: {e}")

        raise


# =========================
# DELETE MENTOR
# =========================

def delete_mentor(
    db: Session,
    mentor_id: int
) -> bool:

    mentor = get_mentor(db, mentor_id)

    if not mentor:
        return False


    try:

        db.delete(mentor)
        db.commit()

        logger.info(f"Mentor deleted: {mentor_id}")

        return True

    except Exception as e:

        db.rollback()

        logger.error(f"Mentor deletion failed: {e}")

        raise


# =========================
# SEARCH MENTORS BY SKILL
# =========================

def search_mentors_by_skill(
    db: Session,
    skill: str
) -> List[Mentor]:
    """
    Used in recommendation engine
    """

    return db.query(Mentor).filter(
        Mentor.skills.ilike(f"%{skill}%")
    ).all()


# =========================
# GET TOP MENTORS
# =========================

def get_top_mentors(
    db: Session,
    limit: int = 10
) -> List[Mentor]:
    """
    Ranked by mentorship score
    """

    return db.query(Mentor)\
        .order_by(Mentor.mentorship_score.desc())\
        .limit(limit)\
        .all()


# =========================
# UPDATE MENTORSHIP SCORE
# =========================

def update_mentorship_score(
    db: Session,
    mentor_id: int,
    score: float
) -> Optional[Mentor]:
    """
    Used by ML pipeline
    """

    mentor = get_mentor(db, mentor_id)

    if not mentor:
        return None


    mentor.mentorship_score = score

    db.commit()
    db.refresh(mentor)

    return mentor