import networkx as nx
from sqlalchemy.orm import Session
from typing import Dict, List

from app.models.student import Student
<<<<<<< HEAD
=======
from app.models.connection import Connection
>>>>>>> ef695a4e05703ba4ec436b8a7ee643f7f61ae8a1
from app.models.achievement import Achievement
from app.models.startup import Startup


class GraphService:

<<<<<<< HEAD
    @staticmethod
    def build_graph(db: Session) -> nx.Graph:
        """
        Builds a campus collaboration graph.
        Nodes: Students
        Edges: Shared achievements, startup collaborations
        """
        G = nx.Graph()

        students = db.query(Student).all()
        achievements = db.query(Achievement).all()
        startups = db.query(Startup).all()

        # Add student nodes
        for student in students:
            G.add_node(student.id, label=student.name)

        # Connect students who worked on same achievement event
=======
    # -----------------------------------
    # Build Graph from Database
    # -----------------------------------
    @staticmethod
    def build_graph(db: Session) -> nx.Graph:
        """
        Builds the full campus graph using:
        - Students as nodes
        - Connections as edges
        - Startup founder relationships
        - Achievement collaborations
        """

        G = nx.Graph()

        # Add student nodes
        students = db.query(Student).all()
        for student in students:
            G.add_node(
                student.id,
                type="student",
                name=student.name
            )

        # Add explicit connections
        connections = db.query(Connection).all()
        for conn in connections:
            G.add_edge(
                conn.source_id,
                conn.target_id,
                type=conn.connection_type
            )

        # Add startup founder relationships
        startups = db.query(Startup).all()
        for startup in startups:
            if startup.founders:
                founders = startup.founders

                for i in range(len(founders)):
                    for j in range(i + 1, len(founders)):
                        G.add_edge(
                            founders[i],
                            founders[j],
                            type="startup_collaboration"
                        )

        # Add achievement collaboration relationships
        achievements = db.query(Achievement).all()

>>>>>>> ef695a4e05703ba4ec436b8a7ee643f7f61ae8a1
        event_map = {}
        for ach in achievements:
            if ach.event_name:
                event_map.setdefault(ach.event_name, []).append(ach.student_id)

<<<<<<< HEAD
        for participants in event_map.values():
            for i in range(len(participants)):
                for j in range(i + 1, len(participants)):
                    G.add_edge(participants[i], participants[j], type="collaboration")

        # Connect startup founders
        for startup in startups:
            if hasattr(startup, "founders") and startup.founders:
                founders = startup.founders
                for i in range(len(founders)):
                    for j in range(i + 1, len(founders)):
                        G.add_edge(founders[i], founders[j], type="startup")

        return G

    # -----------------------------------
    # Innovation Score
    # -----------------------------------
    @staticmethod
    def calculate_innovation_scores(db: Session) -> Dict[int, float]:
        G = GraphService.build_graph(db)

        # Degree centrality = collaboration activity
        degree_centrality = nx.degree_centrality(G)

        # Betweenness centrality = influence in network
        betweenness = nx.betweenness_centrality(G)
=======
        for event, participants in event_map.items():
            for i in range(len(participants)):
                for j in range(i + 1, len(participants)):
                    G.add_edge(
                        participants[i],
                        participants[j],
                        type="achievement_collaboration"
                    )

        return G


    # -----------------------------------
    # Innovation Score Calculation
    # -----------------------------------
    @staticmethod
    def calculate_innovation_scores(db: Session) -> Dict[int, float]:

        G = GraphService.build_graph(db)

        if len(G.nodes) == 0:
            return {}

        degree_centrality = nx.degree_centrality(G)
        betweenness_centrality = nx.betweenness_centrality(G)
        closeness_centrality = nx.closeness_centrality(G)
>>>>>>> ef695a4e05703ba4ec436b8a7ee643f7f61ae8a1

        innovation_scores = {}

        for node in G.nodes():
<<<<<<< HEAD
            innovation_scores[node] = (
                0.6 * degree_centrality.get(node, 0)
                + 0.4 * betweenness.get(node, 0)
            )

        return innovation_scores

    # -----------------------------------
    # Top Innovators
    # -----------------------------------
    @staticmethod
    def get_top_innovators(db: Session, limit: int = 5) -> List[Dict]:
        scores = GraphService.calculate_innovation_scores(db)

        ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)
=======

            score = (
                0.4 * degree_centrality.get(node, 0) +
                0.4 * betweenness_centrality.get(node, 0) +
                0.2 * closeness_centrality.get(node, 0)
            )

            innovation_scores[node] = round(score, 4)

        return innovation_scores


    # -----------------------------------
    # Get Top Innovators
    # -----------------------------------
    @staticmethod
    def get_top_innovators(db: Session, limit: int = 10) -> List[Dict]:

        scores = GraphService.calculate_innovation_scores(db)

        if not scores:
            return []

        sorted_scores = sorted(
            scores.items(),
            key=lambda x: x[1],
            reverse=True
        )
>>>>>>> ef695a4e05703ba4ec436b8a7ee643f7f61ae8a1

        students = db.query(Student).all()
        student_map = {s.id: s.name for s in students}

        results = []
<<<<<<< HEAD
        for student_id, score in ranked[:limit]:
            results.append({
                "student_id": student_id,
                "name": student_map.get(student_id),
                "innovation_score": float(score)
=======

        for student_id, score in sorted_scores[:limit]:
            results.append({
                "student_id": student_id,
                "name": student_map.get(student_id),
                "innovation_score": score
>>>>>>> ef695a4e05703ba4ec436b8a7ee643f7f61ae8a1
            })

        return results

<<<<<<< HEAD
    # -----------------------------------
    # Collaboration Score
    # -----------------------------------
    @staticmethod
    def get_collaboration_score(student_id: int, db: Session) -> float:
=======

    # -----------------------------------
    # Collaboration Score for Student
    # -----------------------------------
    @staticmethod
    def get_collaboration_score(student_id: int, db: Session) -> float:

>>>>>>> ef695a4e05703ba4ec436b8a7ee643f7f61ae8a1
        G = GraphService.build_graph(db)

        if student_id not in G:
            return 0.0

<<<<<<< HEAD
        return float(G.degree(student_id))
=======
        return float(G.degree(student_id))


    # -----------------------------------
    # Get Graph Data (for visualization)
    # -----------------------------------
    @staticmethod
    def get_graph_data(db: Session):

        G = GraphService.build_graph(db)

        nodes = []
        edges = []

        for node in G.nodes(data=True):
            nodes.append({
                "id": node[0],
                "name": node[1].get("name"),
                "type": node[1].get("type")
            })

        for edge in G.edges(data=True):
            edges.append({
                "source": edge[0],
                "target": edge[1],
                "type": edge[2].get("type")
            })

        return {
            "nodes": nodes,
            "edges": edges
        }


    # -----------------------------------
    # Update Innovation Scores in DB
    # -----------------------------------
    @staticmethod
    def update_student_innovation_scores(db: Session):

        scores = GraphService.calculate_innovation_scores(db)

        for student_id, score in scores.items():

            student = db.query(Student).filter(
                Student.id == student_id
            ).first()

            if student:
                student.innovation_score = score

        db.commit()

        return {
            "message": "Innovation scores updated successfully"
        }
>>>>>>> ef695a4e05703ba4ec436b8a7ee643f7f61ae8a1
