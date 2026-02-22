from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.services.graph_service import GraphService

router = APIRouter()


# -----------------------------------
# Get Innovation Scores for All Students
# -----------------------------------
@router.get("/innovation-scores")
def get_innovation_scores(db: Session = Depends(get_db)):
    scores = GraphService.calculate_innovation_scores(db)

    return {
        "message": "Innovation scores calculated successfully",
        "scores": scores
    }


# -----------------------------------
# Get Top Innovators Leaderboard
# -----------------------------------
@router.get("/top-innovators")
def get_top_innovators(limit: int = 5, db: Session = Depends(get_db)):
    innovators = GraphService.get_top_innovators(db, limit)

    return {
        "message": "Top innovators fetched successfully",
        "top_innovators": innovators
    }


# -----------------------------------
# Get Collaboration Score for Student
# -----------------------------------
@router.get("/collaboration-score/{student_id}")
def get_collaboration_score(student_id: int, db: Session = Depends(get_db)):
    score = GraphService.get_collaboration_score(student_id, db)

    if score is None:
        raise HTTPException(
            status_code=404,
            detail="Student not found in graph"
        )

    return {
        "student_id": student_id,
        "collaboration_score": score
    }


# -----------------------------------
# Get Full Graph Data (Nodes + Edges)
# Useful for frontend visualization
# -----------------------------------
@router.get("/graph-data")
def get_graph_data(db: Session = Depends(get_db)):
    G = GraphService.build_graph(db)

    nodes = [
        {"id": node, "label": G.nodes[node].get("label", str(node))}
        for node in G.nodes()
    ]

    edges = [
        {"source": edge[0], "target": edge[1], "type": G.edges[edge].get("type")}
        for edge in G.edges()
    ]

    return {
        "nodes": nodes,
        "edges": edges
    }