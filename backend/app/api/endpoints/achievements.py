from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.dependencies import get_db, get_current_user
from app.models.achievement import Achievement
from app.models.student import Student
from app.schemas.achievement import (
    AchievementCreate,
    AchievementUpdate,
    AchievementResponse
)
from app.models.user import User


router = APIRouter()


# =========================
# CREATE ACHIEVEMENT
# =========================

@router.post(
    "/",
    response_model=AchievementResponse,
    status_code=status.HTTP_201_CREATED
)
def create_achievement(
    achievement_data: AchievementCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Create new achievement for student

    This feeds ML scoring and innovation intelligence
    """

    # Validate student exists
    student = db.query(Student).filter(
        Student.id == achievement_data.student_id
    ).first()

    if not student:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    achievement = Achievement(
        student_id=achievement_data.student_id,
        title=achievement_data.title,
        description=achievement_data.description,
        achievement_type=achievement_data.achievement_type,
        score=achievement_data.score,
        metadata=achievement_data.metadata
    )

    db.add(achievement)
    db.commit()
    db.refresh(achievement)

    return achievement


# =========================
# GET ALL ACHIEVEMENTS
# =========================

@router.get(
    "/",
    response_model=List[AchievementResponse]
)
def get_all_achievements(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get all achievements

    Used for analytics and ML training
    """

    achievements = db.query(Achievement).all()

    return achievements


# =========================
# GET ACHIEVEMENT BY ID
# =========================

@router.get(
    "/{achievement_id}",
    response_model=AchievementResponse
)
def get_achievement(
    achievement_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    achievement = db.query(Achievement).filter(
        Achievement.id == achievement_id
    ).first()

    if not achievement:
        raise HTTPException(
            status_code=404,
            detail="Achievement not found"
        )

    return achievement


# =========================
# GET STUDENT ACHIEVEMENTS
# =========================

@router.get(
    "/student/{student_id}",
    response_model=List[AchievementResponse]
)
def get_student_achievements(
    student_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get all achievements of a student

    Used by ML scoring engine
    """

    achievements = db.query(Achievement).filter(
        Achievement.student_id == student_id
    ).all()

    return achievements


# =========================
# UPDATE ACHIEVEMENT
# =========================

@router.put(
    "/{achievement_id}",
    response_model=AchievementResponse
)
def update_achievement(
    achievement_id: int,
    achievement_update: AchievementUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    achievement = db.query(Achievement).filter(
        Achievement.id == achievement_id
    ).first()

    if not achievement:
        raise HTTPException(
            status_code=404,
            detail="Achievement not found"
        )

    # Update fields
    for field, value in achievement_update.dict(
        exclude_unset=True
    ).items():
        setattr(achievement, field, value)

    db.commit()
    db.refresh(achievement)

    return achievement


# =========================
# DELETE ACHIEVEMENT
# =========================

@router.delete(
    "/{achievement_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_achievement(
    achievement_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    achievement = db.query(Achievement).filter(
        Achievement.id == achievement_id
    ).first()

    if not achievement:
        raise HTTPException(
            status_code=404,
            detail="Achievement not found"
        )

    db.delete(achievement)
    db.commit()

    return None