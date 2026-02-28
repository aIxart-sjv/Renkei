from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.dependencies import get_db, get_current_user
from app.models.connection import Connection
from app.models.user import User
from app.schemas.connection import (
    ConnectionCreate,
    ConnectionUpdate,
    ConnectionResponse
)


router = APIRouter()


# =========================
# CREATE CONNECTION
# =========================

@router.post(
    "/",
    response_model=ConnectionResponse,
    status_code=status.HTTP_201_CREATED
)
def create_connection(
    connection_data: ConnectionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Create connection between entities

    This feeds graph intelligence and ML recommendation engine
    """

    connection = Connection(
        source_id=connection_data.source_id,
        source_type=connection_data.source_type,
        target_id=connection_data.target_id,
        target_type=connection_data.target_type,
        connection_type=connection_data.connection_type,
        strength=connection_data.strength,
        metadata=connection_data.metadata
    )

    db.add(connection)
    db.commit()
    db.refresh(connection)

    return connection


# =========================
# GET ALL CONNECTIONS
# =========================

@router.get(
    "/",
    response_model=List[ConnectionResponse]
)
def get_all_connections(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Used by graph builder to construct innovation network
    """

    connections = db.query(Connection).all()

    return connections


# =========================
# GET CONNECTION BY ID
# =========================

@router.get(
    "/{connection_id}",
    response_model=ConnectionResponse
)
def get_connection(
    connection_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    connection = db.query(Connection).filter(
        Connection.id == connection_id
    ).first()

    if not connection:
        raise HTTPException(
            status_code=404,
            detail="Connection not found"
        )

    return connection


# =========================
# GET CONNECTIONS BY ENTITY
# =========================

@router.get(
    "/entity/{entity_type}/{entity_id}",
    response_model=List[ConnectionResponse]
)
def get_entity_connections(
    entity_type: str,
    entity_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get all connections of an entity

    Used for graph traversal and ML features
    """

    connections = db.query(Connection).filter(
        (
            (Connection.source_type == entity_type) &
            (Connection.source_id == entity_id)
        ) |
        (
            (Connection.target_type == entity_type) &
            (Connection.target_id == entity_id)
        )
    ).all()

    return connections


# =========================
# UPDATE CONNECTION
# =========================

@router.put(
    "/{connection_id}",
    response_model=ConnectionResponse
)
def update_connection(
    connection_id: int,
    connection_update: ConnectionUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    connection = db.query(Connection).filter(
        Connection.id == connection_id
    ).first()

    if not connection:
        raise HTTPException(
            status_code=404,
            detail="Connection not found"
        )

    update_data = connection_update.dict(exclude_unset=True)

    for field, value in update_data.items():
        setattr(connection, field, value)

    db.commit()
    db.refresh(connection)

    return connection


# =========================
# DELETE CONNECTION
# =========================

@router.delete(
    "/{connection_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_connection(
    connection_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    connection = db.query(Connection).filter(
        Connection.id == connection_id
    ).first()

    if not connection:
        raise HTTPException(
            status_code=404,
            detail="Connection not found"
        )

    db.delete(connection)
    db.commit()

    return None


# =========================
# GET CONNECTIONS BY TYPE
# =========================

@router.get(
    "/type/{connection_type}",
    response_model=List[ConnectionResponse]
)
def get_connections_by_type(
    connection_type: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Used by ML recommendation engine and graph analysis
    """

    connections = db.query(Connection).filter(
        Connection.connection_type == connection_type
    ).all()

    return connections