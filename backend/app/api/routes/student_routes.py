from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models.student import Student
from app.schemas.student_schema import (
    StudentCreate,
    StudentUpdate,
    StudentResponse
)

router = APIRouter()


# -----------------------------------
# Create Student Profile
# -----------------------------------
@router.post("/", response_model=StudentResponse)
def create_student(
    student: StudentCreate,
    db: Session = Depends(get_db)
):
    # Check if email already exists
    existing_student = db.query(Student).filter(Student.email == student.email).first()

    if existing_student:
        raise HTTPException(
            status_code=400,
            detail="Student with this email already exists"
        )

    new_student = Student(
        name=student.name,
        email=student.email,
        skills=student.skills,
        interests=student.interests,
        bio=student.bio
    )

    db.add(new_student)
    db.commit()
    db.refresh(new_student)

    return new_student


# -----------------------------------
# Get All Students
# -----------------------------------
@router.get("/", response_model=List[StudentResponse])
def get_all_students(db: Session = Depends(get_db)):
    students = db.query(Student).all()
    return students


# -----------------------------------
# Get Student by ID
# -----------------------------------
@router.get("/{student_id}", response_model=StudentResponse)
def get_student(
    student_id: int,
    db: Session = Depends(get_db)
):
    student = db.query(Student).filter(Student.id == student_id).first()

    if not student:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    return student


# -----------------------------------
# Update Student
# -----------------------------------
@router.put("/{student_id}", response_model=StudentResponse)
def update_student(
    student_id: int,
    student_update: StudentUpdate,
    db: Session = Depends(get_db)
):
    student = db.query(Student).filter(Student.id == student_id).first()

    if not student:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    update_data = student_update.dict(exclude_unset=True)

    for key, value in update_data.items():
        setattr(student, key, value)

    db.commit()
    db.refresh(student)

    return student


# -----------------------------------
# Delete Student
# -----------------------------------
@router.delete("/{student_id}")
def delete_student(
    student_id: int,
    db: Session = Depends(get_db)
):
    student = db.query(Student).filter(Student.id == student_id).first()

    if not student:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    db.delete(student)
    db.commit()

    return {"message": "Student deleted successfully"}


# -----------------------------------
# Search Students by Skill or Interest
# -----------------------------------
@router.get("/search/{query}")
def search_students(
    query: str,
    db: Session = Depends(get_db)
):
    students = db.query(Student).all()

    results = []

    for student in students:
        skills = " ".join(student.skills).lower()
        interests = " ".join(student.interests).lower()

        if query.lower() in skills or query.lower() in interests:
            results.append(student)

    return results