"""
Database seed script

Populates database with demo data for:
- ML training
- Graph intelligence
- Testing
"""

from sqlalchemy.orm import Session
import random

from app.db.session import SessionLocal
from app.core.security import hash_password
from app.core.constants import (
    ROLE_ADMIN,
    ROLE_STUDENT,
    ROLE_MENTOR,
    ROLE_ALUMNI,
    CONNECTION_COLLABORATION,
    CONNECTION_MENTORSHIP
)

from app.models.user import User
from app.models.student import Student
from app.models.mentor import Mentor
from app.models.alumni import Alumni
from app.models.startup import Startup
from app.models.achievement import Achievement
from app.models.connection import Connection

from app.core.logger import get_logger


logger = get_logger(__name__)


# =========================
# SAMPLE DATA
# =========================

SKILLS = [
    "Python",
    "Machine Learning",
    "React",
    "FastAPI",
    "Cybersecurity",
    "Blockchain",
    "Data Science",
    "Cloud Computing",
]

INDUSTRIES = [
    "AI",
    "Fintech",
    "Healthcare",
    "EdTech",
    "Cybersecurity"
]


# =========================
# CREATE USERS
# =========================

def create_users(db: Session):

    logger.info("Seeding users...")

    users = []

    for i in range(10):

        user = User(
            email=f"student{i}@renkei.com",
            name=f"Student {i}",
            hashed_password=hash_password("password123"),
            role=ROLE_STUDENT,
            is_active=True
        )

        db.add(user)
        users.append(user)

    for i in range(5):

        user = User(
            email=f"mentor{i}@renkei.com",
            name=f"Mentor {i}",
            hashed_password=hash_password("password123"),
            role=ROLE_MENTOR,
            is_active=True
        )

        db.add(user)
        users.append(user)

    db.commit()

    return users


# =========================
# CREATE STUDENTS
# =========================

def create_students(db: Session, users):

    logger.info("Seeding students...")

    students = []

    student_users = [u for u in users if u.role == ROLE_STUDENT]

    for user in student_users:

        student = Student(
            user_id=user.id,
            skills=random.choice(SKILLS),
            interests=random.choice(INDUSTRIES),
            bio="Passionate innovator",
            education="B.Tech",
            graduation_year=2026,
            innovation_score=random.uniform(40, 90),
            collaboration_score=random.uniform(40, 90)
        )

        db.add(student)
        students.append(student)

    db.commit()

    return students


# =========================
# CREATE MENTORS
# =========================

def create_mentors(db: Session, users):

    logger.info("Seeding mentors...")

    mentors = []

    mentor_users = [u for u in users if u.role == ROLE_MENTOR]

    for user in mentor_users:

        mentor = Mentor(
            user_id=user.id,
            expertise=random.choice(SKILLS),
            industry=random.choice(INDUSTRIES),
            years_of_experience=random.randint(3, 15),
            current_company="Tech Corp",
            current_role="Senior Engineer",
            bio="Experienced mentor",
            availability=True
        )

        db.add(mentor)
        mentors.append(mentor)

    db.commit()

    return mentors


# =========================
# CREATE STARTUPS
# =========================

def create_startups(db: Session):

    logger.info("Seeding startups...")

    startups = []

    for i in range(5):

        startup = Startup(
            name=f"Startup {i}",
            description="Innovative startup",
            domain=random.choice(INDUSTRIES),
            tech_stack=random.choice(SKILLS),
            founder_id=1,
            stage="mvp",
            industry=random.choice(INDUSTRIES),
            website="https://example.com",
            location="Remote"
        )

        db.add(startup)
        startups.append(startup)

    db.commit()

    return startups


# =========================
# CREATE CONNECTIONS
# =========================

def create_connections(db: Session, students, mentors):

    logger.info("Seeding connections...")

    for student in students:

        mentor = random.choice(mentors)

        connection = Connection(
            source_id=student.id,
            source_type="student",
            target_id=mentor.id,
            target_type="mentor",
            connection_type=CONNECTION_MENTORSHIP,
            strength=random.uniform(0.5, 1.0)
        )

        db.add(connection)

    db.commit()


# =========================
# MAIN SEED FUNCTION
# =========================

def seed_database():

    logger.info("Starting database seed...")

    db = SessionLocal()

    try:

        users = create_users(db)

        students = create_students(db, users)

        mentors = create_mentors(db, users)

        startups = create_startups(db)

        create_connections(db, students, mentors)

    finally:

        db.close()

    logger.info("Database seeding complete")


# =========================
# CLI ENTRY POINT
# =========================

if __name__ == "__main__":

    seed_database()