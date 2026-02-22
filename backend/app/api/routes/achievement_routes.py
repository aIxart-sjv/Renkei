from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.schemas.achievement_schema import (
    AchievementCreate,
    AchievementResponse,
)
from app.services.achievement_service import AchievementService

router = APIRouter()


# -----------------------------------
# Create Achievement
# -----------------------------------
@router.post("/", response_model=AchievementResponse)
def create_achievement(
    achievement: AchievementCreate,
    db: Session = Depends(get_db)
):
    new_achievement = AchievementService.create_achievement(achievement, db)
    return new_achievement


# -----------------------------------
# Get Achievements for a Student
# -----------------------------------
@router.get("/student/{student_id}", response_model=List[AchievementResponse])
def get_student_achievements(
    student_id: int,
    db: Session = Depends(get_db)
):
    achievements = AchievementService.get_student_achievements(student_id, db)

    if not achievements:
        raise HTTPException(
            status_code=404,
            detail="No achievements found for this student"
        )

    return achievements


# -----------------------------------
# Get Performance Score
# -----------------------------------
@router.get("/student/{student_id}/performance-score")
def get_performance_score(
    student_id: int,
    db: Session = Depends(get_db)
):
    score = AchievementService.calculate_performance_score(student_id, db)

    return {
        "student_id": student_id,
        "performance_score": score
    }


# -----------------------------------
# Get Performance Analysis
# -----------------------------------
@router.get("/student/{student_id}/analysis")
def get_performance_analysis(
    student_id: int,
    db: Session = Depends(get_db)
):
    analysis = AchievementService.analyze_performance(student_id, db)

    return {
        "student_id": student_id,
        "analysis": analysis
    }


# -----------------------------------
# Get Improvement Suggestions
# -----------------------------------
@router.get("/student/{student_id}/suggestions")
def get_improvement_suggestions(
    student_id: int,
    db: Session = Depends(get_db)
):
    suggestions = AchievementService.suggest_improvements(student_id, db)

    return {
        "student_id": student_id,
        "suggestions": suggestions
    }