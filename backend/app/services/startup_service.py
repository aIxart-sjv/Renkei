from sqlalchemy.orm import Session
from typing import List, Optional

from app.models.startup import Startup
from app.schemas.startup import (
    StartupCreate,
    StartupUpdate
)

from app.core.logger import get_logger

from app.services.ml_service import (
    generate_entity_embedding
)


logger = get_logger(__name__)


# =========================
# CREATE STARTUP
# =========================

def create_startup(
    db: Session,
    startup_data: StartupCreate
) -> Startup:
    """
    Create startup profile
    """

    try:

        startup = Startup(
            name=startup_data.name,
            description=startup_data.description,
            domain=startup_data.domain,
            industry=startup_data.industry,
            tech_stack=startup_data.tech_stack,
            product_stage=startup_data.product_stage,
            innovation_score=startup_data.innovation_score or 0.0,
            team_size=startup_data.team_size or 1,
            website=startup_data.website,
            github_url=startup_data.github_url,
            linkedin_url=startup_data.linkedin_url,
            location=startup_data.location,
            founder_id=startup_data.founder_id
        )

        db.add(startup)
        db.commit()
        db.refresh(startup)

        logger.info(f"Startup created: {startup.id}")


        # Generate embedding for ML recommendations
        embedding_text = build_startup_embedding_text(startup)

        generate_entity_embedding(
            db,
            startup.id,
            "startup",
            embedding_text
        )


        return startup


    except Exception as e:

        db.rollback()

        logger.error(f"Startup creation failed: {e}")

        raise


# =========================
# GET STARTUP BY ID
# =========================

def get_startup(
    db: Session,
    startup_id: int
) -> Optional[Startup]:

    return db.query(Startup).filter(
        Startup.id == startup_id
    ).first()


# =========================
# GET ALL STARTUPS
# =========================

def get_all_startups(
    db: Session,
    skip: int = 0,
    limit: int = 100
) -> List[Startup]:

    return db.query(Startup)\
        .offset(skip)\
        .limit(limit)\
        .all()


# =========================
# GET STARTUPS BY FOUNDER
# =========================

def get_startups_by_founder(
    db: Session,
    founder_id: int
) -> List[Startup]:

    return db.query(Startup).filter(
        Startup.founder_id == founder_id
    ).all()


# =========================
# UPDATE STARTUP
# =========================

def update_startup(
    db: Session,
    startup_id: int,
    update_data: StartupUpdate
) -> Optional[Startup]:

    startup = get_startup(
        db,
        startup_id
    )

    if not startup:
        return None


    try:

        update_fields = update_data.dict(
            exclude_unset=True
        )

        for field, value in update_fields.items():

            setattr(startup, field, value)


        db.commit()
        db.refresh(startup)

        logger.info(f"Startup updated: {startup.id}")


        # Regenerate embedding
        embedding_text = build_startup_embedding_text(startup)

        generate_entity_embedding(
            db,
            startup.id,
            "startup",
            embedding_text
        )


        return startup


    except Exception as e:

        db.rollback()

        logger.error(f"Startup update failed: {e}")

        raise


# =========================
# DELETE STARTUP
# =========================

def delete_startup(
    db: Session,
    startup_id: int
) -> bool:

    startup = get_startup(db, startup_id)

    if not startup:
        return False


    try:

        db.delete(startup)
        db.commit()

        logger.info(f"Startup deleted: {startup_id}")

        return True

    except Exception as e:

        db.rollback()

        logger.error(f"Startup deletion failed: {e}")

        raise


# =========================
# GET TOP STARTUPS
# =========================

def get_top_startups(
    db: Session,
    limit: int = 10
) -> List[Startup]:

    return db.query(Startup)\
        .order_by(Startup.innovation_score.desc())\
        .limit(limit)\
        .all()


# =========================
# SEARCH STARTUPS BY DOMAIN
# =========================

def search_startups_by_domain(
    db: Session,
    domain: str
) -> List[Startup]:

    return db.query(Startup).filter(
        Startup.domain.ilike(f"%{domain}%")
    ).all()


# =========================
# BUILD EMBEDDING TEXT
# =========================

def build_startup_embedding_text(
    startup: Startup
) -> str:
    """
    Build text for embedding model
    """

    parts = [
        startup.name or "",
        startup.description or "",
        startup.domain or "",
        startup.industry or "",
        startup.tech_stack or "",
        startup.product_stage or "",
        startup.location or ""
    ]

    return " ".join(parts)