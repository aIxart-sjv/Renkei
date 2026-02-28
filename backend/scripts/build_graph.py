"""
Build Innovation Graph Script

Usage:
    python scripts/build_graph.py

This script:
- Loads entities from database
- Builds graph structure
- Computes graph metrics
- Saves graph to file
"""

import os
import json
import networkx as nx

from app.db.session import SessionLocal
import app.db.model_registry
from app.models.student import Student
from app.models.mentor import Mentor
from app.models.alumni import Alumni
from app.models.startup import Startup
from app.models.connection import Connection

from app.graph.centrality import composite_centrality_score
from app.graph.pagerank import compute_pagerank, normalize_pagerank


# =========================
# BUILD GRAPH FROM DATABASE
# =========================

def build_graph():

    db = SessionLocal()

    graph = nx.Graph()


    # ---------------------
    # ADD STUDENTS
    # ---------------------

    students = db.query(Student).all()

    for student in students:

        graph.add_node(
            student.id,
            type="student",
            innovation_score=student.innovation_score
        )


    # ---------------------
    # ADD MENTORS
    # ---------------------

    mentors = db.query(Mentor).all()

    for mentor in mentors:

        graph.add_node(
            mentor.id,
            type="mentor"
        )


    # ---------------------
    # ADD ALUMNI
    # ---------------------

    alumni = db.query(Alumni).all()

    for alum in alumni:

        graph.add_node(
            alum.id,
            type="alumni"
        )


    # ---------------------
    # ADD STARTUPS
    # ---------------------

    startups = db.query(Startup).all()

    for startup in startups:

        graph.add_node(
            startup.id,
            type="startup",
            innovation_score=startup.innovation_score
        )


    # ---------------------
    # ADD CONNECTIONS (EDGES)
    # ---------------------

    connections = db.query(Connection).all()

    for conn in connections:

        graph.add_edge(
            conn.source_id,
            conn.target_id,
            weight=conn.strength,
            connection_type=conn.connection_type
        )


    db.close()

    return graph


# =========================
# SAVE GRAPH TO JSON
# =========================

def save_graph(graph, filepath="graph.json"):

    pagerank = normalize_pagerank(
        compute_pagerank(graph)
    )

    centrality = composite_centrality_score(graph)

    data = {
        "nodes": [],
        "edges": []
    }


    for node_id, attrs in graph.nodes(data=True):

        data["nodes"].append({
            "id": node_id,
            "type": attrs.get("type"),
            "innovation_score": attrs.get("innovation_score", 0),
            "pagerank_score": pagerank.get(node_id, 0),
            "centrality_score": centrality.get(node_id, 0)
        })


    for source, target, attrs in graph.edges(data=True):

        data["edges"].append({
            "source": source,
            "target": target,
            "strength": attrs.get("weight", 1.0),
            "connection_type": attrs.get("connection_type")
        })


    with open(filepath, "w") as f:

        json.dump(data, f, indent=4)


    print(f"Graph saved to {filepath}")


# =========================
# PRINT GRAPH SUMMARY
# =========================

def print_summary(graph):

    print("\nGraph Summary:")
    print(f"Nodes: {graph.number_of_nodes()}")
    print(f"Edges: {graph.number_of_edges()}")

    print("\nNode Types:")

    types = {}

    for _, attrs in graph.nodes(data=True):

        t = attrs.get("type")

        types[t] = types.get(t, 0) + 1

    for t, count in types.items():

        print(f"{t}: {count}")


# =========================
# MAIN
# =========================

def main():

    print("Building innovation graph...")

    graph = build_graph()

    print_summary(graph)

    save_graph(graph, "innovation_graph.json")

    print("Done.")


if __name__ == "__main__":
    main()