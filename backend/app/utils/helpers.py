import re
import math
from typing import List, Dict, Any, Optional


# =========================
# TEXT CLEANING
# =========================

def clean_text(text: Optional[str]) -> str:
    """
    Clean text for ML embedding
    """

    if not text:
        return ""

    # Lowercase
    text = text.lower()

    # Remove special characters
    text = re.sub(r"[^a-z0-9\s]", " ", text)

    # Remove extra whitespace
    text = re.sub(r"\s+", " ", text)

    return text.strip()


# =========================
# COMBINE TEXT FIELDS
# =========================

def combine_text_fields(
    *fields: Optional[str]
) -> str:
    """
    Combine multiple text fields safely
    """

    cleaned_fields = [
        clean_text(field)
        for field in fields
        if field
    ]

    return " ".join(cleaned_fields)


# =========================
# NORMALIZE SCORE (0-100)
# =========================

def normalize_score(
    value: float,
    min_value: float,
    max_value: float
) -> float:
    """
    Normalize score between 0 and 100
    """

    if max_value == min_value:
        return 0.0

    normalized = (
        (value - min_value) /
        (max_value - min_value)
    ) * 100

    return round(normalized, 4)


# =========================
# COSINE SIMILARITY
# =========================

def cosine_similarity(
    vec1: List[float],
    vec2: List[float]
) -> float:
    """
    Compute cosine similarity
    """

    if not vec1 or not vec2:
        return 0.0

    dot_product = sum(
        a * b for a, b in zip(vec1, vec2)
    )

    norm1 = math.sqrt(
        sum(a * a for a in vec1)
    )

    norm2 = math.sqrt(
        sum(b * b for b in vec2)
    )

    if norm1 == 0 or norm2 == 0:
        return 0.0

    similarity = dot_product / (norm1 * norm2)

    return round(similarity, 6)


# =========================
# SAFE FLOAT CONVERSION
# =========================

def safe_float(value: Any) -> float:
    """
    Convert safely to float
    """

    try:
        return float(value)
    except (TypeError, ValueError):
        return 0.0


# =========================
# SAFE INT CONVERSION
# =========================

def safe_int(value: Any) -> int:
    """
    Convert safely to int
    """

    try:
        return int(value)
    except (TypeError, ValueError):
        return 0


# =========================
# DICT SORT BY SCORE
# =========================

def sort_by_score(
    items: List[Dict[str, Any]],
    score_key: str = "score",
    reverse: bool = True
) -> List[Dict[str, Any]]:
    """
    Sort list of dict by score
    """

    return sorted(
        items,
        key=lambda x: x.get(score_key, 0),
        reverse=reverse
    )


# =========================
# TOP K RESULTS
# =========================

def top_k(
    items: List[Dict[str, Any]],
    k: int
) -> List[Dict[str, Any]]:
    """
    Return top k items
    """

    return items[:k]


# =========================
# REMOVE DUPLICATES
# =========================

def remove_duplicates(
    items: List[Dict[str, Any]],
    key: str
) -> List[Dict[str, Any]]:
    """
    Remove duplicate items by key
    """

    seen = set()
    result = []

    for item in items:

        value = item.get(key)

        if value not in seen:

            seen.add(value)

            result.append(item)

    return result


# =========================
# BUILD ENTITY LABEL
# =========================

def build_entity_label(
    entity_type: str,
    entity_id: int
) -> str:
    """
    Build graph label
    """

    return f"{entity_type}:{entity_id}"


# =========================
# SAFE DIVISION
# =========================

def safe_divide(
    numerator: float,
    denominator: float
) -> float:
    """
    Avoid division by zero
    """

    if denominator == 0:
        return 0.0

    return numerator / denominator