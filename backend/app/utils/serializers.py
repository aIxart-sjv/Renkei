from typing import Any, Dict, List, Optional
from datetime import datetime


# =========================
# DATETIME SERIALIZER
# =========================

def serialize_datetime(
    value: Optional[datetime]
) -> Optional[str]:
    """
    Convert datetime to ISO string
    """

    if not value:
        return None

    return value.isoformat()


# =========================
# GENERIC MODEL SERIALIZER
# =========================

def serialize_model(
    model: Any,
    exclude: Optional[List[str]] = None
) -> Dict[str, Any]:
    """
    Convert SQLAlchemy model to dict
    """

    if model is None:
        return {}

    exclude = exclude or []

    data = {}

    for column in model.__table__.columns:

        key = column.name

        if key in exclude:
            continue

        value = getattr(model, key)

        if isinstance(value, datetime):
            value = serialize_datetime(value)

        data[key] = value

    return data


# =========================
# SERIALIZE LIST OF MODELS
# =========================

def serialize_list(
    models: List[Any],
    exclude: Optional[List[str]] = None
) -> List[Dict[str, Any]]:
    """
    Serialize list of SQLAlchemy models
    """

    return [
        serialize_model(model, exclude)
        for model in models
    ]


# =========================
# STUDENT SERIALIZER
# =========================

def serialize_student(
    student: Any
) -> Dict[str, Any]:

    return serialize_model(student)


# =========================
# MENTOR SERIALIZER
# =========================

def serialize_mentor(
    mentor: Any
) -> Dict[str, Any]:

    return serialize_model(mentor)


# =========================
# STARTUP SERIALIZER
# =========================

def serialize_startup(
    startup: Any
) -> Dict[str, Any]:

    return serialize_model(startup)


# =========================
# ALUMNI SERIALIZER
# =========================

def serialize_alumni(
    alumni: Any
) -> Dict[str, Any]:

    return serialize_model(alumni)


# =========================
# ACHIEVEMENT SERIALIZER
# =========================

def serialize_achievement(
    achievement: Any
) -> Dict[str, Any]:

    return serialize_model(achievement)


# =========================
# CONNECTION SERIALIZER
# =========================

def serialize_connection(
    connection: Any
) -> Dict[str, Any]:

    return serialize_model(connection)


# =========================
# EMBEDDING SERIALIZER
# =========================

def serialize_embedding(
    embedding: Any
) -> Dict[str, Any]:

    data = serialize_model(embedding)

    # Optionally hide vector if too large
    if "vector" in data:
        data["vector_dimension"] = (
            len(data["vector"].split(","))
            if data["vector"]
            else 0
        )
        del data["vector"]

    return data


# =========================
# USER SERIALIZER
# =========================

def serialize_user(
    user: Any
) -> Dict[str, Any]:

    return serialize_model(
        user,
        exclude=["hashed_password"]
    )


# =========================
# GRAPH NODE SERIALIZER
# =========================

def serialize_graph_node(
    node_id: int,
    node_data: Dict[str, Any]
) -> Dict[str, Any]:

    return {
        "id": node_id,
        "type": node_data.get("type"),
        "innovation_score": node_data.get("innovation_score", 0),
        "centrality_score": node_data.get("centrality_score", 0),
        "pagerank_score": node_data.get("pagerank_score", 0)
    }


# =========================
# GRAPH EDGE SERIALIZER
# =========================

def serialize_graph_edge(
    source: int,
    target: int,
    edge_data: Dict[str, Any]
) -> Dict[str, Any]:

    return {
        "source": source,
        "target": target,
        "connection_type": edge_data.get("connection_type"),
        "strength": edge_data.get("weight", 1.0)
    }