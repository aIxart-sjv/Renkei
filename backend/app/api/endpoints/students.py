from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.dependencies import get_db, get_current_user, require_admin
from app.models.student import Student
from app.models.user import User
from app.schemas.student import (
    StudentCreate,
    StudentUpdate,
    StudentResponse
)


router = APIRouter()


# =========================
# CREATE STUDENT PROFILE
# =========================

@router.post(
    "/",
    response_model=StudentResponse,
    status_code=status.HTTP_201_CREATED
)
def create_student(
    student_data: StudentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """
    Create student innovation profile

    This feeds ML embedding, scoring, and recommendation systems
    """

    student = Student(
        user_id=student_data.user_id,
        skills=student_data.skills,
        interests=student_data.interests,
        bio=student_data.bio,
        education=student_data.education,
        graduation_year=student_data.graduation_year,
        innovation_score=student_data.innovation_score,
        collaboration_score=student_data.collaboration_score
    )

    db.add(student)
    db.commit()
    db.refresh(student)

    return student


# =========================
# GET ALL STUDENTS
# =========================

@router.get(
    "/",
    response_model=List[StudentResponse]
)
def get_all_students(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Used by ML pipeline and graph intelligence builder
    """

    students = db.query(Student).all()

    return students


# =========================
# GET STUDENT BY ID
# =========================

@router.get(
    "/{student_id}",
    response_model=StudentResponse
)
def get_student(
    student_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    student = db.query(Student).filter(
        Student.id == student_id
    ).first()

    if not student:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    return student


# =========================
# UPDATE STUDENT PROFILE
# =========================

@router.put(
    "/{student_id}",
    response_model=StudentResponse
)
def update_student(
    student_id: int,
    student_update: StudentUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    student = db.query(Student).filter(
        Student.id == student_id
    ).first()

    if not student:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    update_data = student_update.dict(exclude_unset=True)

    for field, value in update_data.items():
        setattr(student, field, value)

    db.commit()
    db.refresh(student)

    return student


# =========================
# DELETE STUDENT PROFILE
# =========================

@router.delete(
    "/{student_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_student(
    student_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    student = db.query(Student).filter(
        Student.id == student_id
    ).first()

    if not student:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    db.delete(student)
    db.commit()

    return None


# =========================
# SEARCH STUDENTS BY SKILL
# =========================

@router.get(
    "/skill/{skill}",
    response_model=List[StudentResponse]
)
def get_students_by_skill(
    skill: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Used in recommendation filtering and graph analysis
    """

    students = db.query(Student).filter(
        Student.skills.ilike(f"%{skill}%")
    ).all()

    return students


# =========================
# SEARCH STUDENTS BY INTEREST
# =========================

@router.get(
    "/interest/{interest}",
    response_model=List[StudentResponse]
)
def get_students_by_interest(
    interest: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Used in ML similarity matching
    """

    students = db.query(Student).filter(
        Student.interests.ilike(f"%{interest}%")
    ).all()

    return students


# =========================
# GET TOP STUDENTS BY INNOVATION SCORE
# =========================

@router.get(
    "/top/innovators",
    response_model=List[StudentResponse]
)
def get_top_students(
    limit: int = 10,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Used for dashboard and ranking
    """

    students = db.query(Student).order_by(
        Student.innovation_score.desc()
    ).limit(limit).all()

    return students