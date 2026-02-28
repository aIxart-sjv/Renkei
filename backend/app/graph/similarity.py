"""
Graph similarity engine

Provides:
- Jaccard similarity
- Common neighbor similarity
- Adamic-Adar index
- Resource allocation index
- Structural similarity scoring
"""

import networkx as nx
from typing import Dict, List, Tuple

from app.core.logger import get_logger


logger = get_logger(__name__)


# =========================
# JACCARD SIMILARITY
# =========================

def jaccard_similarity(
    graph: nx.Graph,
    node_id: int
) -> List[Tuple[int, float]]:
    """
    Measures similarity based on shared neighbors
    """

    if node_id not in graph:
        return []

    try:

        similarities = nx.jaccard_coefficient(
            graph,
            [(node_id, other) for other in graph.nodes() if other != node_id]
        )

        results = [(v, score) for _, v, score in similarities]

        results.sort(
            key=lambda x: x[1],
            reverse=True
        )

        return results

    except Exception as e:

        logger.error(f"Jaccard similarity error: {e}")

        return []


# =========================
# COMMON NEIGHBOR SIMILARITY
# =========================

def common_neighbor_similarity(
    graph: nx.Graph,
    node_id: int
) -> List[Tuple[int, int]]:
    """
    Counts shared connections
    """

    if node_id not in graph:
        return []

    try:

        scores = []

        neighbors = set(graph.neighbors(node_id))

        for other in graph.nodes():

            if other == node_id:
                continue

            other_neighbors = set(graph.neighbors(other))

            common = len(
                neighbors.intersection(other_neighbors)
            )

            scores.append((other, common))

        scores.sort(
            key=lambda x: x[1],
            reverse=True
        )

        return scores

    except Exception as e:

        logger.error(f"Common neighbor error: {e}")

        return []


# =========================
# ADAMIC-ADAR INDEX
# =========================

def adamic_adar_similarity(
    graph: nx.Graph,
    node_id: int
) -> List[Tuple[int, float]]:
    """
    Penalizes high-degree neighbors

    More meaningful similarity measure
    """

    if node_id not in graph:
        return []

    try:

        similarities = nx.adamic_adar_index(
            graph,
            [(node_id, other) for other in graph.nodes() if other != node_id]
        )

        results = [(v, score) for _, v, score in similarities]

        results.sort(
            key=lambda x: x[1],
            reverse=True
        )

        return results

    except Exception as e:

        logger.error(f"Adamic-Adar error: {e}")

        return []


# =========================
# RESOURCE ALLOCATION INDEX
# =========================

def resource_allocation_similarity(
    graph: nx.Graph,
    node_id: int
) -> List[Tuple[int, float]]:
    """
    Measures resource-sharing probability
    """

    if node_id not in graph:
        return []

    try:

        similarities = nx.resource_allocation_index(
            graph,
            [(node_id, other) for other in graph.nodes() if other != node_id]
        )

        results = [(v, score) for _, v, score in similarities]

        results.sort(
            key=lambda x: x[1],
            reverse=True
        )

        return results

    except Exception as e:

        logger.error(f"Resource allocation error: {e}")

        return []


# =========================
# STRUCTURAL SIMILARITY SCORE
# =========================

def structural_similarity_score(
    graph: nx.Graph,
    node_a: int,
    node_b: int
) -> float:
    """
    Combined structural similarity metric
    """

    if node_a not in graph or node_b not in graph:
        return 0.0

    try:

        neighbors_a = set(graph.neighbors(node_a))
        neighbors_b = set(graph.neighbors(node_b))

        intersection = len(
            neighbors_a.intersection(neighbors_b)
        )

        union = len(
            neighbors_a.union(neighbors_b)
        )

        if union == 0:
            return 0.0

        score = intersection / union

        return score

    except Exception as e:

        logger.error(f"Structural similarity error: {e}")

        return 0.0


# =========================
# FIND MOST SIMILAR NODES
# =========================

def find_most_similar_nodes(
    graph: nx.Graph,
    node_id: int,
    top_k: int = 10
) -> List[Tuple[int, float]]:
    """
    Combined similarity ranking
    """

    try:

        jaccard_scores = jaccard_similarity(graph, node_id)

        return jaccard_scores[:top_k]

    except Exception as e:

        logger.error(f"Similarity ranking error: {e}")

        return []


# =========================
# BUILD SIMILARITY MATRIX
# =========================

def similarity_matrix(
    graph: nx.Graph
) -> Dict[int, Dict[int, float]]:
    """
    Compute similarity between all node pairs
    """

    matrix = {}

    for node_a in graph.nodes():

        matrix[node_a] = {}

        for node_b in graph.nodes():

            if node_a == node_b:
                continue

            matrix[node_a][node_b] = structural_similarity_score(
                graph,
                node_a,
                node_b
            )

    return matrix