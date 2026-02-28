"""
Embedding model training / fine-tuning

Fine-tunes SentenceTransformer on Renkei domain data.

Improves semantic similarity understanding for:
- skills
- mentor expertise
- startup domains
- innovation profiles
"""

import os
from sqlalchemy.orm import Session
from sentence_transformers import (
    SentenceTransformer,
    InputExample,
    losses
)
from torch.utils.data import DataLoader

from app.db.session import SessionLocal
from app.config import settings
from app.core.logger import get_logger

from app.models.student import Student
from app.models.mentor import Mentor
from app.models.startup import Startup


logger = get_logger(__name__)


# =========================
# BUILD TRAINING DATA
# =========================

def build_training_examples(db: Session):
    """
    Build semantic similarity training pairs
    """

    logger.info("Building embedding training examples...")

    examples = []

    students = db.query(Student).all()
    mentors = db.query(Mentor).all()
    startups = db.query(Startup).all()

    # Student ↔ Mentor similarity
    for student in students:

        student_text = f"""
        Skills: {student.skills}
        Interests: {student.interests}
        Bio: {student.bio}
        """

        for mentor in mentors:

            mentor_text = f"""
            Expertise: {mentor.expertise}
            Industry: {mentor.industry}
            Bio: {mentor.bio}
            """

            examples.append(
                InputExample(
                    texts=[student_text, mentor_text],
                    label=0.8  # assumed similarity
                )
            )


    # Student ↔ Startup similarity
    for student in students:

        student_text = f"""
        Skills: {student.skills}
        Interests: {student.interests}
        """

        for startup in startups:

            startup_text = f"""
            Domain: {startup.domain}
            Tech stack: {startup.tech_stack}
            Description: {startup.description}
            """

            examples.append(
                InputExample(
                    texts=[student_text, startup_text],
                    label=0.7
                )
            )

    logger.info(f"Built {len(examples)} training examples")

    return examples


# =========================
# TRAIN MODEL
# =========================

def train_embedding_model():

    logger.info("Starting embedding model training...")

    db = SessionLocal()

    try:

        examples = build_training_examples(db)

        if not examples:
            logger.warning("No training data available")
            return


        # Load base model
        model = SentenceTransformer(
            "all-MiniLM-L6-v2"
        )

        train_dataloader = DataLoader(
            examples,
            shuffle=True,
            batch_size=16
        )

        train_loss = losses.CosineSimilarityLoss(model)


        # Train model
        model.fit(
            train_objectives=[
                (train_dataloader, train_loss)
            ],
            epochs=1,
            warmup_steps=100,
            show_progress_bar=True
        )


        # Save model
        save_path = settings.EMBEDDING_MODEL_PATH

        os.makedirs(
            os.path.dirname(save_path),
            exist_ok=True
        )

        model.save(save_path)

        logger.info(
            f"Embedding model saved to {save_path}"
        )

    finally:

        db.close()


# =========================
# CLI ENTRY
# =========================

if __name__ == "__main__":

    train_embedding_model()