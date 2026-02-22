from sqlalchemy.orm import Session
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from typing import List

from app.models.student import Student
from app.models.mentor import Mentor
from app.models.startup import Startup


class RecommendationService:

    @staticmethod
    def _compute_similarity(base_text: str, comparison_texts: List[str]):
        """
        Generic cosine similarity engine.
        """
        documents = [base_text] + comparison_texts

        vectorizer = CountVectorizer().fit_transform(documents)
        vectors = vectorizer.toarray()

        similarity_matrix = cosine_similarity([vectors[0]], vectors[1:])
        return similarity_matrix[0]

    # -----------------------------
    # Student ↔ Student Matching
    # -----------------------------
    @staticmethod
    def recommend_students(student_id: int, db: Session):
        base_student = db.query(Student).filter(Student.id == student_id).first()
        if not base_student:
            return []

        other_students = db.query(Student).filter(Student.id != student_id).all()
        if not other_students:
            return []

        base_text = " ".join(base_student.skills + base_student.interests)
        comparison_texts = [
            " ".join(student.skills + student.interests)
            for student in other_students
        ]

        similarities = RecommendationService._compute_similarity(
            base_text, comparison_texts
        )

        recommendations = sorted(
            zip(other_students, similarities),
            key=lambda x: x[1],
            reverse=True
        )

        return [
            {
                "student_id": student.id,
                "name": student.name,
                "similarity_score": float(score)
            }
            for student, score in recommendations
        ]

    # -----------------------------
    # Student ↔ Mentor Matching
    # -----------------------------
    @staticmethod
    def recommend_mentors(student_id: int, db: Session):
        base_student = db.query(Student).filter(Student.id == student_id).first()
        if not base_student:
            return []

        mentors = db.query(Mentor).all()
        if not mentors:
            return []

        base_text = " ".join(base_student.skills + base_student.interests)
        comparison_texts = [
            " ".join(mentor.expertise)
            for mentor in mentors
        ]

        similarities = RecommendationService._compute_similarity(
            base_text, comparison_texts
        )

        recommendations = sorted(
            zip(mentors, similarities),
            key=lambda x: x[1],
            reverse=True
        )

        return [
            {
                "mentor_id": mentor.id,
                "name": mentor.name,
                "organization": mentor.organization,
                "similarity_score": float(score)
            }
            for mentor, score in recommendations
        ]

    # -----------------------------
    # Student ↔ Startup Matching
    # -----------------------------
    @staticmethod
    def recommend_startups(student_id: int, db: Session):
        base_student = db.query(Student).filter(Student.id == student_id).first()
        if not base_student:
            return []

        startups = db.query(Startup).all()
        if not startups:
            return []

        base_text = " ".join(base_student.skills + base_student.interests)
        comparison_texts = [
            " ".join(startup.tech_stack) + " " + startup.domain
            for startup in startups
        ]

        similarities = RecommendationService._compute_similarity(
            base_text, comparison_texts
        )

        recommendations = sorted(
            zip(startups, similarities),
            key=lambda x: x[1],
            reverse=True
        )

        return [
            {
                "startup_id": startup.id,
                "name": startup.name,
                "domain": startup.domain,
                "similarity_score": float(score)
            }
            for startup, score in recommendations
        ]