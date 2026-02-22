import sys
import os

# Add backend directory to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.database import SessionLocal
from app.models.student import Student


def seed_student_test_data(db):
    """
    Seed database with student test data
    """

    if db.query(Student).count() > 0:
        print("Student test data already exists.")
        return

    print("Seeding student test data...")

    student1 = Student(
        name="Test Student 1",
        email="student1@test.com",
        skills=["Python", "FastAPI"],
        interests=["AI", "Startups"],
        bio="Backend developer interested in AI."
    )

    student2 = Student(
        name="Test Student 2",
        email="student2@test.com",
        skills=["React", "JavaScript"],
        interests=["Web Development", "UI/UX"],
        bio="Frontend developer."
    )

    db.add_all([student1, student2])
    db.commit()

    print("Student test data seeded.")


# -----------------------------------
# Test Create Student
# -----------------------------------
def test_create_student():
    db = SessionLocal()

    try:
        print("\nTesting student creation...")

        new_student = Student(
            name="New Test Student",
            email="newstudent@test.com",
            skills=["Machine Learning"],
            interests=["AI"],
            bio="ML enthusiast"
        )

        db.add(new_student)
        db.commit()
        db.refresh(new_student)

        print("Created student:", new_student.id, new_student.name)

    finally:
        db.close()


# -----------------------------------
# Test Get All Students
# -----------------------------------
def test_get_all_students():
    db = SessionLocal()

    try:
        print("\nTesting get all students...")

        students = db.query(Student).all()

        for student in students:
            print({
                "id": student.id,
                "name": student.name,
                "email": student.email,
                "skills": student.skills,
                "interests": student.interests
            })

    finally:
        db.close()


# -----------------------------------
# Test Get Student by ID
# -----------------------------------
def test_get_student_by_id():
    db = SessionLocal()

    try:
        print("\nTesting get student by ID...")

        student = db.query(Student).first()

        if student:
            print({
                "id": student.id,
                "name": student.name,
                "email": student.email
            })
        else:
            print("No student found.")

    finally:
        db.close()


# -----------------------------------
# Test Update Student
# -----------------------------------
def test_update_student():
    db = SessionLocal()

    try:
        print("\nTesting update student...")

        student = db.query(Student).first()

        if student:
            student.bio = "Updated bio for testing."
            db.commit()
            db.refresh(student)

            print("Updated student bio:", student.bio)

        else:
            print("No student found.")

    finally:
        db.close()


# -----------------------------------
# Test Delete Student
# -----------------------------------
def test_delete_student():
    db = SessionLocal()

    try:
        print("\nTesting delete student...")

        student = db.query(Student).filter(
            Student.email == "newstudent@test.com"
        ).first()

        if student:
            db.delete(student)
            db.commit()
            print("Deleted student:", student.email)
        else:
            print("Student not found.")

    finally:
        db.close()


# -----------------------------------
# Test Search Students by Skill
# -----------------------------------
def test_search_students():
    db = SessionLocal()

    try:
        print("\nTesting student search...")

        query = "Python"

        students = db.query(Student).all()

        results = [
            student for student in students
            if query.lower() in " ".join(student.skills).lower()
            or query.lower() in " ".join(student.interests).lower()
        ]

        print(f"Search results for '{query}':")

        for student in results:
            print({
                "id": student.id,
                "name": student.name,
                "skills": student.skills,
                "interests": student.interests
            })

    finally:
        db.close()


# -----------------------------------
# Run All Tests
# -----------------------------------
if __name__ == "__main__":

    print("=== TESTING STUDENT MODEL ===")

    db = SessionLocal()
    seed_student_test_data(db)
    db.close()

    test_create_student()
    test_get_all_students()
    test_get_student_by_id()
    test_update_student()
    test_search_students()
    test_delete_student()

    print("\n=== STUDENT TEST COMPLETE ===")