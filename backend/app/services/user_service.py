from sqlalchemy.orm import Session
from typing import List, Optional

from app.models.user import User, UserRole
from app.schemas.user import UserUpdate

from app.core.logger import get_logger
from app.core.security import hash_password


logger = get_logger(__name__)


# =========================
# GET USER BY ID
# =========================

def get_user(
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
# GET ALL USERS
# =========================

def get_all_users(
    db: Session,
    skip: int = 0,
    limit: int = 100
) -> List[User]:

    return db.query(User)\
        .offset(skip)\
        .limit(limit)\
        .all()


# =========================
# UPDATE USER
# =========================

def update_user(
    db: Session,
    user_id: int,
    update_data: UserUpdate
) -> Optional[User]:

    user = get_user(
        db,
        user_id
    )

    if not user:
        return None


    try:

        update_fields = update_data.dict(
            exclude_unset=True
        )

        # Handle password separately
        if "password" in update_fields:

            update_fields["hashed_password"] = hash_password(
                update_fields.pop("password")
            )


        for field, value in update_fields.items():

            setattr(user, field, value)


        db.commit()
        db.refresh(user)

        logger.info(f"User updated: {user.id}")

        return user


    except Exception as e:

        db.rollback()

        logger.error(f"User update failed: {e}")

        raise


# =========================
# DELETE USER
# =========================

def delete_user(
    db: Session,
    user_id: int
) -> bool:

    user = get_user(db, user_id)

    if not user:
        return False


    try:

        db.delete(user)
        db.commit()

        logger.info(f"User deleted: {user_id}")

        return True

    except Exception as e:

        db.rollback()

        logger.error(f"User deletion failed: {e}")

        raise


# =========================
# ACTIVATE USER
# =========================

def activate_user(
    db: Session,
    user_id: int
) -> Optional[User]:

    user = get_user(db, user_id)

    if not user:
        return None


    user.is_active = True

    db.commit()
    db.refresh(user)

    return user


# =========================
# DEACTIVATE USER
# =========================

def deactivate_user(
    db: Session,
    user_id: int
) -> Optional[User]:

    user = get_user(db, user_id)

    if not user:
        return None


    user.is_active = False

    db.commit()
    db.refresh(user)

    return user


# =========================
# VERIFY USER
# =========================

def verify_user(
    db: Session,
    user_id: int
) -> Optional[User]:

    user = get_user(db, user_id)

    if not user:
        return None


    user.is_verified = True

    db.commit()
    db.refresh(user)

    return user


# =========================
# CHANGE USER ROLE
# =========================

def change_user_role(
    db: Session,
    user_id: int,
    role: UserRole
) -> Optional[User]:

    user = get_user(db, user_id)

    if not user:
        return None


    user.role = role

    db.commit()
    db.refresh(user)

    logger.info(f"User role updated: {user.id} → {role}")

    return user


# =========================
# GET USERS BY ROLE
# =========================

def get_users_by_role(
    db: Session,
    role: UserRole
) -> List[User]:

    return db.query(User).filter(
        User.role == role
    ).all()


# =========================
# COUNT USERS
# =========================

def count_users(
    db: Session
) -> int:

    return db.query(User).count()