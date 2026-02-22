from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.services.recommendation_service import RecommendationService
from app.models.student import Student

router = APIRouter()


# -----------------------------------
# Recommend Students (Peer Matching)
# -----------------------------------
@router.get("/students/{student_id}")
def recommend_students(
    student_id: int,
    db: Session = Depends(get_db)
):
    student = db.query(Student).filter(Student.id == student_id).first()

    if not student:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    recommendations = RecommendationService.recommend_students(student_id, db)

    return {
        "student_id": student_id,
        "recommended_students": recommendations
    }


# -----------------------------------
# Recommend Mentors
# -----------------------------------
@router.get("/mentors/{student_id}")
def recommend_mentors(
    student_id: int,
    db: Session = Depends(get_db)
):
    student = db.query(Student).filter(Student.id == student_id).first()

    if not student:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    recommendations = RecommendationService.recommend_mentors(student_id, db)

    return {
        "student_id": student_id,
        "recommended_mentors": recommendations
    }


# -----------------------------------
# Recommend Startups
# -----------------------------------
@router.get("/startups/{student_id}")
def recommend_startups(
    student_id: int,
    db: Session = Depends(get_db)
):
    student = db.query(Student).filter(Student.id == student_id).first()

    if not student:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    recommendations = RecommendationService.recommend_startups(student_id, db)

    return {
        "student_id": student_id,
        "recommended_startups": recommendations
    }


# -----------------------------------
# Full Recommendation Bundle
# -----------------------------------
@router.get("/full/{student_id}")
def full_recommendation(
    student_id: int,
    db: Session = Depends(get_db)
):
    student = db.query(Student).filter(Student.id == student_id).first()

    if not student:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    student_recs = RecommendationService.recommend_students(student_id, db)
    mentor_recs = RecommendationService.recommend_mentors(student_id, db)
    startup_recs = RecommendationService.recommend_startups(student_id, db)

    return {
        "student_id": student_id,
        "recommendations": {
            "students": student_recs,
            "mentors": mentor_recs,
            "startups": startup_recs
        }
    }