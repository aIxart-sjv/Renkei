from sqlalchemy.orm import Session
from typing import List, Optional

from app.models.connection import Connection
from app.schemas.connection import (
    ConnectionCreate,
    ConnectionUpdate
)

from app.core.logger import get_logger


logger = get_logger(__name__)


# =========================
# CREATE CONNECTION
# =========================

def create_connection(
    db: Session,
    connection_data: ConnectionCreate
) -> Connection:
    """
    Create graph connection between entities
    """

    try:

        connection = Connection(
            source_id=connection_data.source_id,
            source_type=connection_data.source_type,
            target_id=connection_data.target_id,
            target_type=connection_data.target_type,
            connection_type=connection_data.connection_type,
            strength=connection_data.strength,
            description=connection_data.description
        )

        db.add(connection)
        db.commit()
        db.refresh(connection)

        logger.info(
            f"Connection created: {connection.id}"
        )

        return connection

    except Exception as e:

        db.rollback()

        logger.error(
            f"Connection creation failed: {e}"
        )

        raise


# =========================
# GET CONNECTION BY ID
# =========================

def get_connection(
    db: Session,
    connection_id: int
) -> Optional[Connection]:

    return db.query(Connection).filter(
        Connection.id == connection_id
    ).first()


# =========================
# GET ALL CONNECTIONS
# =========================

def get_all_connections(
    db: Session,
    skip: int = 0,
    limit: int = 1000
) -> List[Connection]:

    return db.query(Connection)\
        .offset(skip)\
        .limit(limit)\
        .all()


# =========================
# GET CONNECTIONS BY ENTITY
# =========================

def get_entity_connections(
    db: Session,
    entity_id: int,
    entity_type: str
) -> List[Connection]:
    """
    Get all connections for an entity
    """

    return db.query(Connection).filter(
        (
            (Connection.source_id == entity_id) &
            (Connection.source_type == entity_type)
        ) |
        (
            (Connection.target_id == entity_id) &
            (Connection.target_type == entity_type)
        )
    ).all()


# =========================
# GET OUTGOING CONNECTIONS
# =========================

def get_outgoing_connections(
    db: Session,
    entity_id: int,
    entity_type: str
) -> List[Connection]:

    return db.query(Connection).filter(
        Connection.source_id == entity_id,
        Connection.source_type == entity_type
    ).all()


# =========================
# GET INCOMING CONNECTIONS
# =========================

def get_incoming_connections(
    db: Session,
    entity_id: int,
    entity_type: str
) -> List[Connection]:

    return db.query(Connection).filter(
        Connection.target_id == entity_id,
        Connection.target_type == entity_type
    ).all()


# =========================
# UPDATE CONNECTION
# =========================

def update_connection(
    db: Session,
    connection_id: int,
    update_data: ConnectionUpdate
) -> Optional[Connection]:

    connection = get_connection(
        db,
        connection_id
    )

    if not connection:
        return None


    try:

        update_fields = update_data.dict(
            exclude_unset=True
        )

        for field, value in update_fields.items():

            setattr(
                connection,
                field,
                value
            )

        db.commit()
        db.refresh(connection)

        logger.info(
            f"Connection updated: {connection.id}"
        )

        return connection

    except Exception as e:

        db.rollback()

        logger.error(
            f"Connection update failed: {e}"
        )

        raise


# =========================
# DELETE CONNECTION
# =========================

def delete_connection(
    db: Session,
    connection_id: int
) -> bool:

    connection = get_connection(
        db,
        connection_id
    )

    if not connection:
        return False


    try:

        db.delete(connection)
        db.commit()

        logger.info(
            f"Connection deleted: {connection_id}"
        )

        return True

    except Exception as e:

        db.rollback()

        logger.error(
            f"Connection deletion failed: {e}"
        )

        raise


# =========================
# GET STRONG CONNECTIONS
# =========================

def get_strong_connections(
    db: Session,
    threshold: float = 0.7
) -> List[Connection]:
    """
    Used for ML training and graph intelligence
    """

    return db.query(Connection).filter(
        Connection.strength >= threshold
    ).all()


# =========================
# CHECK IF CONNECTION EXISTS
# =========================

def connection_exists(
    db: Session,
    source_id: int,
    source_type: str,
    target_id: int,
    target_type: str
) -> bool:

    connection = db.query(Connection).filter(
        Connection.source_id == source_id,
        Connection.source_type == source_type,
        Connection.target_id == target_id,
        Connection.target_type == target_type
    ).first()

    return connection is not None


# =========================
# GET CONNECTION STRENGTH
# =========================

def get_connection_strength(
    db: Session,
    source_id: int,
    target_id: int
) -> float:

    connection = db.query(Connection).filter(
        Connection.source_id == source_id,
        Connection.target_id == target_id
    ).first()

    if not connection:
        return 0.0

    return connection.strength