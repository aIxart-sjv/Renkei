"""
Vector store using FAISS for fast similarity search

Stores and retrieves embeddings efficiently.

Used for:
- Recommendation search
- Similarity search
- Fast nearest neighbor lookup
"""

import os
import faiss
import numpy as np
import pickle
from typing import List, Tuple

from app.config import settings
from app.core.logger import get_logger


logger = get_logger(__name__)


class VectorStore:
    """
    FAISS-based vector storage and retrieval
    """

    def __init__(
        self,
        dimension: int = 384,
        index_path: str = None,
        metadata_path: str = None
    ):

        self.dimension = dimension

        self.index_path = index_path or settings.VECTOR_INDEX_PATH
        self.metadata_path = metadata_path or settings.VECTOR_METADATA_PATH

        self.index = None
        self.metadata = []

        self.load()


    # =========================
    # CREATE NEW INDEX
    # =========================

    def create_index(self):

        logger.info("Creating new FAISS index")

        self.index = faiss.IndexFlatIP(
            self.dimension
        )

        self.metadata = []


    # =========================
    # LOAD INDEX
    # =========================

    def load(self):

        try:

            if os.path.exists(self.index_path):

                logger.info("Loading vector index")

                self.index = faiss.read_index(
                    self.index_path
                )

                if os.path.exists(self.metadata_path):

                    with open(
                        self.metadata_path,
                        "rb"
                    ) as f:

                        self.metadata = pickle.load(f)

            else:

                self.create_index()

        except Exception as e:

            logger.error(f"Vector store load failed: {e}")

            self.create_index()


    # =========================
    # SAVE INDEX
    # =========================

    def save(self):

        try:

            os.makedirs(
                os.path.dirname(self.index_path),
                exist_ok=True
            )

            faiss.write_index(
                self.index,
                self.index_path
            )

            with open(
                self.metadata_path,
                "wb"
            ) as f:

                pickle.dump(self.metadata, f)

            logger.info("Vector store saved")

        except Exception as e:

            logger.error(f"Vector store save failed: {e}")


    # =========================
    # ADD VECTOR
    # =========================

    def add(
        self,
        vector: np.ndarray,
        metadata: dict
    ):

        try:

            vector = vector.astype(np.float32)

            self.index.add(
                vector.reshape(1, -1)
            )

            self.metadata.append(metadata)

        except Exception as e:

            logger.error(f"Vector add failed: {e}")


    # =========================
    # ADD BATCH
    # =========================

    def add_batch(
        self,
        vectors: List[np.ndarray],
        metadata_list: List[dict]
    ):

        try:

            vectors = np.array(
                vectors,
                dtype=np.float32
            )

            self.index.add(vectors)

            self.metadata.extend(metadata_list)

        except Exception as e:

            logger.error(f"Batch add failed: {e}")


    # =========================
    # SEARCH
    # =========================

    def search(
        self,
        query_vector: np.ndarray,
        top_k: int = 10
    ) -> List[Tuple[dict, float]]:
        """
        Search most similar vectors
        """

        try:

            query_vector = query_vector.astype(
                np.float32
            ).reshape(1, -1)

            scores, indices = self.index.search(
                query_vector,
                top_k
            )

            results = []

            for idx, score in zip(
                indices[0],
                scores[0]
            ):

                if idx < len(self.metadata):

                    results.append(
                        (
                            self.metadata[idx],
                            float(score)
                        )
                    )

            return results

        except Exception as e:

            logger.error(f"Vector search failed: {e}")

            return []


    # =========================
    # CLEAR INDEX
    # =========================

    def clear(self):

        self.create_index()

        logger.info("Vector store cleared")


    # =========================
    # COUNT
    # =========================

    def count(self) -> int:

        return self.index.ntotal


# =========================
# SINGLETON INSTANCE
# =========================

_vector_store_instance = None


def get_vector_store() -> VectorStore:

    global _vector_store_instance

    if _vector_store_instance is None:

        _vector_store_instance = VectorStore()

    return _vector_store_instance