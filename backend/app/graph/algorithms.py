"""
Graph algorithms for innovation intelligence

Provides:
- PageRank (influence scoring)
- Centrality (importance scoring)
- Collaboration score
- Similarity scoring
"""

import networkx as nx
from typing import Dict, List, Tuple

from app.core.logger import get_logger
from app.core.constants import (
    DEFAULT_EDGE_WEIGHT,
    COLLABORATION_WEIGHT,
    MENTORSHIP_WEIGHT,
    FOUNDER_WEIGHT
)


logger = get_logger(__name__)


# =========================
# PAGERANK (INFLUENCE)
# =========================

def compute_pagerank(
    graph: nx.Graph,
    alpha: float = 0.85
) -> Dict[int, float]:
    """
    Compute PageRank influence score

    Used to identify most influential innovators
    """

    if graph.number_of_nodes() == 0:
        return {}

    try:

        pagerank_scores = nx.pagerank(
            graph,
            alpha=alpha,
            weight="weight"
        )

        logger.info("PageRank computed")

        return pagerank_scores

    except Exception as e:

        logger.error(f"PageRank error: {e}")

        return {}


# =========================
# DEGREE CENTRALITY
# =========================

def compute_centrality(
    graph: nx.Graph
) -> Dict[int, float]:
    """
    Compute node importance using degree centrality

    Used in ML features and ranking
    """

    if graph.number_of_nodes() == 0:
        return {}

    try:

        centrality = nx.degree_centrality(graph)

        logger.info("Centrality computed")

        return centrality

    except Exception as e:

        logger.error(f"Centrality error: {e}")

        return {}


# =========================
# BETWEENNESS CENTRALITY
# =========================

def compute_betweenness_centrality(
    graph: nx.Graph
) -> Dict[int, float]:
    """
    Measures how often node connects other nodes
    """

    if graph.number_of_nodes() == 0:
        return {}

    try:

        centrality = nx.betweenness_centrality(
            graph,
            weight="weight",
            normalized=True
        )

        return centrality

    except Exception as e:

        logger.error(f"Betweenness error: {e}")

        return {}


# =========================
# COLLABORATION SCORE
# =========================

def compute_collaboration_score(
    graph: nx.Graph,
    node_id: int
) -> float:
    """
    Collaboration score based on connections and weights

    Used in innovation score ML model
    """

    if node_id not in graph:
        return 0.0

    try:

        total_weight = 0.0

        for neighbor in graph.neighbors(node_id):

            edge_data = graph.get_edge_data(
                node_id,
                neighbor
            )

            weight = edge_data.get(
                "weight",
                DEFAULT_EDGE_WEIGHT
            )

            total_weight += weight

        return total_weight

    except Exception as e:

        logger.error(f"Collaboration score error: {e}")

        return 0.0


# =========================
# FIND SHORTEST PATH
# =========================

def shortest_path_length(
    graph: nx.Graph,
    source: int,
    target: int
) -> int:
    """
    Used to measure graph distance for recommendations
    """

    try:

        length = nx.shortest_path_length(
            graph,
            source=source,
            target=target
        )

        return length

    except nx.NetworkXNoPath:

        return -1

    except Exception as e:

        logger.error(f"Path error: {e}")

        return -1


# =========================
# FIND SIMILAR NODES
# =========================

def find_similar_nodes(
    graph: nx.Graph,
    node_id: int,
    top_k: int = 5
) -> List[Tuple[int, float]]:
    """
    Find nodes with similar connection structure

    Used in graph-based recommendations
    """

    if node_id not in graph:
        return []

    try:

        similarities = []

        neighbors = set(graph.neighbors(node_id))

        for other_node in graph.nodes():

            if other_node == node_id:
                continue

            other_neighbors = set(
                graph.neighbors(other_node)
            )

            intersection = len(
                neighbors.intersection(other_neighbors)
            )

            union = len(
                neighbors.union(other_neighbors)
            )

            if union == 0:
                similarity = 0
            else:
                similarity = intersection / union

            similarities.append(
                (other_node, similarity)
            )

        similarities.sort(
            key=lambda x: x[1],
            reverse=True
        )

        return similarities[:top_k]

    except Exception as e:

        logger.error(f"Similarity error: {e}")

        return []


# =========================
# GRAPH SUMMARY METRICS
# =========================

def graph_summary(
    graph: nx.Graph
) -> Dict:
    """
    Returns key graph metrics
    """

    try:

        summary = {
            "nodes": graph.number_of_nodes(),
            "edges": graph.number_of_edges(),
            "density": nx.density(graph),
            "connected_components": nx.number_connected_components(graph)
        }

        return summary

    except Exception as e:

        logger.error(f"Graph summary error: {e}")

        return {}