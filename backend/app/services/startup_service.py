from sqlalchemy.orm import Session
from typing import List, Dict

from app.models.startup import Startup
from app.models.student import Student
from app.models.achievement import Achievement


class StartupService:

    # -----------------------------------
    # Create Startup
    # -----------------------------------
    @staticmethod
    def create_startup(startup_data, db: Session):
        new_startup = Startup(**startup_data.dict())
        db.add(new_startup)
        db.commit()
        db.refresh(new_startup)
        return new_startup

    # -----------------------------------
    # Get All Startups
    # -----------------------------------
    @staticmethod
    def get_all_startups(db: Session):
        return db.query(Startup).all()

    # -----------------------------------
    # Get Startup by ID
    # -----------------------------------
    @staticmethod
    def get_startup_by_id(startup_id: int, db: Session):
        return db.query(Startup).filter(Startup.id == startup_id).first()

    # -----------------------------------
    # Calculate Startup Score
    # -----------------------------------
    @staticmethod
    def calculate_startup_score(startup: Startup, db: Session) -> float:
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
                "startup_id": startup.id,
                "name": startup.name,
                "domain": startup.domain,
                "stage": startup.stage,
                "startup_score": score
            }
            for startup, score in ranked[:limit]
        ]

    # -----------------------------------
    # Get Startups by Domain (Investor Matching)
    # -----------------------------------
    @staticmethod
    def get_startups_by_domain(domain: str, db: Session):
        return db.query(Startup).filter(Startup.domain.ilike(f"%{domain}%")).all()