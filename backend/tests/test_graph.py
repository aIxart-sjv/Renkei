import sys
import os

# Add backend directory to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.database import SessionLocal
from app.services.graph_service import GraphService
from app.models.student import Student
from app.models.connection import Connection
from app.models.achievement import Achievement
from app.models.startup import Startup


def seed_test_data(db):
    """
    Insert sample test data if database is empty
    """

    if db.query(Student).count() > 0:
        print("Test data already exists.")
        return

    print("Seeding test data...")

    # Create students
    student1 = Student(
        name="Alice",
        email="alice@test.com",
        skills=["Python", "AI"],
        interests=["Machine Learning", "Startups"],
    )

    student2 = Student(
        name="Bob",
        email="bob@test.com",
        skills=["JavaScript", "React"],
        interests=["Web Development", "Startups"],
    )

    student3 = Student(
        name="Charlie",
        email="charlie@test.com",
        skills=["Python", "Data Science"],
        interests=["AI", "Analytics"],
    )

    db.add_all([student1, student2, student3])
    db.commit()

    db.refresh(student1)
    db.refresh(student2)
    db.refresh(student3)

    # Create connections
    connection1 = Connection(
        source_id=student1.id,
        target_id=student2.id,
        connection_type="student_student"
    )

    connection2 = Connection(
        source_id=student1.id,
        target_id=student3.id,
        connection_type="student_student"
    )

    db.add_all([connection1, connection2])
    db.commit()

    # Create achievement collaboration
    achievement1 = Achievement(
        title="Hackathon Winner",
        category="Hackathon",
        outcome="Won",
        technologies_used=["Python", "FastAPI"],
        event_name="HackFest 2026",
        student_id=student1.id
    )

    achievement2 = Achievement(
        title="Hackathon Participant",
        category="Hackathon",
        outcome="Participated",
        technologies_used=["React"],
        event_name="HackFest 2026",
        student_id=student2.id
    )

    db.add_all([achievement1, achievement2])
    db.commit()

    # Create startup
    startup = Startup(
        name="AI Startup",
        domain="AI",
        tech_stack=["Python", "FastAPI"],
        founders=[student1.id, student3.id],
        stage="MVP"
    )

    db.add(startup)
    db.commit()

    print("Test data seeded.")


def test_graph_build():
    db = SessionLocal()

    try:
        seed_test_data(db)

        print("\nBuilding graph...")
        graph = GraphService.build_graph(db)

        print(f"Nodes: {len(graph.nodes())}")
        print(f"Edges: {len(graph.edges())}")

        print("\nNodes:")
        for node in graph.nodes(data=True):
            print(node)

        print("\nEdges:")
        for edge in graph.edges(data=True):
            print(edge)

    finally:
        db.close()


def test_innovation_scores():
    db = SessionLocal()

    try:
        print("\nCalculating innovation scores...")

        scores = GraphService.calculate_innovation_scores(db)

        for student_id, score in scores.items():
            print(f"Student {student_id}: Innovation Score = {score}")

    finally:
        db.close()


def test_top_innovators():
    db = SessionLocal()

    try:
        print("\nTop innovators:")

        innovators = GraphService.get_top_innovators(db, limit=5)

        for innovator in innovators:
            print(innovator)

    finally:
        db.close()


def test_graph_visualization_data():
    db = SessionLocal()

    try:
        print("\nGraph visualization data:")

        data = GraphService.get_graph_data(db)

        print("Nodes:")
        print(data["nodes"])

        print("Edges:")
        print(data["edges"])

    finally:
        db.close()


if __name__ == "__main__":

    print("=== TESTING GRAPH SERVICE ===")

    test_graph_build()
    test_innovation_scores()
    test_top_innovators()
    test_graph_visualization_data()

    print("\n=== GRAPH TEST COMPLETE ===")