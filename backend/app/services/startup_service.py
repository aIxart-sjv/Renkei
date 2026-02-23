from typing import List, Optional, Dict
from sqlalchemy.orm import Session

from app.models.startup import Startup
from app.models.achievement import Achievement
from app.services.graph_service import GraphService


class StartupService:

    # -----------------------------------
    # Get All Startups
    # -----------------------------------
    @staticmethod
    def get_all_startups(db: Session) -> List[Startup]:
        return db.query(Startup).order_by(
            Startup.created_at.desc()
        ).all()

    # -----------------------------------
    # Get Startup by ID
    # -----------------------------------
    @staticmethod
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

    # -----------------------------------
    # Calculate Startup Score
    # -----------------------------------
    @staticmethod
    def calculate_startup_score(startup: Startup, db: Session) -> float:

        score = 0.0

        # Founder innovation score from graph
        innovation_scores = GraphService.calculate_innovation_scores(db)

        if startup.founders:
            founder_scores = [
                innovation_scores.get(founder_id, 0)
                for founder_id in startup.founders
            ]
            score += sum(founder_scores) * 2

        # Achievement score
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
    # Promote Top Startups
    # -----------------------------------
    @staticmethod
    def promote_startups(db: Session, limit: int = 10) -> List[Dict]:

        startups = db.query(Startup).all()

        scored = []

        for startup in startups:

            score = StartupService.calculate_startup_score(
                startup, db
            )

            scored.append({
                "startup_id": startup.id,
                "name": startup.name,
                "domain": startup.domain,
                "stage": startup.stage,
                "startup_score": score
            })

        scored.sort(
            key=lambda x: x["startup_score"],
            reverse=True
        )

        return scored[:limit]

    # -----------------------------------
    # Get Startups by Domain
    # -----------------------------------
    @staticmethod
    def get_startups_by_domain(
        domain: str,
        db: Session
    ) -> List[Startup]:

        return db.query(Startup).filter(
            Startup.domain.ilike(f"%{domain}%")
        ).all()

    # -----------------------------------
    # Update Startup Innovation Scores
    # -----------------------------------
    @staticmethod
    def update_startup_innovation_scores(db: Session):

        startups = db.query(Startup).all()

        for startup in startups:

            score = StartupService.calculate_startup_score(
                startup, db
            )

            startup.innovation_score = score

        db.commit()

        return {
            "message": "Startup innovation scores updated successfully"
        }