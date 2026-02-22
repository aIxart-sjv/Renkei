from sqlalchemy.orm import Session
<<<<<<< HEAD
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from typing import List
=======
from typing import List, Dict
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
>>>>>>> ef695a4e05703ba4ec436b8a7ee643f7f61ae8a1

from app.models.student import Student
from app.models.mentor import Mentor
from app.models.startup import Startup
<<<<<<< HEAD
=======
from app.models.alumni import Alumni
from app.services.graph_service import GraphService
>>>>>>> ef695a4e05703ba4ec436b8a7ee643f7f61ae8a1


class RecommendationService:

<<<<<<< HEAD
    @staticmethod
    def _compute_similarity(base_text: str, comparison_texts: List[str]):
        """
        Generic cosine similarity engine.
        """
=======
    # -----------------------------------
    # Internal similarity function
    # -----------------------------------
    @staticmethod
    def _calculate_similarity(base_text: str, comparison_texts: List[str]) -> List[float]:

        if not comparison_texts:
            return []

>>>>>>> ef695a4e05703ba4ec436b8a7ee643f7f61ae8a1
        documents = [base_text] + comparison_texts

        vectorizer = CountVectorizer().fit_transform(documents)
        vectors = vectorizer.toarray()

<<<<<<< HEAD
        similarity_matrix = cosine_similarity([vectors[0]], vectors[1:])
        return similarity_matrix[0]

    # -----------------------------
    # Student ↔ Student Matching
    # -----------------------------
    @staticmethod
    def recommend_students(student_id: int, db: Session):
        base_student = db.query(Student).filter(Student.id == student_id).first()
=======
        similarity_scores = cosine_similarity([vectors[0]], vectors[1:])[0]

        return similarity_scores.tolist()


    # -----------------------------------
    # Recommend Students (Peer Matching)
    # -----------------------------------
    @staticmethod
    def recommend_students(student_id: int, db: Session, limit: int = 10) -> List[Dict]:

        base_student = db.query(Student).filter(Student.id == student_id).first()

>>>>>>> ef695a4e05703ba4ec436b8a7ee643f7f61ae8a1
        if not base_student:
            return []

        other_students = db.query(Student).filter(Student.id != student_id).all()
<<<<<<< HEAD
        if not other_students:
            return []

        base_text = " ".join(base_student.skills + base_student.interests)
=======

        base_text = " ".join(base_student.skills + base_student.interests)

>>>>>>> ef695a4e05703ba4ec436b8a7ee643f7f61ae8a1
        comparison_texts = [
            " ".join(student.skills + student.interests)
            for student in other_students
        ]

<<<<<<< HEAD
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
=======
        similarity_scores = RecommendationService._calculate_similarity(
            base_text,
            comparison_texts
        )

        innovation_scores = GraphService.calculate_innovation_scores(db)

        results = []

        for student, similarity in zip(other_students, similarity_scores):

            innovation_score = innovation_scores.get(student.id, 0)

            final_score = (0.7 * similarity) + (0.3 * innovation_score)

            results.append({
                "student_id": student.id,
                "name": student.name,
                "skills": student.skills,
                "interests": student.interests,
                "similarity_score": round(similarity, 4),
                "innovation_score": round(innovation_score, 4),
                "final_score": round(final_score, 4)
            })

        results.sort(key=lambda x: x["final_score"], reverse=True)

        return results[:limit]


    # -----------------------------------
    # Recommend Mentors
    # -----------------------------------
    @staticmethod
    def recommend_mentors(student_id: int, db: Session, limit: int = 10) -> List[Dict]:

        student = db.query(Student).filter(Student.id == student_id).first()

        if not student:
            return []

        mentors = db.query(Mentor).all()

        base_text = " ".join(student.skills + student.interests)

>>>>>>> ef695a4e05703ba4ec436b8a7ee643f7f61ae8a1
        comparison_texts = [
            " ".join(mentor.expertise)
            for mentor in mentors
        ]

<<<<<<< HEAD
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
=======
        similarity_scores = RecommendationService._calculate_similarity(
            base_text,
            comparison_texts
        )

        results = []

        for mentor, similarity in zip(mentors, similarity_scores):

            results.append({
                "mentor_id": mentor.id,
                "name": mentor.name,
                "organization": mentor.organization,
                "designation": mentor.designation,
                "expertise": mentor.expertise,
                "match_score": round(similarity, 4)
            })

        results.sort(key=lambda x: x["match_score"], reverse=True)

        return results[:limit]


    # -----------------------------------
    # Recommend Alumni
    # -----------------------------------
    @staticmethod
    def recommend_alumni(student_id: int, db: Session, limit: int = 10) -> List[Dict]:

        student = db.query(Student).filter(Student.id == student_id).first()

        if not student:
            return []

        alumni_list = db.query(Alumni).all()

        base_text = " ".join(student.skills + student.interests)

        comparison_texts = [
            " ".join(alumni.expertise)
            for alumni in alumni_list
        ]

        similarity_scores = RecommendationService._calculate_similarity(
            base_text,
            comparison_texts
        )

        results = []

        for alumni, similarity in zip(alumni_list, similarity_scores):

            results.append({
                "alumni_id": alumni.id,
                "name": alumni.name,
                "organization": alumni.organization,
                "designation": alumni.designation,
                "expertise": alumni.expertise,
                "match_score": round(similarity, 4)
            })

        results.sort(key=lambda x: x["match_score"], reverse=True)

        return results[:limit]


    # -----------------------------------
    # Recommend Startups
    # -----------------------------------
    @staticmethod
    def recommend_startups(student_id: int, db: Session, limit: int = 10) -> List[Dict]:

        student = db.query(Student).filter(Student.id == student_id).first()

        if not student:
            return []

        startups = db.query(Startup).all()

        base_text = " ".join(student.skills + student.interests)

        comparison_texts = [
            startup.domain + " " + " ".join(startup.tech_stack)
            for startup in startups
        ]

        similarity_scores = RecommendationService._calculate_similarity(
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
    # Full Recommendation Bundle
    # -----------------------------------
    @staticmethod
    def get_full_recommendations(student_id: int, db: Session):

        return {
            "students": RecommendationService.recommend_students(student_id, db),
            "mentors": RecommendationService.recommend_mentors(student_id, db),
            "alumni": RecommendationService.recommend_alumni(student_id, db),
            "startups": RecommendationService.recommend_startups(student_id, db),
        }
>>>>>>> ef695a4e05703ba4ec436b8a7ee643f7f61ae8a1
