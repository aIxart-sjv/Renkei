from sqlalchemy.orm import Session
from typing import Optional

from app.models.user import User, UserRole
from app.schemas.user import UserCreate, UserLogin

from app.core.security import (
    hash_password,
    verify_password,
    create_access_token
)

from app.core.logger import get_logger


logger = get_logger(__name__)


# =========================
# REGISTER USER
# =========================

def register_user(
    db: Session,
    user_data: UserCreate
) -> User:
    """
    Register new user
    """

    # Check if email exists
    existing_user = db.query(User).filter(
        User.email == user_data.email
    ).first()

    if existing_user:
        raise ValueError("Email already registered")


    # Check if username exists
    existing_username = db.query(User).filter(
        User.username == user_data.username
    ).first()

    if existing_username:
        raise ValueError("Username already exists")


    try:

        hashed_pw = hash_password(
            user_data.password
        )

        user = User(
            email=user_data.email,
            username=user_data.username,
            hashed_password=hashed_pw,
            role=user_data.role,
            full_name=user_data.full_name,
            profile_image=user_data.profile_image,
            is_active=True,
            is_verified=False
        )

        db.add(user)
        db.commit()
        db.refresh(user)

        logger.info(
            f"User registered: {user.id}"
        )

        return user

    except Exception as e:

        db.rollback()

        logger.error(
            f"User registration failed: {e}"
        )

        raise


# =========================
# AUTHENTICATE USER (LOGIN)
# =========================

def authenticate_user(
    db: Session,
    login_data: UserLogin
) -> Optional[User]:
    """
    Authenticate user credentials
    """

    user = db.query(User).filter(
        User.email == login_data.email
    ).first()

    if not user:
        return None


    if not verify_password(
        login_data.password,
        user.hashed_password
    ):
        return None


    if not user.is_active:
        return None


    return user


# =========================
# LOGIN USER (GET TOKEN)
# =========================

def login_user(
    db: Session,
    login_data: UserLogin
) -> dict:
    """
    Authenticate and generate token
    """

    user = authenticate_user(
        db,
        login_data
    )

    if not user:
        raise ValueError(
            "Invalid credentials"
        )


    access_token = create_access_token(
        data={
            "sub": str(user.id),
            "role": user.role.value
        }
    )


    logger.info(
        f"User logged in: {user.id}"
    )


    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user_id": user.id,
        "role": user.role.value
    }


# =========================
# GET USER BY ID
# =========================

def get_user_by_id(
    db: Session,
    user_id: int
) -> Optional[User]:

    return db.query(User).filter(
        User.id == user_id
    ).first()


# =========================
# GET USER BY EMAIL
# =========================

def get_user_by_email(
    db: Session,
    email: str
) -> Optional[User]:

    return db.query(User).filter(
        User.email == email
    ).first()


# =========================
# GET USER BY USERNAME
# =========================

def get_user_by_username(
    db: Session,
    username: str
) -> Optional[User]:

    return db.query(User).filter(
        User.username == username
    ).first()


# =========================
# DELETE USER
# =========================

def delete_user(
    db: Session,
    user_id: int
) -> bool:

    user = get_user_by_id(
        db,
        user_id
    )

    if not user:
        return False


    try:

        db.delete(user)
        db.commit()

        logger.info(
            f"User deleted: {user_id}"
        )

        return True

    except Exception as e:

        db.rollback()

        logger.error(
            f"User deletion failed: {e}"
        )

        raise


# =========================
# CHECK USER ROLE
# =========================

def check_user_role(
    user: User,
    required_role: UserRole
) -> bool:

    return user.role == required_role