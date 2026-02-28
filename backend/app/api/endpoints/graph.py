from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Dict, List

from app.dependencies import get_db, get_current_user
from app.models.connection import Connection
from app.models.student import Student
from app.models.mentor import Mentor
from app.models.alumni import Alumni
from app.models.startup import Startup
from app.models.user import User

from app.graph.builder import build_graph
from app.graph.algorithms import (
    compute_pagerank,
    compute_centrality,
    compute_collaboration_score
)


router = APIRouter()


# =========================
# GET FULL GRAPH DATA
# =========================

@router.get("/graph-data")
def get_graph_data(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Returns nodes and edges for graph visualization
    """

    graph = build_graph(db)

    nodes = []
    edges = []

    for node in graph.nodes():
        nodes.append({
            "id": node,
            "label": str(node)
        })

    for edge in graph.edges(data=True):
        edges.append({
            "source": edge[0],
            "target": edge[1],
            "weight": edge[2].get("weight", 1)
        })

    return {
        "nodes": nodes,
        "edges": edges
    }


# =========================
# GET PAGERANK SCORES
# =========================

@router.get("/pagerank")
def get_pagerank_scores(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Influence ranking using PageRank algorithm
    """

    graph = build_graph(db)

    scores = compute_pagerank(graph)

    return scores


# =========================
# GET CENTRALITY SCORES
# =========================

@router.get("/centrality")
def get_centrality_scores(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Measures node importance in network
    """

    graph = build_graph(db)

    centrality = compute_centrality(graph)

    return centrality


# =========================
# GET COLLABORATION SCORE
# =========================

@router.get("/collaboration-score/{entity_id}")
def get_collaboration_score(
    entity_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Used as ML feature and innovation score component
    """

    graph = build_graph(db)

    score = compute_collaboration_score(graph, entity_id)

    return {
        "entity_id": entity_id,
        "collaboration_score": score
    }


# =========================
# GET TOP INNOVATORS
# =========================

@router.get("/top-innovators")
def get_top_innovators(
    limit: int = 10,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Returns highest ranked nodes based on graph intelligence
    """

    graph = build_graph(db)

    pagerank_scores = compute_pagerank(graph)

    sorted_nodes = sorted(
        pagerank_scores.items(),
        key=lambda x: x[1],
        reverse=True
    )

    top_nodes = sorted_nodes[:limit]

    return [
        {
            "entity_id": node,
            "score": score
        }
        for node, score in top_nodes
    ]


# =========================
# GET GRAPH SUMMARY
# =========================

@router.get("/summary")
def get_graph_summary(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Overview metrics for dashboard and ML pipeline
    """

    graph = build_graph(db)

    return {
        "total_nodes": graph.number_of_nodes(),
        "total_edges": graph.number_of_edges(),
        "density": round(graph.number_of_edges() / max(graph.number_of_nodes(), 1), 4)
    }