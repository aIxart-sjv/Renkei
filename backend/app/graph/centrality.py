"""
Centrality scoring for innovation intelligence

Provides:
- Degree centrality
- Betweenness centrality
- Closeness centrality
- Eigenvector centrality
- Composite innovation centrality score
"""

import networkx as nx
from typing import Dict

from app.core.logger import get_logger


logger = get_logger(__name__)


# =========================
# DEGREE CENTRALITY
# =========================

def degree_centrality(graph: nx.Graph) -> Dict[int, float]:
    """
    Measures how connected a node is

    High score = highly collaborative
    """

    if graph.number_of_nodes() == 0:
        return {}

    try:

        scores = nx.degree_centrality(graph)

        logger.info("Degree centrality computed")

        return scores

    except Exception as e:

        logger.error(f"Degree centrality error: {e}")

        return {}


# =========================
# BETWEENNESS CENTRALITY
# =========================

def betweenness_centrality(graph: nx.Graph) -> Dict[int, float]:
    """
    Measures how often node connects other nodes

    High score = connector/influencer
    """

    if graph.number_of_nodes() == 0:
        return {}

    try:

        scores = nx.betweenness_centrality(
            graph,
            weight="weight",
            normalized=True
        )

        logger.info("Betweenness centrality computed")

        return scores

    except Exception as e:

        logger.error(f"Betweenness centrality error: {e}")

        return {}


# =========================
# CLOSENESS CENTRALITY
# =========================

def closeness_centrality(graph: nx.Graph) -> Dict[int, float]:
    """
    Measures how close node is to others

    High score = fast information spread
    """

    if graph.number_of_nodes() == 0:
        return {}

    try:

        scores = nx.closeness_centrality(graph)

        logger.info("Closeness centrality computed")

        return scores

    except Exception as e:

        logger.error(f"Closeness centrality error: {e}")

        return {}


# =========================
# EIGENVECTOR CENTRALITY
# =========================

def eigenvector_centrality(graph: nx.Graph) -> Dict[int, float]:
    """
    Measures influence based on neighbor importance

    High score = connected to influential nodes
    """

    if graph.number_of_nodes() == 0:
        return {}

    try:

        scores = nx.eigenvector_centrality(
            graph,
            weight="weight",
            max_iter=1000
        )

        logger.info("Eigenvector centrality computed")

        return scores

    except Exception as e:

        logger.error(f"Eigenvector centrality error: {e}")

        return {}


# =========================
# COMPOSITE CENTRALITY SCORE
# =========================

def composite_centrality_score(graph: nx.Graph) -> Dict[int, float]:
    """
    Combined innovation centrality score

    Used directly in ML innovation scoring
    """

    try:

        deg = degree_centrality(graph)
        bet = betweenness_centrality(graph)
        clo = closeness_centrality(graph)
        eig = eigenvector_centrality(graph)

        composite = {}

        for node in graph.nodes():

            composite[node] = (
                deg.get(node, 0) * 0.25 +
                bet.get(node, 0) * 0.25 +
                clo.get(node, 0) * 0.25 +
                eig.get(node, 0) * 0.25
            )

        logger.info("Composite centrality computed")

        return composite

    except Exception as e:

        logger.error(f"Composite centrality error: {e}")

        return {}


# =========================
# GET TOP CENTRAL NODES
# =========================

def top_central_nodes(
    graph: nx.Graph,
    limit: int = 10
):
    """
    Get most important innovators
    """

    scores = composite_centrality_score(graph)

    ranked = sorted(
        scores.items(),
        key=lambda x: x[1],
        reverse=True
    )

    return ranked[:limit]