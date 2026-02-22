from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.schemas.startup_schema import (
    StartupCreate,
    StartupUpdate,
    StartupResponse
)
from app.services.startup_service import StartupService
from app.models.startup import Startup

router = APIRouter()


# -----------------------------------
# Create Startup
# -----------------------------------
@router.post("/", response_model=StartupResponse)
def create_startup(
    startup: StartupCreate,
    db: Session = Depends(get_db)
):
    new_startup = StartupService.create_startup(startup, db)
    return new_startup


# -----------------------------------
# Get All Startups
# -----------------------------------
@router.get("/", response_model=List[StartupResponse])
def get_all_startups(db: Session = Depends(get_db)):
    startups = StartupService.get_all_startups(db)
    return startups


# -----------------------------------
# Get Startup by ID
# -----------------------------------
@router.get("/{startup_id}", response_model=StartupResponse)
def get_startup(
    startup_id: int,
    db: Session = Depends(get_db)
):
    startup = StartupService.get_startup_by_id(startup_id, db)

    if not startup:
        raise HTTPException(
            status_code=404,
            detail="Startup not found"
        )

    return startup


# -----------------------------------
# Update Startup
# -----------------------------------
@router.put("/{startup_id}", response_model=StartupResponse)
def update_startup(
    startup_id: int,
    startup_update: StartupUpdate,
    db: Session = Depends(get_db)
):
    startup = db.query(Startup).filter(Startup.id == startup_id).first()

    if not startup:
        raise HTTPException(
            status_code=404,
            detail="Startup not found"
        )

    update_data = startup_update.dict(exclude_unset=True)

    for key, value in update_data.items():
        setattr(startup, key, value)

    db.commit()
    db.refresh(startup)

    return startup


# -----------------------------------
# Delete Startup
# -----------------------------------
@router.delete("/{startup_id}")
def delete_startup(
    startup_id: int,
    db: Session = Depends(get_db)
):
    startup = db.query(Startup).filter(Startup.id == startup_id).first()

    if not startup:
        raise HTTPException(
            status_code=404,
            detail="Startup not found"
        )

    db.delete(startup)
    db.commit()

    return {"message": "Startup deleted successfully"}


# -----------------------------------
# Get Top Promoted Startups (InnoVenture Core)
# -----------------------------------
@router.get("/promoted/top")
def get_promoted_startups(
    limit: int = 5,
    db: Session = Depends(get_db)
):
    promoted = StartupService.promote_startups(db, limit)

    return {
        "message": "Top promoted startups fetched successfully",
        "startups": promoted
    }


# -----------------------------------
# Get Startups by Domain (Investor Matching)
# -----------------------------------
@router.get("/domain/{domain}")
def get_startups_by_domain(
    domain: str,
    db: Session = Depends(get_db)
):
    startups = StartupService.get_startups_by_domain(domain, db)

    return {
        "domain": domain,
        "startups": startups
    }