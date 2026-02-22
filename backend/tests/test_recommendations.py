import sys
import os

# Add backend directory to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.database import SessionLocal
from app.services.recommendation_service import RecommendationService
from app.models.student import Student
from app.models.mentor import Mentor
from app.models.alumni import Alumni
from app.models.startup import Startup


def seed_recommendation_test_data(db):
    """
    Seed database with test data for recommendation testing
    """

    if db.query(Student).count() > 2:
        print("Recommendation test data already exists.")
        return

    print("Seeding recommendation test data...")

    # Create students
    student1 = Student(
        name="Alice",
        email="alice_rec@test.com",
        skills=["Python", "Machine Learning", "FastAPI"],
        interests=["AI", "Startups"],
    )

    student2 = Student(
        name="Bob",
        email="bob_rec@test.com",
        skills=["JavaScript", "React", "Node.js"],
        interests=["Web Development", "Startups"],
    )

    student3 = Student(
        name="Charlie",
        email="charlie_rec@test.com",
        skills=["Python", "Data Science", "TensorFlow"],
        interests=["AI", "Analytics"],
    )

    db.add_all([student1, student2, student3])
    db.commit()

    db.refresh(student1)
    db.refresh(student2)
    db.refresh(student3)

    # Create mentors
    mentor1 = Mentor(
        name="Dr. AI",
        email="mentor_ai@test.com",
        expertise=["Machine Learning", "AI", "Python"],
        organization="Tech University",
        designation="Professor",
    )

    mentor2 = Mentor(
        name="Web Expert",
        email="mentor_web@test.com",
        expertise=["React", "Node.js", "JavaScript"],
        organization="Startup Inc",
        designation="Senior Engineer",
    )

    db.add_all([mentor1, mentor2])
    db.commit()

    # Create alumni
    alumni1 = Alumni(
        name="Alumni AI",
        email="alumni_ai@test.com",
        expertise=["AI", "Deep Learning"],
        organization="Google",
        designation="AI Engineer",
    )

    db.add(alumni1)
    db.commit()

    # Create startups
    startup1 = Startup(
        name="AI Startup",
        domain="Artificial Intelligence",
        tech_stack=["Python", "FastAPI", "TensorFlow"],
        founders=[student1.id],
        stage="MVP",
    )

    startup2 = Startup(
        name="Web Startup",
        domain="Web Development",
        tech_stack=["React", "Node.js"],
        founders=[student2.id],
        stage="Ideation",
    )

    db.add_all([startup1, startup2])
    db.commit()

    print("Recommendation test data seeded.")


def test_student_recommendations():
    db = SessionLocal()

    try:
        seed_recommendation_test_data(db)

        student = db.query(Student).first()

        print("\nTesting student recommendations...")
        recommendations = RecommendationService.recommend_students(student.id, db)

        for rec in recommendations:
            print(rec)

    finally:
        db.close()


def test_mentor_recommendations():
    db = SessionLocal()

    try:
        student = db.query(Student).first()

        print("\nTesting mentor recommendations...")
        recommendations = RecommendationService.recommend_mentors(student.id, db)

        for rec in recommendations:
            print(rec)

    finally:
        db.close()


def test_alumni_recommendations():
    db = SessionLocal()

    try:
        student = db.query(Student).first()

        print("\nTesting alumni recommendations...")
        recommendations = RecommendationService.recommend_alumni(student.id, db)

        for rec in recommendations:
            print(rec)

    finally:
        db.close()


def test_startup_recommendations():
    db = SessionLocal()

    try:
        student = db.query(Student).first()

        print("\nTesting startup recommendations...")
        recommendations = RecommendationService.recommend_startups(student.id, db)

        for rec in recommendations:
            print(rec)

    finally:
        db.close()


def test_full_recommendations():
    db = SessionLocal()

    try:
        student = db.query(Student).first()

        print("\nTesting full recommendation bundle...")
        recommendations = RecommendationService.get_full_recommendations(student.id, db)

        print("\nStudents:")
        print(recommendations["students"])

        print("\nMentors:")
        print(recommendations["mentors"])

        print("\nAlumni:")
        print(recommendations["alumni"])

        print("\nStartups:")
        print(recommendations["startups"])

    finally:
        db.close()


if __name__ == "__main__":

    print("=== TESTING RECOMMENDATION SERVICE ===")

    test_student_recommendations()
    test_mentor_recommendations()
    test_alumni_recommendations()
    test_startup_recommendations()
    test_full_recommendations()

    print("\n=== RECOMMENDATION TEST COMPLETE ===")