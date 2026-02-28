from sqlalchemy.orm import Session
from typing import List, Optional

from app.models.achievement import Achievement
from app.schemas.achievement import (
    AchievementCreate,
    AchievementUpdate
)

from app.core.logger import get_logger


logger = get_logger(__name__)


# =========================
# CREATE ACHIEVEMENT
# =========================

def create_achievement(
    db: Session,
    achievement_data: AchievementCreate
) -> Achievement:
    """
    Create new achievement
    """

    try:

        achievement = Achievement(
            student_id=achievement_data.student_id,
            title=achievement_data.title,
            description=achievement_data.description,
            category=achievement_data.category,
            score=achievement_data.score,
            rank=achievement_data.rank,
            position=achievement_data.position,
            organization=achievement_data.organization,
            achievement_date=achievement_data.achievement_date
        )

        db.add(achievement)
        db.commit()
        db.refresh(achievement)

        logger.info(
            f"Achievement created: {achievement.id}"
        )

        return achievement

    except Exception as e:

        db.rollback()

        logger.error(
            f"Achievement creation failed: {e}"
        )

        raise


# =========================
# GET ACHIEVEMENT BY ID
# =========================

def get_achievement(
    db: Session,
    achievement_id: int
) -> Optional[Achievement]:
    """
    Get achievement by ID
    """

    return db.query(Achievement).filter(
        Achievement.id == achievement_id
    ).first()


# =========================
# GET STUDENT ACHIEVEMENTS
# =========================

def get_student_achievements(
    db: Session,
    student_id: int
) -> List[Achievement]:
    """
    Get all achievements of a student
    """

    return db.query(Achievement).filter(
        Achievement.student_id == student_id
    ).all()


# =========================
# GET ALL ACHIEVEMENTS
# =========================

def get_all_achievements(
    db: Session,
    skip: int = 0,
    limit: int = 100
) -> List[Achievement]:
    """
    Get all achievements
    """

    return db.query(Achievement).offset(skip).limit(limit).all()


# =========================
# UPDATE ACHIEVEMENT
# =========================

def update_achievement(
    db: Session,
    achievement_id: int,
    update_data: AchievementUpdate
) -> Optional[Achievement]:
    """
    Update achievement
    """

    achievement = get_achievement(
        db,
        achievement_id
    )

    if not achievement:
        return None


    try:

        update_fields = update_data.dict(
            exclude_unset=True
        )

        for field, value in update_fields.items():

            setattr(
                achievement,
                field,
                value
            )

        db.commit()
        db.refresh(achievement)

        logger.info(
            f"Achievement updated: {achievement.id}"
        )

        return achievement

    except Exception as e:

        db.rollback()

        logger.error(
            f"Achievement update failed: {e}"
        )

        raise


# =========================
# DELETE ACHIEVEMENT
# =========================

def delete_achievement(
    db: Session,
    achievement_id: int
) -> bool:
    """
    Delete achievement
    """

    achievement = get_achievement(
        db,
        achievement_id
    )

    if not achievement:
        return False


    try:

        db.delete(achievement)
        db.commit()

        logger.info(
            f"Achievement deleted: {achievement_id}"
        )

        return True

    except Exception as e:

        db.rollback()

        logger.error(
            f"Achievement deletion failed: {e}"
        )

        raise


# =========================
# GET TOP ACHIEVEMENTS
# =========================

def get_top_achievements(
    db: Session,
    limit: int = 10
) -> List[Achievement]:
    """
    Get highest scoring achievements
    """

    return db.query(Achievement)\
        .order_by(Achievement.score.desc())\
        .limit(limit)\
        .all()


# =========================
# CALCULATE STUDENT ACHIEVEMENT SCORE
# =========================

def calculate_student_achievement_score(
    db: Session,
    student_id: int
) -> float:
    """
    Calculate aggregated achievement score
    Used in ML feature engineering
    """

    achievements = get_student_achievements(
        db,
        student_id
    )

    if not achievements:
        return 0.0


    total_score = sum(
        a.score for a in achievements
    )

    avg_score = total_score / len(achievements)

    return avg_score