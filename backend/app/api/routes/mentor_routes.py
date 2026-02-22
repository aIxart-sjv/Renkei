from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models.mentor import Mentor
from app.schemas.mentor_schema import (
    MentorCreate,
    MentorUpdate,
    MentorResponse
)

router = APIRouter()


# -----------------------------------
# Create Mentor
# -----------------------------------
@router.post("/", response_model=MentorResponse)
def create_mentor(
    mentor: MentorCreate,
    db: Session = Depends(get_db)
):
    new_mentor = Mentor(
        name=mentor.name,
        email=mentor.email,
        expertise=mentor.expertise,
        organization=mentor.organization,
        designation=mentor.designation,
        bio=mentor.bio
    )

    db.add(new_mentor)
    db.commit()
    db.refresh(new_mentor)

    return new_mentor


# -----------------------------------
# Get All Mentors
# -----------------------------------
@router.get("/", response_model=List[MentorResponse])
def get_all_mentors(db: Session = Depends(get_db)):
    mentors = db.query(Mentor).all()
    return mentors


# -----------------------------------
# Get Mentor by ID
# -----------------------------------
@router.get("/{mentor_id}", response_model=MentorResponse)
def get_mentor(mentor_id: int, db: Session = Depends(get_db)):
    mentor = db.query(Mentor).filter(Mentor.id == mentor_id).first()

    if not mentor:
        raise HTTPException(
            status_code=404,
            detail="Mentor not found"
        )

    return mentor


# -----------------------------------
# Update Mentor
# -----------------------------------
@router.put("/{mentor_id}", response_model=MentorResponse)
def update_mentor(
    mentor_id: int,
    mentor_update: MentorUpdate,
    db: Session = Depends(get_db)
):
    mentor = db.query(Mentor).filter(Mentor.id == mentor_id).first()

    if not mentor:
        raise HTTPException(
            status_code=404,
            detail="Mentor not found"
        )

    update_data = mentor_update.dict(exclude_unset=True)

    for key, value in update_data.items():
        setattr(mentor, key, value)

    db.commit()
    db.refresh(mentor)

    return mentor


# -----------------------------------
# Delete Mentor
# -----------------------------------
@router.delete("/{mentor_id}")
def delete_mentor(mentor_id: int, db: Session = Depends(get_db)):
    mentor = db.query(Mentor).filter(Mentor.id == mentor_id).first()

    if not mentor:
        raise HTTPException(
            status_code=404,
            detail="Mentor not found"
        )

    db.delete(mentor)
    db.commit()

    return {"message": "Mentor deleted successfully"}