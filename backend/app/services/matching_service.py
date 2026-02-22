from sqlalchemy.orm import Session
from typing import List, Dict
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from app.models.student import Student
from app.models.mentor import Mentor
from app.models.alumni import Alumni
from app.models.startup import Startup
from app.services.graph_service import GraphService


class MatchingService:

    # -----------------------------------
    # Core similarity function
    # -----------------------------------
    @staticmethod
    def compute_similarity(base_text: str, comparison_texts: List[str]) -> List[float]:

        if not comparison_texts:
            return []

        documents = [base_text] + comparison_texts

        vectorizer = CountVectorizer().fit_transform(documents)
        vectors = vectorizer.toarray()

        similarities = cosine_similarity([vectors[0]], vectors[1:])[0]

        return similarities.tolist()


    # -----------------------------------
    # Match Students with Students
    # -----------------------------------
    @staticmethod
    def match_students(student_id: int, db: Session, limit: int = 10) -> List[Dict]:

        base_student = db.query(Student).filter(Student.id == student_id).first()

        if not base_student:
            return []

        other_students = db.query(Student).filter(Student.id != student_id).all()

        base_text = " ".join(base_student.skills + base_student.interests)

        comparison_texts = [
            " ".join(student.skills + student.interests)
            for student in other_students
        ]

        similarity_scores = MatchingService.compute_similarity(
            base_text,
            comparison_texts
        )

        graph_scores = GraphService.calculate_innovation_scores(db)

        results = []

        for student, similarity in zip(other_students, similarity_scores):

            innovation_bonus = graph_scores.get(student.id, 0)

            final_score = (0.7 * similarity) + (0.3 * innovation_bonus)

            results.append({
                "student_id": student.id,
                "name": student.name,
                "similarity_score": round(similarity, 4),
                "innovation_score": round(innovation_bonus, 4),
                "match_score": round(final_score, 4)
            })

        results.sort(key=lambda x: x["match_score"], reverse=True)

        return results[:limit]


    # -----------------------------------
    # Match Students with Mentors
    # -----------------------------------
    @staticmethod
    def match_mentors(student_id: int, db: Session, limit: int = 10) -> List[Dict]:

        student = db.query(Student).filter(Student.id == student_id).first()

        if not student:
            return []

        mentors = db.query(Mentor).all()

        base_text = " ".join(student.skills + student.interests)

        comparison_texts = [
            " ".join(mentor.expertise)
            for mentor in mentors
        ]

        similarity_scores = MatchingService.compute_similarity(
            base_text,
            comparison_texts
        )

        results = []

        for mentor, similarity in zip(mentors, similarity_scores):

            results.append({
                "mentor_id": mentor.id,
                "name": mentor.name,
                "organization": mentor.organization,
                "expertise": mentor.expertise,
                "match_score": round(similarity, 4)
            })

        results.sort(key=lambda x: x["match_score"], reverse=True)

        return results[:limit]


    # -----------------------------------
    # Match Students with Alumni
    # -----------------------------------
    @staticmethod
    def match_alumni(student_id: int, db: Session, limit: int = 10) -> List[Dict]:

        student = db.query(Student).filter(Student.id == student_id).first()

        if not student:
            return []

        alumni_list = db.query(Alumni).all()

        base_text = " ".join(student.skills + student.interests)

        comparison_texts = [
            " ".join(alumni.expertise)
            for alumni in alumni_list
        ]

        similarity_scores = MatchingService.compute_similarity(
            base_text,
            comparison_texts
        )

        results = []

        for alumni, similarity in zip(alumni_list, similarity_scores):

            results.append({
                "alumni_id": alumni.id,
                "name": alumni.name,
                "organization": alumni.organization,
                "expertise": alumni.expertise,
                "match_score": round(similarity, 4)
            })

        results.sort(key=lambda x: x["match_score"], reverse=True)

        return results[:limit]


    # -----------------------------------
    # Match Students with Startups
    # -----------------------------------
    @staticmethod
    def match_startups(student_id: int, db: Session, limit: int = 10) -> List[Dict]:

        student = db.query(Student).filter(Student.id == student_id).first()

        if not student:
            return []

        startups = db.query(Startup).all()

        base_text = " ".join(student.skills + student.interests)

        comparison_texts = [
            startup.domain + " " + " ".join(startup.tech_stack)
            for startup in startups
        ]

        similarity_scores = MatchingService.compute_similarity(
            base_text,
            comparison_texts
        )

        results = []

        for startup, similarity in zip(startups, similarity_scores):

            results.append({
                "startup_id": startup.id,
                "name": startup.name,
                "domain": startup.domain,
                "tech_stack": startup.tech_stack,
                "match_score": round(similarity, 4)
            })

        results.sort(key=lambda x: x["match_score"], reverse=True)

        return results[:limit]


    # -----------------------------------
    # Full Matching Bundle
    # -----------------------------------
    @staticmethod
    def full_match(student_id: int, db: Session):

        return {
            "students": MatchingService.match_students(student_id, db),
            "mentors": MatchingService.match_mentors(student_id, db),
            "alumni": MatchingService.match_alumni(student_id, db),
            "startups": MatchingService.match_startups(student_id, db),
        }