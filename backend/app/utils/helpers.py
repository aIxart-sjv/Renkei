from typing import List, Dict, Any
from datetime import datetime


# -----------------------------------
# Convert SQLAlchemy object to dict
# -----------------------------------
def model_to_dict(obj) -> Dict[str, Any]:
    """
    Converts SQLAlchemy model instance to dictionary
    """
    return {
        column.name: getattr(obj, column.name)
        for column in obj.__table__.columns
    }


# -----------------------------------
# Safe join for JSON list fields
# -----------------------------------
def safe_join(items: List[str]) -> str:
    """
    Safely joins list of strings into single text.
    Used for similarity matching.
    """
    if not items:
        return ""
    return " ".join([str(item) for item in items])


# -----------------------------------
# Normalize text for matching
# -----------------------------------
def normalize_text(text: str) -> str:
    """
    Normalize text for consistent matching.
    """
    if not text:
        return ""
    return text.lower().strip()


# -----------------------------------
# Get current UTC timestamp
# -----------------------------------
def get_current_timestamp() -> datetime:
    """
    Returns current UTC timestamp
    """
    return datetime.utcnow()


# -----------------------------------
# Calculate percentage safely
# -----------------------------------
def calculate_percentage(part: int, total: int) -> float:
    """
    Safe percentage calculation
    """
    if total == 0:
        return 0.0
    return round((part / total) * 100, 2)


# -----------------------------------
# Remove duplicates from list of dicts
# -----------------------------------
def remove_duplicates(data: List[Dict], key: str) -> List[Dict]:
    """
    Removes duplicate dictionaries based on key
    """
    seen = set()
    result = []

    for item in data:
        value = item.get(key)
        if value not in seen:
            seen.add(value)
            result.append(item)

    return result


# -----------------------------------
# Sort list of dicts by key
# -----------------------------------
def sort_by_key(data: List[Dict], key: str, reverse: bool = True) -> List[Dict]:
    """
    Sort dictionaries safely
    """
    return sorted(
        data,
        key=lambda x: x.get(key, 0),
        reverse=reverse
    )


# -----------------------------------
# Limit results safely
# -----------------------------------
def limit_results(data: List[Any], limit: int = 10) -> List[Any]:
    """
    Limit result size safely
    """
    return data[:limit]


# -----------------------------------
# Format response wrapper
# -----------------------------------
def success_response(message: str, data: Any = None) -> Dict:
    return {
        "success": True,
        "message": message,
        "data": data
    }


def error_response(message: str) -> Dict:
    return {
        "success": False,
        "message": message
    }