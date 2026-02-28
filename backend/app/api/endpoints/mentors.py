from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.dependencies import get_db, get_current_user, require_admin
from app.models.mentor import Mentor
from app.models.user import User
from app.schemas.mentor import (
    MentorCreate,
    MentorUpdate,
    MentorResponse
)


router = APIRouter()


# =========================
# CREATE MENTOR
# =========================

@router.post(
    "/",
    response_model=MentorResponse,
    status_code=status.HTTP_201_CREATED
)
def create_mentor(
    mentor_data: MentorCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """
    Create mentor profile

    Used in ML recommendation and graph intelligence
    """

    mentor = Mentor(
        user_id=mentor_data.user_id,
        expertise=mentor_data.expertise,
        industry=mentor_data.industry,
        years_of_experience=mentor_data.years_of_experience,
        current_company=mentor_data.current_company,
        current_role=mentor_data.current_role,
        bio=mentor_data.bio,
        availability=mentor_data.availability
    )

    db.add(mentor)
    db.commit()
    db.refresh(mentor)

    return mentor


# =========================
# GET ALL MENTORS
# =========================

@router.get(
    "/",
    response_model=List[MentorResponse]
)
def get_all_mentors(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Used by recommendation engine and graph builder
    """

    mentors = db.query(Mentor).all()

    return mentors


# =========================
# GET MENTOR BY ID
# =========================

@router.get(
    "/{mentor_id}",
    response_model=MentorResponse
)
def get_mentor(
    mentor_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    mentor = db.query(Mentor).filter(
        Mentor.id == mentor_id
    ).first()

    if not mentor:
        raise HTTPException(
            status_code=404,
            detail="Mentor not found"
        )

    return mentor


# =========================
# UPDATE MENTOR
# =========================

@router.put(
    "/{mentor_id}",
    response_model=MentorResponse
)
def update_mentor(
    mentor_id: int,
    mentor_update: MentorUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    mentor = db.query(Mentor).filter(
        Mentor.id == mentor_id
    ).first()

    if not mentor:
        raise HTTPException(
            status_code=404,
            detail="Mentor not found"
        )

    update_data = mentor_update.dict(exclude_unset=True)

    for field, value in update_data.items():
        setattr(mentor, field, value)

    db.commit()
    db.refresh(mentor)

    return mentor


# =========================
# DELETE MENTOR
# =========================

@router.delete(
    "/{mentor_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_mentor(
    mentor_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    mentor = db.query(Mentor).filter(
        Mentor.id == mentor_id
    ).first()

    if not mentor:
        raise HTTPException(
            status_code=404,
            detail="Mentor not found"
        )

    db.delete(mentor)
    db.commit()

    return None


# =========================
# GET MENTORS BY INDUSTRY
# =========================

@router.get(
    "/industry/{industry}",
    response_model=List[MentorResponse]
)
def get_mentors_by_industry(
    industry: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Used by ML recommendation engine
    """

    mentors = db.query(Mentor).filter(
        Mentor.industry.ilike(f"%{industry}%")
    ).all()

    return mentors


# =========================
# GET AVAILABLE MENTORS
# =========================

@router.get(
    "/available/list",
    response_model=List[MentorResponse]
)
def get_available_mentors(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Used for real-time recommendation filtering
    """

    mentors = db.query(Mentor).filter(
        Mentor.availability == True
    ).all()

    return mentors