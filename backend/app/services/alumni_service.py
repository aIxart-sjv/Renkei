from sqlalchemy.orm import Session
from typing import List, Optional

from app.models.alumni import Alumni
from app.schemas.alumni import (
    AlumniCreate,
    AlumniUpdate
)

from app.core.logger import get_logger


logger = get_logger(__name__)


# =========================
# CREATE ALUMNI PROFILE
# =========================

def create_alumni(
    db: Session,
    alumni_data: AlumniCreate
) -> Alumni:
    """
    Create alumni profile
    """

    try:

        alumni = Alumni(
            user_id=alumni_data.user_id,
            current_company=alumni_data.current_company,
            current_role=alumni_data.current_role,
            industry=alumni_data.industry,
            years_of_experience=alumni_data.years_of_experience,
            graduation_year=alumni_data.graduation_year,
            degree=alumni_data.degree,
            field_of_study=alumni_data.field_of_study,
            bio=alumni_data.bio,
            skills=alumni_data.skills,
            linkedin_url=alumni_data.linkedin_url,
            portfolio_url=alumni_data.portfolio_url,
            available_for_mentorship=alumni_data.available_for_mentorship
        )

        db.add(alumni)
        db.commit()
        db.refresh(alumni)

        logger.info(
            f"Alumni created: {alumni.id}"
        )

        return alumni

    except Exception as e:

        db.rollback()

        logger.error(
            f"Alumni creation failed: {e}"
        )

        raise


# =========================
# GET ALUMNI BY ID
# =========================

def get_alumni(
    db: Session,
    alumni_id: int
) -> Optional[Alumni]:

    return db.query(Alumni).filter(
        Alumni.id == alumni_id
    ).first()


# =========================
# GET ALUMNI BY USER ID
# =========================

def get_alumni_by_user(
    db: Session,
    user_id: int
) -> Optional[Alumni]:

    return db.query(Alumni).filter(
        Alumni.user_id == user_id
    ).first()


# =========================
# GET ALL ALUMNI
# =========================

def get_all_alumni(
    db: Session,
    skip: int = 0,
    limit: int = 100
) -> List[Alumni]:

    return db.query(Alumni)\
        .offset(skip)\
        .limit(limit)\
        .all()


# =========================
# UPDATE ALUMNI
# =========================

def update_alumni(
    db: Session,
    alumni_id: int,
    update_data: AlumniUpdate
) -> Optional[Alumni]:

    alumni = get_alumni(
        db,
        alumni_id
    )

    if not alumni:
        return None


    try:

        update_fields = update_data.dict(
            exclude_unset=True
        )

        for field, value in update_fields.items():

            setattr(
                alumni,
                field,
                value
            )

        db.commit()
        db.refresh(alumni)

        logger.info(
            f"Alumni updated: {alumni.id}"
        )

        return alumni

    except Exception as e:

        db.rollback()

        logger.error(
            f"Alumni update failed: {e}"
        )

        raise


# =========================
# DELETE ALUMNI
# =========================

def delete_alumni(
    db: Session,
    alumni_id: int
) -> bool:

    alumni = get_alumni(
        db,
        alumni_id
    )

    if not alumni:
        return False


    try:

        db.delete(alumni)
        db.commit()

        logger.info(
            f"Alumni deleted: {alumni_id}"
        )

        return True

    except Exception as e:

        db.rollback()

        logger.error(
            f"Alumni deletion failed: {e}"
        )

        raise


# =========================
# GET AVAILABLE MENTORS (ALUMNI)
# =========================

def get_available_alumni_mentors(
    db: Session
) -> List[Alumni]:
    """
    Get alumni available for mentorship
    """

    return db.query(Alumni).filter(
        Alumni.available_for_mentorship == True
    ).all()


# =========================
# SEARCH ALUMNI BY INDUSTRY
# =========================

def search_alumni_by_industry(
    db: Session,
    industry: str
) -> List[Alumni]:

    return db.query(Alumni).filter(
        Alumni.industry.ilike(f"%{industry}%")
    ).all()