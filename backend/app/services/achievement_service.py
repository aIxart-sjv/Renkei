from sqlalchemy.orm import Session
from typing import List, Dict

from app.models.achievement import Achievement
from app.models.student import Student


class AchievementService:

    # -----------------------------------
    # Create Achievement
    # -----------------------------------
    @staticmethod
<<<<<<< HEAD
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
=======
    def create_achievement(achievement_data, db: Session) -> Achievement:
        new_achievement = Achievement(
            title=achievement_data.title,
            description=achievement_data.description,
            category=achievement_data.category,
            outcome=achievement_data.outcome,
            technologies_used=achievement_data.technologies_used,
            event_name=achievement_data.event_name,
            date=achievement_data.date,
            student_id=achievement_data.student_id,
        )

        db.add(new_achievement)
        db.commit()
        db.refresh(new_achievement)

        return new_achievement


    # -----------------------------------
    # Get Achievements for a Student
    # -----------------------------------
    @staticmethod
    def get_student_achievements(student_id: int, db: Session) -> List[Achievement]:
        return db.query(Achievement).filter(
            Achievement.student_id == student_id
        ).order_by(Achievement.created_at.desc()).all()


    # -----------------------------------
    # Delete Achievement
    # -----------------------------------
    @staticmethod
    def delete_achievement(achievement_id: int, db: Session) -> bool:
        achievement = db.query(Achievement).filter(
            Achievement.id == achievement_id
        ).first()

        if not achievement:
            return False

        db.delete(achievement)
        db.commit()

        return True

>>>>>>> ef695a4e05703ba4ec436b8a7ee643f7f61ae8a1

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

<<<<<<< HEAD
        score = 0

        for ach in achievements:
            if ach.outcome:
                if ach.outcome.lower() == "won":
                    score += 10
                elif ach.outcome.lower() == "runner-up":
                    score += 6
                elif ach.outcome.lower() == "participated":
                    score += 2

=======
        score = 0.0

        for ach in achievements:

            # Outcome scoring
            if ach.outcome:
                outcome = ach.outcome.lower()

                if outcome == "won":
                    score += 10

                elif outcome == "runner-up":
                    score += 7

                elif outcome == "participated":
                    score += 3

                elif outcome in ["lost", "failed"]:
                    score += 1

            # Tech stack diversity scoring
>>>>>>> ef695a4e05703ba4ec436b8a7ee643f7f61ae8a1
            if ach.technologies_used:
                score += len(ach.technologies_used) * 0.5

        return round(score, 2)

<<<<<<< HEAD
    # -----------------------------------
    # Analyze Win/Loss Pattern
    # -----------------------------------
    @staticmethod
    def analyze_performance(student_id: int, db: Session) -> Dict:
=======

    # -----------------------------------
    # Analyze Performance
    # -----------------------------------
    @staticmethod
    def analyze_performance(student_id: int, db: Session) -> Dict:

>>>>>>> ef695a4e05703ba4ec436b8a7ee643f7f61ae8a1
        achievements = db.query(Achievement).filter(
            Achievement.student_id == student_id
        ).all()

        total = len(achievements)
        wins = 0
<<<<<<< HEAD
        losses = 0
        tech_counter = {}

        for ach in achievements:
            if ach.outcome:
                if ach.outcome.lower() == "won":
                    wins += 1
                elif ach.outcome.lower() in ["lost", "failed"]:
=======
        runner_ups = 0
        participations = 0
        losses = 0

        tech_usage = {}

        for ach in achievements:

            if ach.outcome:
                outcome = ach.outcome.lower()

                if outcome == "won":
                    wins += 1

                elif outcome == "runner-up":
                    runner_ups += 1

                elif outcome == "participated":
                    participations += 1

                elif outcome in ["lost", "failed"]:
>>>>>>> ef695a4e05703ba4ec436b8a7ee643f7f61ae8a1
                    losses += 1

            if ach.technologies_used:
                for tech in ach.technologies_used:
<<<<<<< HEAD
                    tech_counter[tech] = tech_counter.get(tech, 0) + 1

        win_rate = (wins / total) * 100 if total > 0 else 0

        most_used_tech = sorted(
            tech_counter.items(),
=======
                    tech_usage[tech] = tech_usage.get(tech, 0) + 1

        win_rate = (wins / total * 100) if total > 0 else 0

        most_used_tech = sorted(
            tech_usage.items(),
>>>>>>> ef695a4e05703ba4ec436b8a7ee643f7f61ae8a1
            key=lambda x: x[1],
            reverse=True
        )

        return {
<<<<<<< HEAD
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
=======
            "total_achievements": total,
            "wins": wins,
            "runner_ups": runner_ups,
            "participations": participations,
            "losses": losses,
            "win_rate_percentage": round(win_rate, 2),
            "most_used_technologies": most_used_tech[:5],
        }


    # -----------------------------------
    # Suggest Improvements (AI logic base)
    # -----------------------------------
    @staticmethod
    def suggest_improvements(student_id: int, db: Session) -> Dict:

>>>>>>> ef695a4e05703ba4ec436b8a7ee643f7f61ae8a1
        analysis = AchievementService.analyze_performance(student_id, db)

        suggestions = []

<<<<<<< HEAD
        if analysis["win_rate_percentage"] < 40:
            suggestions.append("Improve problem-solving and domain depth.")

        if analysis["wins"] == 0:
            suggestions.append("Collaborate with stronger peers or mentors.")

        if len(analysis["most_used_technologies"]) < 2:
            suggestions.append("Diversify your tech stack.")

        return {
            "performance_analysis": analysis,
=======
        if analysis["total_achievements"] == 0:
            suggestions.append("Start participating in hackathons and projects.")

        if analysis["win_rate_percentage"] < 40:
            suggestions.append("Improve problem-solving skills and preparation.")

        if analysis["wins"] == 0:
            suggestions.append("Collaborate with experienced teammates or mentors.")

        if len(analysis["most_used_technologies"]) < 3:
            suggestions.append("Expand your tech stack to increase competitiveness.")

        if not suggestions:
            suggestions.append("Excellent performance. Continue building advanced projects.")

        return {
            "analysis": analysis,
>>>>>>> ef695a4e05703ba4ec436b8a7ee643f7f61ae8a1
            "suggestions": suggestions
        }