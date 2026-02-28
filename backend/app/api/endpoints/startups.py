from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.dependencies import get_db, get_current_user, require_admin
from app.models.startup import Startup
from app.models.user import User
from app.schemas.startup import (
    StartupCreate,
    StartupUpdate,
    StartupResponse
)


router = APIRouter()


# =========================
# CREATE STARTUP
# =========================

@router.post(
    "/",
    response_model=StartupResponse,
    status_code=status.HTTP_201_CREATED
)
def create_startup(
    startup_data: StartupCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """
    Create startup profile

    Used in ML recommendation and graph intelligence
    """

    startup = Startup(
        name=startup_data.name,
        description=startup_data.description,
        domain=startup_data.domain,
        tech_stack=startup_data.tech_stack,
        founder_id=startup_data.founder_id,
        stage=startup_data.stage,
        industry=startup_data.industry,
        website=startup_data.website,
        location=startup_data.location
    )

    db.add(startup)
    db.commit()
    db.refresh(startup)

    return startup


# =========================
# GET ALL STARTUPS
# =========================

@router.get(
    "/",
    response_model=List[StartupResponse]
)
def get_all_startups(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Used by ML recommendation engine and graph builder
    """

    startups = db.query(Startup).all()

    return startups


# =========================
# GET STARTUP BY ID
# =========================

@router.get(
    "/{startup_id}",
    response_model=StartupResponse
)
def get_startup(
    startup_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    startup = db.query(Startup).filter(
        Startup.id == startup_id
    ).first()

    if not startup:
        raise HTTPException(
            status_code=404,
            detail="Startup not found"
        )

    return startup


# =========================
# UPDATE STARTUP
# =========================

@router.put(
    "/{startup_id}",
    response_model=StartupResponse
)
def update_startup(
    startup_id: int,
    startup_update: StartupUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    startup = db.query(Startup).filter(
        Startup.id == startup_id
    ).first()

    if not startup:
        raise HTTPException(
            status_code=404,
            detail="Startup not found"
        )

    update_data = startup_update.dict(exclude_unset=True)

    for field, value in update_data.items():
        setattr(startup, field, value)

    db.commit()
    db.refresh(startup)

    return startup


# =========================
# DELETE STARTUP
# =========================

@router.delete(
    "/{startup_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_startup(
    startup_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    startup = db.query(Startup).filter(
        Startup.id == startup_id
    ).first()

    if not startup:
        raise HTTPException(
            status_code=404,
            detail="Startup not found"
        )

    db.delete(startup)
    db.commit()

    return None


# =========================
# GET STARTUPS BY DOMAIN
# =========================

@router.get(
    "/domain/{domain}",
    response_model=List[StartupResponse]
)
def get_startups_by_domain(
    domain: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Used in ML recommendation filtering
    """

    startups = db.query(Startup).filter(
        Startup.domain.ilike(f"%{domain}%")
    ).all()

    return startups


# =========================
# GET STARTUPS BY INDUSTRY
# =========================

@router.get(
    "/industry/{industry}",
    response_model=List[StartupResponse]
)
def get_startups_by_industry(
    industry: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Used in ML recommendation filtering
    """

    startups = db.query(Startup).filter(
        Startup.industry.ilike(f"%{industry}%")
    ).all()

    return startups


# =========================
# GET STARTUPS BY FOUNDER
# =========================

@router.get(
    "/founder/{founder_id}",
    response_model=List[StartupResponse]
)
def get_startups_by_founder(
    founder_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Used in graph intelligence
    """

    startups = db.query(Startup).filter(
        Startup.founder_id == founder_id
    ).all()

    return startups