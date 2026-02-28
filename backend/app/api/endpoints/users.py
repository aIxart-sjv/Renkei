from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.dependencies import get_db, get_current_user, require_admin
from app.models.user import User
from app.schemas.user import (
    UserCreate,
    UserUpdate,
    UserResponse
)
from app.core.security import hash_password


router = APIRouter()


# =========================
# CREATE USER (ADMIN ONLY)
# =========================

@router.post(
    "/",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED
)
def create_user(
    user_data: UserCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """
    Create new user account

    All entities (student, mentor, alumni) link to user
    """

    existing_user = db.query(User).filter(
        User.email == user_data.email
    ).first()

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email already exists"
        )


    hashed_pw = hash_password(user_data.password)

    user = User(
        email=user_data.email,
        full_name=user_data.name,
        hashed_password=hashed_pw,
        role=user_data.role,
        is_active=True
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user


# =========================
# GET ALL USERS (ADMIN)
# =========================

@router.get(
    "/",
    response_model=List[UserResponse]
)
def get_all_users(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    users = db.query(User).all()

    return users


# =========================
# GET USER BY ID
# =========================

@router.get(
    "/{user_id}",
    response_model=UserResponse
)
def get_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    user = db.query(User).filter(
        User.id == user_id
    ).first()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return user


# =========================
# UPDATE USER
# =========================

@router.put(
    "/{user_id}",
    response_model=UserResponse
)
def update_user(
    user_id: int,
    user_update: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    user = db.query(User).filter(
        User.id == user_id
    ).first()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    update_data = user_update.dict(exclude_unset=True)

    if "password" in update_data:
        update_data["hashed_password"] = hash_password(
            update_data.pop("password")
        )

    for field, value in update_data.items():
        setattr(user, field, value)

    db.commit()
    db.refresh(user)

    return user


# =========================
# DELETE USER
# =========================

@router.delete(
    "/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    user = db.query(User).filter(
        User.id == user_id
    ).first()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    db.delete(user)
    db.commit()

    return None


# =========================
# GET USERS BY ROLE
# =========================

@router.get(
    "/role/{role}",
    response_model=List[UserResponse]
)
def get_users_by_role(
    role: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """
    Used in system management and ML grouping
    """

    users = db.query(User).filter(
        User.role == role
    ).all()

    return users


# =========================
# GET CURRENT USER PROFILE
# =========================

@router.get(
    "/me",
    response_model=UserResponse
)
def get_my_profile(
    current_user: User = Depends(get_current_user)
):
    """
    Returns authenticated user profile
    """

    return current_user