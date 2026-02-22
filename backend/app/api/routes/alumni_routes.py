from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.schemas.mentor_schema import MentorCreate, MentorResponse, MentorUpdate
from app.models.alumni import Alumni


router = APIRouter()


# -----------------------------------
# Create Alumni Profile
# -----------------------------------
@router.post("/", response_model=MentorResponse)
def create_alumni(
    alumni: MentorCreate,
    db: Session = Depends(get_db)
):
    new_alumni = Alumni(
        name=alumni.name,
        email=alumni.email,
        expertise=alumni.expertise,
        organization=alumni.organization,
        designation=alumni.designation,
        bio=alumni.bio,
    )

    db.add(new_alumni)
    db.commit()
    db.refresh(new_alumni)

    return new_alumni


# -----------------------------------
# Get All Alumni
# -----------------------------------
@router.get("/", response_model=List[MentorResponse])
def get_all_alumni(
    db: Session = Depends(get_db)
):
    alumni_list = db.query(Alumni).all()
    return alumni_list


# -----------------------------------
# Get Alumni by ID
# -----------------------------------
@router.get("/{alumni_id}", response_model=MentorResponse)
def get_alumni(
    alumni_id: int,
    db: Session = Depends(get_db)
):
    alumni = db.query(Alumni).filter(Alumni.id == alumni_id).first()

    if not alumni:
        raise HTTPException(
            status_code=404,
            detail="Alumni not found"
        )

    return alumni


# -----------------------------------
# Update Alumni Profile
# -----------------------------------
@router.put("/{alumni_id}", response_model=MentorResponse)
def update_alumni(
    alumni_id: int,
    alumni_update: MentorUpdate,
    db: Session = Depends(get_db)
):
    alumni = db.query(Alumni).filter(Alumni.id == alumni_id).first()

    if not alumni:
        raise HTTPException(
            status_code=404,
            detail="Alumni not found"
        )

    update_data = alumni_update.dict(exclude_unset=True)

    for key, value in update_data.items():
        setattr(alumni, key, value)

    db.commit()
    db.refresh(alumni)

    return alumni


# -----------------------------------
# Delete Alumni Profile
# -----------------------------------
@router.delete("/{alumni_id}")
def delete_alumni(
    alumni_id: int,
    db: Session = Depends(get_db)
):
    alumni = db.query(Alumni).filter(Alumni.id == alumni_id).first()

    if not alumni:
        raise HTTPException(
            status_code=404,
            detail="Alumni not found"
        )

    db.delete(alumni)
    db.commit()

    return {"message": "Alumni deleted successfully"}