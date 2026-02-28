from sqlalchemy.orm import Session
from typing import Dict, List, Any

from app.core.logger import get_logger

from app.models.student import Student
from app.models.mentor import Mentor
from app.models.alumni import Alumni
from app.models.startup import Startup
from app.models.connection import Connection

from app.graph.builder import build_graph
from app.graph.centrality import composite_centrality_score
from app.graph.pagerank import compute_pagerank, normalize_pagerank
from app.graph.algorithms import compute_collaboration_score


logger = get_logger(__name__)


# =========================
# BUILD FULL GRAPH
# =========================

def get_graph(db: Session):
    """
    Build graph from database
    """

    graph = build_graph(db)

    return graph


# =========================
# GET GRAPH DATA FOR FRONTEND
# =========================

def get_graph_data(
    db: Session
) -> Dict[str, List[Dict[str, Any]]]:
    """
    Return graph nodes and edges
    """

    graph = build_graph(db)

    pagerank_scores = normalize_pagerank(
        compute_pagerank(graph)
    )

    centrality_scores = composite_centrality_score(graph)

    nodes = []
    edges = []


    # Add nodes
    for node_id, data in graph.nodes(data=True):

        nodes.append({
            "id": node_id,
            "type": data.get("type"),
            "innovation_score": data.get("innovation_score", 0.0),
            "pagerank_score": pagerank_scores.get(node_id, 0.0),
            "centrality_score": centrality_scores.get(node_id, 0.0)
        })


    # Add edges
    for source, target, data in graph.edges(data=True):

        edges.append({
            "source": source,
            "target": target,
            "connection_type": data.get("connection_type"),
            "strength": data.get("weight", 1.0)
        })


    return {
        "nodes": nodes,
        "edges": edges
    }


# =========================
# GET INNOVATION SCORES
# =========================

def get_innovation_scores(
    db: Session
) -> List[Dict[str, Any]]:
    """
    Get innovation scores for all entities
    """

    graph = build_graph(db)

    pagerank_scores = normalize_pagerank(
        compute_pagerank(graph)
    )

    centrality_scores = composite_centrality_score(graph)

    results = []

    for node_id, data in graph.nodes(data=True):

        results.append({
            "entity_id": node_id,
            "entity_type": data.get("type"),
            "innovation_score": data.get("innovation_score", 0.0),
            "pagerank_score": pagerank_scores.get(node_id, 0.0),
            "centrality_score": centrality_scores.get(node_id, 0.0)
        })

    return results


# =========================
# GET TOP INNOVATORS
# =========================

def get_top_innovators(
    db: Session,
    limit: int = 10
) -> List[Dict[str, Any]]:
    """
    Rank entities by innovation score
    """

    scores = get_innovation_scores(db)

    scores.sort(
        key=lambda x: x["innovation_score"],
        reverse=True
    )

    return scores[:limit]


# =========================
# GET COLLABORATION SCORE
# =========================

def get_collaboration_score(
    db: Session,
    entity_id: int
) -> float:
    """
    Get collaboration score of entity
    """

    graph = build_graph(db)

    score = compute_collaboration_score(
        graph,
        entity_id
    )

    return score


# =========================
# GET ENTITY NEIGHBORS
# =========================

def get_neighbors(
    db: Session,
    entity_id: int
) -> List[Dict[str, Any]]:
    """
    Get connected entities
    """

    graph = build_graph(db)

    neighbors = []

    if entity_id not in graph:
        return neighbors


    for neighbor in graph.neighbors(entity_id):

        neighbors.append({
            "entity_id": neighbor,
            "entity_type": graph.nodes[neighbor].get("type")
        })

    return neighbors


# =========================
# GET ENTITY DEGREE
# =========================

def get_entity_degree(
    db: Session,
    entity_id: int
) -> int:

    graph = build_graph(db)

    if entity_id not in graph:
        return 0

    return graph.degree(entity_id)


# =========================
# GET GRAPH SUMMARY
# =========================

def get_graph_summary(
    db: Session
) -> Dict[str, Any]:
    """
    Graph overview stats
    """

    graph = build_graph(db)

    return {
        "total_nodes": graph.number_of_nodes(),
        "total_edges": graph.number_of_edges(),
        "density": (
            graph.number_of_edges() /
            max(graph.number_of_nodes(), 1)
        )
    }