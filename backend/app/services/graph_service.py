import networkx as nx
from sqlalchemy.orm import Session
from typing import Dict, List

from app.models.student import Student
from app.models.connection import Connection
from app.models.achievement import Achievement
from app.models.startup import Startup


class GraphService:

    # -----------------------------------
    # Build Graph from Database
    # -----------------------------------
    @staticmethod
    def build_graph(db: Session) -> nx.Graph:
        """
        Builds the campus innovation graph

        Nodes:
            - Students

        Edges:
            - Explicit connections
            - Achievement collaborations
            - Startup founder collaborations
        """

        G = nx.Graph()

        # -----------------------------
        # Add student nodes
        # -----------------------------
        students = db.query(Student).all()

        for student in students:
            G.add_node(
                student.id,
                type="student",
                name=student.name
            )

        # -----------------------------
        # Add explicit connections
        # -----------------------------
        connections = db.query(Connection).all()

        for conn in connections:
            G.add_edge(
                conn.source_id,
                conn.target_id,
                type="connection"
            )

        # -----------------------------
        # Add achievement collaborations
        # -----------------------------
        achievements = db.query(Achievement).all()

        event_map = {}

        for ach in achievements:
            if ach.event_name:
                event_map.setdefault(
                    ach.event_name,
                    []
                ).append(ach.student_id)

        for event, participants in event_map.items():
            for i in range(len(participants)):
                for j in range(i + 1, len(participants)):
                    G.add_edge(
                        participants[i],
                        participants[j],
                        type="achievement"
                    )

        # -----------------------------
        # Add startup collaborations
        # -----------------------------
        startups = db.query(Startup).all()

        for startup in startups:

            if startup.founders:

                founders = startup.founders

                for i in range(len(founders)):
                    for j in range(i + 1, len(founders)):

                        G.add_edge(
                            founders[i],
                            founders[j],
                            type="startup"
                        )

        return G

    # -----------------------------------
    # Calculate Innovation Scores
    # -----------------------------------
    @staticmethod
    def calculate_innovation_scores(
        db: Session
    ) -> Dict[int, float]:

        G = GraphService.build_graph(db)

        if len(G.nodes) == 0:
            return {}

        degree = nx.degree_centrality(G)

        betweenness = nx.betweenness_centrality(G)

        closeness = nx.closeness_centrality(G)

        scores = {}

        for node in G.nodes():

            score = (
                0.4 * degree.get(node, 0) +
                0.4 * betweenness.get(node, 0) +
                0.2 * closeness.get(node, 0)
            )

            scores[node] = round(score, 4)

        return scores

    # -----------------------------------
    # Get Top Innovators
    # -----------------------------------
    @staticmethod
    def get_top_innovators(
        db: Session,
        limit: int = 10
    ) -> List[Dict]:

        scores = GraphService.calculate_innovation_scores(db)

        if not scores:
            return []

        sorted_scores = sorted(
            scores.items(),
            key=lambda x: x[1],
            reverse=True
        )

        students = db.query(Student).all()

        student_map = {
            s.id: s.name for s in students
        }

        results = []

        for student_id, score in sorted_scores[:limit]:

            results.append({
                "student_id": student_id,
                "name": student_map.get(student_id),
                "innovation_score": score
            })

        return results

    # -----------------------------------
    # Collaboration Score
    # -----------------------------------
    @staticmethod
    def get_collaboration_score(
        student_id: int,
        db: Session
    ) -> float:

        G = GraphService.build_graph(db)

        if student_id not in G:
            return 0.0

        return float(G.degree(student_id))

    # -----------------------------------
    # Graph data for frontend visualization
    # -----------------------------------
    @staticmethod
    def get_graph_data(db: Session):

        G = GraphService.build_graph(db)

        nodes = []
        edges = []

        for node_id, data in G.nodes(data=True):

            nodes.append({
                "id": node_id,
                "name": data.get("name"),
                "type": data.get("type")
            })

        for source, target, data in G.edges(data=True):

            edges.append({
                "source": source,
                "target": target,
                "type": data.get("type")
            })

        return {
            "nodes": nodes,
            "edges": edges
        }

    # -----------------------------------
    # Update DB innovation scores
    # -----------------------------------
    @staticmethod
    def update_student_innovation_scores(
        db: Session
    ):

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