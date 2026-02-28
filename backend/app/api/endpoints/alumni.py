from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.dependencies import get_db, get_current_user, require_admin
from app.models.alumni import Alumni
from app.models.user import User
from app.schemas.alumni import (
    AlumniCreate,
    AlumniUpdate,
    AlumniResponse
)


router = APIRouter()


# =========================
# CREATE ALUMNI
# =========================

@router.post(
    "/",
    response_model=AlumniResponse,
    status_code=status.HTTP_201_CREATED
)
def create_alumni(
    alumni_data: AlumniCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """
    Create new alumni profile

    Alumni act as high-value nodes in innovation graph
    """

    alumni = Alumni(
        user_id=alumni_data.user_id,
        graduation_year=alumni_data.graduation_year,
        degree=alumni_data.degree,
        field_of_study=alumni_data.field_of_study,
        current_company=alumni_data.current_company,
        current_role=alumni_data.current_role,
        industry=alumni_data.industry,
        expertise=alumni_data.expertise,
        bio=alumni_data.bio
    )

    db.add(alumni)
    db.commit()
    db.refresh(alumni)

    return alumni


# =========================
# GET ALL ALUMNI
# =========================

@router.get(
    "/",
    response_model=List[AlumniResponse]
)
def get_all_alumni(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get all alumni

    Used by recommendation engine and graph builder
    """

    alumni_list = db.query(Alumni).all()

    return alumni_list


# =========================
# GET ALUMNI BY ID
# =========================

@router.get(
    "/{alumni_id}",
    response_model=AlumniResponse
)
def get_alumni(
    alumni_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    alumni = db.query(Alumni).filter(
        Alumni.id == alumni_id
    ).first()

    if not alumni:
        raise HTTPException(
            status_code=404,
            detail="Alumni not found"
        )

    return alumni


# =========================
# UPDATE ALUMNI
# =========================

@router.put(
    "/{alumni_id}",
    response_model=AlumniResponse
)
def update_alumni(
    alumni_id: int,
    alumni_update: AlumniUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    alumni = db.query(Alumni).filter(
        Alumni.id == alumni_id
    ).first()

    if not alumni:
        raise HTTPException(
            status_code=404,
            detail="Alumni not found"
        )

    update_data = alumni_update.dict(exclude_unset=True)

    for field, value in update_data.items():
        setattr(alumni, field, value)

    db.commit()
    db.refresh(alumni)

    return alumni


# =========================
# DELETE ALUMNI
# =========================

@router.delete(
    "/{alumni_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_alumni(
    alumni_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    alumni = db.query(Alumni).filter(
        Alumni.id == alumni_id
    ).first()

    if not alumni:
        raise HTTPException(
            status_code=404,
            detail="Alumni not found"
        )

    db.delete(alumni)
    db.commit()

    return None


# =========================
# GET ALUMNI BY INDUSTRY
# =========================

@router.get(
    "/industry/{industry}",
    response_model=List[AlumniResponse]
)
def get_alumni_by_industry(
    industry: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Used by ML recommendation engine
    to find industry-specific mentors/advisors
    """

    alumni_list = db.query(Alumni).filter(
        Alumni.industry.ilike(f"%{industry}%")
    ).all()

    return alumni_list