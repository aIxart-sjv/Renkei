"""
Graph-based scoring engine

Combines:
- PageRank
- Centrality
- Collaboration strength
- Node degree

Produces:
- Innovation score
- Influence score
- Recommendation score
"""

import networkx as nx
from typing import Dict

from app.graph.centrality import composite_centrality_score
from app.graph.pagerank import compute_pagerank, normalize_pagerank
from app.graph.algorithms import compute_collaboration_score

from app.core.logger import get_logger


logger = get_logger(__name__)


# =========================
# COMPUTE INNOVATION SCORES
# =========================

def compute_innovation_scores(
    graph: nx.Graph
) -> Dict[int, float]:
    """
    Combine multiple graph signals into innovation score

    Final score range: 0–100
    """

    if graph.number_of_nodes() == 0:
        return {}

    try:

        pagerank_scores = compute_pagerank(graph)
        pagerank_scores = normalize_pagerank(pagerank_scores)

        centrality_scores = composite_centrality_score(graph)

        innovation_scores = {}

        for node in graph.nodes():

            pagerank = pagerank_scores.get(node, 0)
            centrality = centrality_scores.get(node, 0)
            collaboration = compute_collaboration_score(
                graph,
                node
            )

            # Normalize collaboration roughly
            collaboration_scaled = min(collaboration * 10, 100)

            # Weighted combination
            score = (
                pagerank * 0.4 +
                centrality * 100 * 0.3 +
                collaboration_scaled * 0.3
            )

            innovation_scores[node] = round(score, 2)

        logger.info("Innovation scores computed")

        return innovation_scores

    except Exception as e:

        logger.error(f"Innovation score error: {e}")

        return {}


# =========================
# GET SINGLE NODE SCORE
# =========================

def innovation_score(
    graph: nx.Graph,
    node_id: int
) -> float:
    """
    Get innovation score for one entity
    """

    scores = compute_innovation_scores(graph)

    return scores.get(node_id, 0.0)


# =========================
# COMPUTE INFLUENCE SCORES
# =========================

def compute_influence_scores(
    graph: nx.Graph
) -> Dict[int, float]:
    """
    Influence based primarily on PageRank
    """

    pagerank_scores = compute_pagerank(graph)

    normalized = normalize_pagerank(pagerank_scores)

    return normalized


# =========================
# COMPUTE RECOMMENDATION SCORE
# =========================

def compute_recommendation_score(
    graph: nx.Graph,
    source_id: int,
    target_id: int,
    similarity_score: float
) -> float:
    """
    Final recommendation ranking score

    Combines:
    - similarity
    - influence
    - collaboration strength
    """

    try:

        influence_scores = compute_influence_scores(graph)

        target_influence = influence_scores.get(target_id, 0)

        collaboration_score = compute_collaboration_score(
            graph,
            target_id
        )

        collaboration_scaled = min(collaboration_score * 10, 100)

        final_score = (
            similarity_score * 0.5 +
            target_influence * 0.3 +
            collaboration_scaled * 0.2
        )

        return round(final_score, 2)

    except Exception as e:

        logger.error(f"Recommendation score error: {e}")

        return 0.0


# =========================
# RANK NODES BY SCORE
# =========================

def rank_nodes(
    scores: Dict[int, float],
    limit: int = 10
):
    """
    Rank nodes by score descending
    """

    ranked = sorted(
        scores.items(),
        key=lambda x: x[1],
        reverse=True
    )

    return ranked[:limit]


# =========================
# GET TOP INNOVATORS
# =========================

def top_innovators(
    graph: nx.Graph,
    limit: int = 10
):
    """
    Returns highest innovation score nodes
    """

    scores = compute_innovation_scores(graph)

    return rank_nodes(scores, limit)