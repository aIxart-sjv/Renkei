"""
Seed Database Script

Usage:
    python scripts/seed_data.py

This script populates the database with sample data
for testing ML, graph intelligence, and recommendations.
"""

import random
from faker import Faker

from app.db.session import SessionLocal
import app.db.model_registry
from app.models.user import User, UserRole
from app.models.student import Student
from app.models.mentor import Mentor
from app.models.alumni import Alumni
from app.models.startup import Startup
from app.models.achievement import Achievement
from app.models.connection import Connection

from app.core.security import hash_password


fake = Faker()


# =========================
# CONFIG
# =========================

NUM_STUDENTS = 25
NUM_MENTORS = 10
NUM_ALUMNI = 8
NUM_STARTUPS = 6
NUM_CONNECTIONS = 60
NUM_ACHIEVEMENTS = 80


SKILLS = [
    "Python", "Machine Learning", "AI", "React",
    "FastAPI", "Cybersecurity", "Data Science",
    "Blockchain", "Cloud", "DevOps"
]

DOMAINS = [
    "AI", "FinTech", "HealthTech",
    "EdTech", "Cybersecurity", "Robotics"
]


# =========================
# CREATE USERS
# =========================

def create_users(db):

    users = []

    total = NUM_STUDENTS + NUM_MENTORS + NUM_ALUMNI

    for i in range(total):

        role = (
            UserRole.student if i < NUM_STUDENTS else
            UserRole.mentor if i < NUM_STUDENTS + NUM_MENTORS else
            UserRole.alumni
        )

        user = User(
            email=fake.email(),
            username=fake.user_name(),
            hashed_password=hash_password("password123"),
            role=role,
            full_name=fake.name(),
            is_active=True,
            is_verified=True
        )

        db.add(user)
        users.append(user)

    db.commit()

    return users


# =========================
# CREATE STUDENTS
# =========================

def create_students(db, users):

    students = []

    for user in users[:NUM_STUDENTS]:

        student = Student(
            user_id=user.id,
            university=fake.company(),
            degree="B.Tech",
            field_of_study="Computer Science",
            graduation_year=random.randint(2024, 2028),
            skills=", ".join(random.sample(SKILLS, 3)),
            interests=", ".join(random.sample(SKILLS, 3)),
            bio=fake.text(max_nb_chars=200),
            innovation_score=random.uniform(10, 80),
            collaboration_score=random.uniform(0, 1),
            influence_score=random.uniform(0, 1)
        )

        db.add(student)
        students.append(student)

    db.commit()

    return students


# =========================
# CREATE MENTORS
# =========================

def create_mentors(db, users):

    mentors = []

    mentor_users = users[
        NUM_STUDENTS:NUM_STUDENTS + NUM_MENTORS
    ]

    for user in mentor_users:

        mentor = Mentor(
            user_id=user.id,
            current_company=fake.company(),
            current_role="Senior Engineer",
            industry=random.choice(DOMAINS),
            years_of_experience=random.randint(3, 15),
            skills=", ".join(random.sample(SKILLS, 4)),
            expertise=", ".join(random.sample(SKILLS, 3)),
            mentorship_score=random.uniform(50, 100),
            total_mentees=random.randint(1, 20),
            available=True
        )

        db.add(mentor)
        mentors.append(mentor)

    db.commit()

    return mentors


# =========================
# CREATE ALUMNI
# =========================

def create_alumni(db, users):

    alumni_list = []

    alumni_users = users[-NUM_ALUMNI:]

    for user in alumni_users:

        alumni = Alumni(
            user_id=user.id,
            current_company=fake.company(),
            current_role="Engineer",
            industry=random.choice(DOMAINS),
            years_of_experience=random.randint(2, 10),
            skills=", ".join(random.sample(SKILLS, 3)),
            bio=fake.text(max_nb_chars=200)
        )

        db.add(alumni)
        alumni_list.append(alumni)

    db.commit()

    return alumni_list


# =========================
# CREATE STARTUPS
# =========================

def create_startups(db, students):

    startups = []

    for i in range(NUM_STARTUPS):

        founder = random.choice(students)

        startup = Startup(
            name=fake.company(),
            description=fake.text(max_nb_chars=200),
            domain=random.choice(DOMAINS),
            tech_stack=", ".join(random.sample(SKILLS, 3)),
            innovation_score=random.uniform(30, 90),
            team_size=random.randint(1, 10),
            founder_id=founder.id
        )

        db.add(startup)
        startups.append(startup)

    db.commit()

    return startups


# =========================
# CREATE ACHIEVEMENTS
# =========================

def create_achievements(db, students):

    for _ in range(NUM_ACHIEVEMENTS):

        student = random.choice(students)

        achievement = Achievement(
            student_id=student.id,
            title=fake.catch_phrase(),
            description=fake.text(max_nb_chars=200),
            category="hackathon",
            score=random.uniform(50, 100),
            organization=fake.company()
        )

        db.add(achievement)

    db.commit()


# =========================
# CREATE CONNECTIONS
# =========================

def create_connections(
    db,
    students,
    mentors,
    alumni_list,
    startups
):

    entities = (
        [(s.id, "student") for s in students] +
        [(m.id, "mentor") for m in mentors] +
        [(a.id, "alumni") for a in alumni_list] +
        [(s.id, "startup") for s in startups]
    )

    for _ in range(NUM_CONNECTIONS):

        source = random.choice(entities)
        target = random.choice(entities)

        if source == target:
            continue

        connection = Connection(
            source_id=source[0],
            source_type=source[1],
            target_id=target[0],
            target_type=target[1],
            connection_type="collaboration",
            strength=random.uniform(0.3, 1.0)
        )

        db.add(connection)

    db.commit()


# =========================
# MAIN
# =========================

def main():

    print("Seeding database...")

    db = SessionLocal()

    users = create_users(db)

    students = create_students(db, users)
    mentors = create_mentors(db, users)
    alumni_list = create_alumni(db, users)
    startups = create_startups(db, students)

    create_achievements(db, students)

    create_connections(
        db,
        students,
        mentors,
        alumni_list,
        startups
    )

    db.close()

    print("Database seeded successfully.")


if __name__ == "__main__":
    main()