"""
PageRank-based influence scoring

Used to identify:
- Most influential students
- Most impactful mentors
- Key connectors in innovation ecosystem
"""

import networkx as nx
from typing import Dict, List, Tuple

from app.core.logger import get_logger


logger = get_logger(__name__)


# =========================
# COMPUTE PAGERANK
# =========================

def compute_pagerank(
    graph: nx.Graph,
    alpha: float = 0.85,
    max_iter: int = 100,
    tol: float = 1e-06
) -> Dict[int, float]:
    """
    Compute PageRank influence scores

    alpha: damping factor
    """

    if graph.number_of_nodes() == 0:
        return {}

    try:

        scores = nx.pagerank(
            graph,
            alpha=alpha,
            max_iter=max_iter,
            tol=tol,
            weight="weight"
        )

        logger.info("PageRank computed successfully")

        return scores

    except Exception as e:

        logger.error(f"PageRank computation failed: {e}")

        return {}


# =========================
# GET NODE PAGERANK SCORE
# =========================

def pagerank_score(
    graph: nx.Graph,
    node_id: int
) -> float:
    """
    Get influence score of specific node
    """

    scores = compute_pagerank(graph)

    return scores.get(node_id, 0.0)


# =========================
# GET TOP INFLUENTIAL NODES
# =========================

def top_influential_nodes(
    graph: nx.Graph,
    limit: int = 10
) -> List[Tuple[int, float]]:
    """
    Get most influential nodes in graph
    """

    scores = compute_pagerank(graph)

    ranked = sorted(
        scores.items(),
        key=lambda x: x[1],
        reverse=True
    )

    return ranked[:limit]


# =========================
# NORMALIZE PAGERANK SCORES
# =========================

def normalize_pagerank(
    scores: Dict[int, float]
) -> Dict[int, float]:
    """
    Normalize scores to 0–100 scale

    Used for innovation scoring
    """

    if not scores:
        return {}

    max_score = max(scores.values())

    if max_score == 0:
        return scores

    normalized = {}

    for node, score in scores.items():

        normalized[node] = (
            score / max_score
        ) * 100

    return normalized


# =========================
# PERSONALIZED PAGERANK
# =========================

def personalized_pagerank(
    graph: nx.Graph,
    personalization: Dict[int, float]
) -> Dict[int, float]:
    """
    Personalized PageRank

    Used for recommendation targeting
    """

    try:

        scores = nx.pagerank(
            graph,
            personalization=personalization,
            weight="weight"
        )

        logger.info("Personalized PageRank computed")

        return scores

    except Exception as e:

        logger.error(f"Personalized PageRank error: {e}")

        return {}