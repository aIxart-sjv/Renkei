"""
Graph builder for Renkei innovation intelligence

Builds NetworkX graph from database entities and connections
"""

import networkx as nx
from sqlalchemy.orm import Session

from app.models.student import Student
from app.models.mentor import Mentor
from app.models.alumni import Alumni
from app.models.startup import Startup
from app.models.connection import Connection

from app.core.logger import get_logger
from app.core.constants import (
    ENTITY_STUDENT,
    ENTITY_MENTOR,
    ENTITY_ALUMNI,
    ENTITY_STARTUP,
    DEFAULT_EDGE_WEIGHT,
    CONNECTION_COLLABORATION,
    CONNECTION_MENTORSHIP,
    CONNECTION_STARTUP_MEMBER,
    CONNECTION_STARTUP_FOUNDER,
    MENTORSHIP_WEIGHT,
    COLLABORATION_WEIGHT,
    FOUNDER_WEIGHT
)


logger = get_logger(__name__)


# =========================
# BUILD FULL GRAPH
# =========================

def build_graph(db: Session) -> nx.Graph:
    """
    Build complete innovation graph from database

    Nodes:
        students
        mentors
        alumni
        startups

    Edges:
        connections
    """

    graph = nx.Graph()

    try:

        # =========================
        # ADD STUDENT NODES
        # =========================

        students = db.query(Student).all()

        for student in students:

            graph.add_node(
                student.id,
                type=ENTITY_STUDENT,
                innovation_score=student.innovation_score,
                collaboration_score=student.collaboration_score
            )


        logger.info(f"Added {len(students)} student nodes")


        # =========================
        # ADD MENTOR NODES
        # =========================

        mentors = db.query(Mentor).all()

        for mentor in mentors:

            graph.add_node(
                mentor.id,
                type=ENTITY_MENTOR,
                expertise=mentor.expertise
            )

        logger.info(f"Added {len(mentors)} mentor nodes")


        # =========================
        # ADD ALUMNI NODES
        # =========================

        alumni_list = db.query(Alumni).all()

        for alumni in alumni_list:

            graph.add_node(
                alumni.id,
                type=ENTITY_ALUMNI,
                industry=alumni.industry
            )

        logger.info(f"Added {len(alumni_list)} alumni nodes")


        # =========================
        # ADD STARTUP NODES
        # =========================

        startups = db.query(Startup).all()

        for startup in startups:

            graph.add_node(
                startup.id,
                type=ENTITY_STARTUP,
                domain=startup.domain,
                stage=startup.product_stage
            )

        logger.info(f"Added {len(startups)} startup nodes")


        # =========================
        # ADD EDGES (CONNECTIONS)
        # =========================

        connections = db.query(Connection).all()

        for conn in connections:

            weight = compute_edge_weight(conn)

            graph.add_edge(
                conn.source_id,
                conn.target_id,
                weight=weight,
                type=conn.connection_type,
                strength=conn.strength
            )

        logger.info(f"Added {len(connections)} edges")


        logger.info(
            f"Graph built: {graph.number_of_nodes()} nodes, "
            f"{graph.number_of_edges()} edges"
        )

        return graph


    except Exception as e:

        logger.error(f"Graph build failed: {e}")

        return nx.Graph()


# =========================
# EDGE WEIGHT CALCULATION
# =========================

def compute_edge_weight(connection: Connection) -> float:
    """
    Assign weight based on connection type and strength
    """

    base_weight = connection.strength or DEFAULT_EDGE_WEIGHT

    if connection.connection_type == CONNECTION_MENTORSHIP:

        return base_weight * MENTORSHIP_WEIGHT

    elif connection.connection_type == CONNECTION_COLLABORATION:

        return base_weight * COLLABORATION_WEIGHT

    elif connection.connection_type == CONNECTION_STARTUP_FOUNDER:

        return base_weight * FOUNDER_WEIGHT

    elif connection.connection_type == CONNECTION_STARTUP_MEMBER:

        return base_weight * COLLABORATION_WEIGHT

    else:

        return base_weight


# =========================
# BUILD SUBGRAPH FOR ENTITY
# =========================

def build_entity_subgraph(
    db: Session,
    entity_id: int,
    depth: int = 2
) -> nx.Graph:
    """
    Build subgraph centered around entity

    Used for recommendations and visualization
    """

    full_graph = build_graph(db)

    if entity_id not in full_graph:

        return nx.Graph()

    nodes = nx.single_source_shortest_path_length(
        full_graph,
        entity_id,
        cutoff=depth
    ).keys()

    subgraph = full_graph.subgraph(nodes).copy()

    return subgraph


# =========================
# GET NEIGHBORS
# =========================

def get_neighbors(
    graph: nx.Graph,
    entity_id: int
):
    """
    Get connected entities
    """

    if entity_id not in graph:

        return []

    return list(graph.neighbors(entity_id))