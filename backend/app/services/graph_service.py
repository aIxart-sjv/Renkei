import networkx as nx
from sqlalchemy.orm import Session
from typing import Dict, List

from app.models.student import Student
from app.models.achievement import Achievement
from app.models.startup import Startup


class GraphService:

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
        event_map = {}
        for ach in achievements:
            if ach.event_name:
                event_map.setdefault(ach.event_name, []).append(ach.student_id)

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

        innovation_scores = {}

        for node in G.nodes():
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

        students = db.query(Student).all()
        student_map = {s.id: s.name for s in students}

        results = []
        for student_id, score in ranked[:limit]:
            results.append({
                "student_id": student_id,
                "name": student_map.get(student_id),
                "innovation_score": float(score)
            })

        return results

    # -----------------------------------
    # Collaboration Score
    # -----------------------------------
    @staticmethod
    def get_collaboration_score(student_id: int, db: Session) -> float:
        G = GraphService.build_graph(db)

        if student_id not in G:
            return 0.0

        return float(G.degree(student_id))