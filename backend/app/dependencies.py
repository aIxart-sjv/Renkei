from typing import Generator

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.orm import Session

from app.config import settings
from app.db.session import SessionLocal
from app.models.user import User


# =========================
# DATABASE DEPENDENCY
# =========================

def get_db() -> Generator[Session, None, None]:
    """
    Provides database session to endpoints
    Automatically closes after request
    """

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()


# =========================
# AUTH DEPENDENCY
# =========================

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/api/auth/login"
)


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> User:
    """
    Extract and validate JWT token
    Return current authenticated user
    """

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:

        payload = jwt.decode(
            token,
            settings.JWT_SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM],
        )

        user_id: int | None = int(payload.get("sub"))

        if user_id is None:
            raise credentials_exception

    except JWTError:
        raise credentials_exception


    # Fetch user from database
    user = db.query(User).filter(User.id == user_id).first()

    if user is None:
        raise credentials_exception

    return user


# =========================
# ROLE-BASED ACCESS CONTROL
# =========================

def require_admin(
    current_user: User = Depends(get_current_user),
) -> User:
    """
    Ensure user is admin
    """

    if current_user.role != "admin":
        raise HTTPException(
            status_code=403,
            detail="Admin access required"
        )

    return current_user


def require_mentor(
    current_user: User = Depends(get_current_user),
) -> User:
    """
    Ensure user is mentor
    """

    if current_user.role != "mentor":
        raise HTTPException(
            status_code=403,
            detail="Mentor access required"
        )

    return current_user


def require_student(
    current_user: User = Depends(get_current_user),
) -> User:
    """
    Ensure user is student
    """

    if current_user.role != "student":
        raise HTTPException(
            status_code=403,
            detail="Student access required"
        )

    return current_user