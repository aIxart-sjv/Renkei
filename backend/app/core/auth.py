from datetime import datetime, timedelta
from typing import Optional

from jose import jwt, JWTError
from fastapi import HTTPException, status

from app.config import settings


# =========================
# CREATE ACCESS TOKEN
# =========================

def create_access_token(
    subject: str | int,
    expires_delta: Optional[timedelta] = None
) -> str:
    """
    Create JWT access token

    subject: usually user_id
    """

    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES
        )

    payload = {
        "sub": str(subject),
        "exp": expire,
        "iat": datetime.utcnow(),
        "type": "access"
    }

    token = jwt.encode(
        payload,
        settings.JWT_SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM
    )

    return token


# =========================
# VERIFY TOKEN
# =========================

def verify_token(token: str) -> dict:
    """
    Decode and validate JWT token
    """

    try:

        payload = jwt.decode(
            token,
            settings.JWT_SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM]
        )

        return payload

    except JWTError:

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )


# =========================
# EXTRACT USER ID
# =========================

def get_user_id_from_token(token: str) -> int:
    """
    Extract user_id from JWT token
    """

    payload = verify_token(token)

    user_id = payload.get("sub")

    if user_id is None:

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload"
        )

    return int(user_id)


# =========================
# OPTIONAL: CREATE REFRESH TOKEN
# =========================

def create_refresh_token(
    subject: str | int
) -> str:
    """
    Long-lived refresh token
    """

    expire = datetime.utcnow() + timedelta(days=7)

    payload = {
        "sub": str(subject),
        "exp": expire,
        "iat": datetime.utcnow(),
        "type": "refresh"
    }

    token = jwt.encode(
        payload,
        settings.JWT_SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM
    )

    return token


# =========================
# VERIFY TOKEN TYPE
# =========================

def verify_token_type(
    token: str,
    expected_type: str = "access"
) -> dict:
    """
    Ensure correct token type
    """

    payload = verify_token(token)

    token_type = payload.get("type")

    if token_type != expected_type:

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid token type: expected {expected_type}"
        )

    return payload