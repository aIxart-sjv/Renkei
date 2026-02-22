from sqlalchemy.orm import Session
<<<<<<< HEAD
from typing import List, Dict
=======
from typing import List, Dict, Optional
>>>>>>> ef695a4e05703ba4ec436b8a7ee643f7f61ae8a1

from app.models.startup import Startup
from app.models.student import Student
from app.models.achievement import Achievement
<<<<<<< HEAD
=======
from app.services.graph_service import GraphService
>>>>>>> ef695a4e05703ba4ec436b8a7ee643f7f61ae8a1


class StartupService:

    # -----------------------------------
    # Create Startup
    # -----------------------------------
    @staticmethod
<<<<<<< HEAD
    def create_startup(startup_data, db: Session):
        new_startup = Startup(**startup_data.dict())
        db.add(new_startup)
        db.commit()
        db.refresh(new_startup)
        return new_startup

=======
    def create_startup(startup_data, db: Session) -> Startup:

        new_startup = Startup(
            name=startup_data.name,
            domain=startup_data.domain,
            description=startup_data.description,
            tech_stack=startup_data.tech_stack,
            founders=startup_data.founders,
            stage=startup_data.stage,
            funding_received=startup_data.funding_received,
        )

        db.add(new_startup)
        db.commit()
        db.refresh(new_startup)

        return new_startup


>>>>>>> ef695a4e05703ba4ec436b8a7ee643f7f61ae8a1
    # -----------------------------------
    # Get All Startups
    # -----------------------------------
    @staticmethod
<<<<<<< HEAD
    def get_all_startups(db: Session):
        return db.query(Startup).all()
=======
    def get_all_startups(db: Session) -> List[Startup]:

        return db.query(Startup).order_by(Startup.created_at.desc()).all()

>>>>>>> ef695a4e05703ba4ec436b8a7ee643f7f61ae8a1

    # -----------------------------------
    # Get Startup by ID
    # -----------------------------------
    @staticmethod
<<<<<<< HEAD
    def get_startup_by_id(startup_id: int, db: Session):
        return db.query(Startup).filter(Startup.id == startup_id).first()
=======
    def get_startup_by_id(startup_id: int, db: Session) -> Optional[Startup]:

        return db.query(Startup).filter(
            Startup.id == startup_id
        ).first()


    # -----------------------------------
    # Delete Startup
    # -----------------------------------
    @staticmethod
    def delete_startup(startup_id: int, db: Session) -> bool:

        startup = db.query(Startup).filter(
            Startup.id == startup_id
        ).first()

        if not startup:
            return False

        db.delete(startup)
        db.commit()

        return True

>>>>>>> ef695a4e05703ba4ec436b8a7ee643f7f61ae8a1

    # -----------------------------------
    # Calculate Startup Score
    # -----------------------------------
    @staticmethod
    def calculate_startup_score(startup: Startup, db: Session) -> float:
<<<<<<< HEAD
        """
        Startup score based on:
        - Founder experience
        - Number of achievements
        - Tech stack depth
        - Funding received
        """

        founder_score = 0
        achievement_score = 0
        tech_score = len(startup.tech_stack) if startup.tech_stack else 0
        funding_score = startup.funding_received or 0

        # Founder experience
        if hasattr(startup, "founders") and startup.founders:
            for founder_id in startup.founders:
                achievements = db.query(Achievement).filter(
                    Achievement.student_id == founder_id
                ).count()

                founder_score += achievements

        # Normalize components
        achievement_score = founder_score * 0.5
        tech_score = tech_score * 0.3
        funding_score = funding_score * 0.0001  # scaled down

        total_score = achievement_score + tech_score + funding_score

        return round(total_score, 4)

    # -----------------------------------
    # Promote Startups (InnoVenture Core)
    # -----------------------------------
    @staticmethod
    def promote_startups(db: Session, limit: int = 5) -> List[Dict]:
        startups = db.query(Startup).all()

        scored_startups = []

        for startup in startups:
            score = StartupService.calculate_startup_score(startup, db)
            scored_startups.append((startup, score))

        ranked = sorted(scored_startups, key=lambda x: x[1], reverse=True)

        return [
            {
=======

        score = 0.0

        # Founder innovation score from graph
        innovation_scores = GraphService.calculate_innovation_scores(db)

        if startup.founders:
            founder_scores = [
                innovation_scores.get(founder_id, 0)
                for founder_id in startup.founders
            ]
            score += sum(founder_scores) * 2

        # Achievement score of founders
        achievement_count = 0
        for founder_id in startup.founders or []:
            achievement_count += db.query(Achievement).filter(
                Achievement.student_id == founder_id
            ).count()

        score += achievement_count * 1.5

        # Tech stack strength
        score += len(startup.tech_stack or []) * 1.2

        # Funding strength
        score += (startup.funding_received or 0) * 0.0001

        return round(score, 4)


    # -----------------------------------
    # Promote Top Startups (InnoVenture Core)
    # -----------------------------------
    @staticmethod
    def promote_startups(db: Session, limit: int = 10) -> List[Dict]:

        startups = db.query(Startup).all()

        scored = []

        for startup in startups:
            score = StartupService.calculate_startup_score(startup, db)

            scored.append({
>>>>>>> ef695a4e05703ba4ec436b8a7ee643f7f61ae8a1
                "startup_id": startup.id,
                "name": startup.name,
                "domain": startup.domain,
                "stage": startup.stage,
                "startup_score": score
<<<<<<< HEAD
            }
            for startup, score in ranked[:limit]
        ]

    # -----------------------------------
    # Get Startups by Domain (Investor Matching)
    # -----------------------------------
    @staticmethod
    def get_startups_by_domain(domain: str, db: Session):
        return db.query(Startup).filter(Startup.domain.ilike(f"%{domain}%")).all()
=======
            })

        scored.sort(key=lambda x: x["startup_score"], reverse=True)

        return scored[:limit]


    # -----------------------------------
    # Get Startups by Domain
    # -----------------------------------
    @staticmethod
    def get_startups_by_domain(domain: str, db: Session) -> List[Startup]:

        return db.query(Startup).filter(
            Startup.domain.ilike(f"%{domain}%")
        ).all()


    # -----------------------------------
    # Update Innovation Scores for Startups
    # -----------------------------------
    @staticmethod
    def update_startup_innovation_scores(db: Session):

        startups = db.query(Startup).all()

        for startup in startups:

            score = StartupService.calculate_startup_score(startup, db)

            startup.innovation_score = score

        db.commit()

        return {
            "message": "Startup innovation scores updated successfully"
        }
>>>>>>> ef695a4e05703ba4ec436b8a7ee643f7f61ae8a1
