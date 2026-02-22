from sqlalchemy.orm import Session
from typing import List, Dict

from app.models.achievement import Achievement
from app.models.student import Student


class AchievementService:

    # -----------------------------------
    # Create Achievement
    # -----------------------------------
    @staticmethod
    def create_achievement(achievement_data, db: Session):
        new_achievement = Achievement(**achievement_data.dict())
        db.add(new_achievement)
        db.commit()
        db.refresh(new_achievement)
        return new_achievement

    # -----------------------------------
    # Get Achievements by Student
    # -----------------------------------
    @staticmethod
    def get_student_achievements(student_id: int, db: Session):
        return db.query(Achievement).filter(
            Achievement.student_id == student_id
        ).all()

    # -----------------------------------
    # Calculate Performance Score
    # -----------------------------------
    @staticmethod
    def calculate_performance_score(student_id: int, db: Session) -> float:
        achievements = db.query(Achievement).filter(
            Achievement.student_id == student_id
        ).all()

        if not achievements:
            return 0.0

        score = 0

        for ach in achievements:
            if ach.outcome:
                if ach.outcome.lower() == "won":
                    score += 10
                elif ach.outcome.lower() == "runner-up":
                    score += 6
                elif ach.outcome.lower() == "participated":
                    score += 2

            if ach.technologies_used:
                score += len(ach.technologies_used) * 0.5

        return round(score, 2)

    # -----------------------------------
    # Analyze Win/Loss Pattern
    # -----------------------------------
    @staticmethod
    def analyze_performance(student_id: int, db: Session) -> Dict:
        achievements = db.query(Achievement).filter(
            Achievement.student_id == student_id
        ).all()

        total = len(achievements)
        wins = 0
        losses = 0
        tech_counter = {}

        for ach in achievements:
            if ach.outcome:
                if ach.outcome.lower() == "won":
                    wins += 1
                elif ach.outcome.lower() in ["lost", "failed"]:
                    losses += 1

            if ach.technologies_used:
                for tech in ach.technologies_used:
                    tech_counter[tech] = tech_counter.get(tech, 0) + 1

        win_rate = (wins / total) * 100 if total > 0 else 0

        most_used_tech = sorted(
            tech_counter.items(),
            key=lambda x: x[1],
            reverse=True
        )

        return {
            "total_participations": total,
            "wins": wins,
            "losses": losses,
            "win_rate_percentage": round(win_rate, 2),
            "most_used_technologies": most_used_tech[:5]
        }

    # -----------------------------------
    # Improvement Suggestions (Basic AI Logic)
    # -----------------------------------
    @staticmethod
    def suggest_improvements(student_id: int, db: Session) -> Dict:
        analysis = AchievementService.analyze_performance(student_id, db)

        suggestions = []

        if analysis["win_rate_percentage"] < 40:
            suggestions.append("Improve problem-solving and domain depth.")

        if analysis["wins"] == 0:
            suggestions.append("Collaborate with stronger peers or mentors.")

        if len(analysis["most_used_technologies"]) < 2:
            suggestions.append("Diversify your tech stack.")

        return {
            "performance_analysis": analysis,
            "suggestions": suggestions
        }