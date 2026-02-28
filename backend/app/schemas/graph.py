from pydantic import BaseModel, Field
from typing import List, Optional


# =========================
# GRAPH NODE SCHEMA
# =========================

class GraphNode(BaseModel):
    """
    Represents a node in the innovation graph
    """

    id: int

    type: str = Field(
        ...,
        description="student, mentor, alumni, startup"
    )

    label: Optional[str] = Field(
        default=None,
        description="Display name"
    )

    innovation_score: Optional[float] = 0.0

    centrality_score: Optional[float] = 0.0

    pagerank_score: Optional[float] = 0.0


# =========================
# GRAPH EDGE SCHEMA
# =========================

class GraphEdge(BaseModel):
    """
    Represents a connection between two nodes
    """

    source: int

    target: int

    connection_type: str

    strength: float = Field(
        ...,
        ge=0.0,
        le=1.0
    )


# =========================
# FULL GRAPH RESPONSE
# =========================

class GraphResponse(BaseModel):
    """
    Full graph structure returned to frontend
    """

    nodes: List[GraphNode]

    edges: List[GraphEdge]


# =========================
# INNOVATION SCORE RESPONSE
# =========================

class InnovationScoreResponse(BaseModel):

    entity_id: int

    entity_type: str

    innovation_score: float

    centrality_score: Optional[float] = 0.0

    pagerank_score: Optional[float] = 0.0


# =========================
# TOP INNOVATORS RESPONSE
# =========================

class TopInnovator(BaseModel):

    entity_id: int

    entity_type: str

    innovation_score: float


class TopInnovatorsResponse(BaseModel):

    innovators: List[TopInnovator]


# =========================
# COLLABORATION SCORE RESPONSE
# =========================

class CollaborationScoreResponse(BaseModel):

    entity_id: int

    collaboration_score: float


# =========================
# SIMPLE NODE RESPONSE
# =========================

class GraphNodeResponse(BaseModel):

    id: int

    type: str

    innovation_score: float


# =========================
# SIMPLE EDGE RESPONSE
# =========================

class GraphEdgeResponse(BaseModel):

    source: int

    target: int

    strength: float

    connection_type: str