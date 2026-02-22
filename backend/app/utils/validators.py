import re
from typing import List, Any


# -----------------------------------
# Email Validator
# -----------------------------------
def validate_email(email: str) -> bool:
    """
    Validates email format
    """
    if not email:
        return False

    pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    return re.match(pattern, email) is not None


# -----------------------------------
# Password Validator
# -----------------------------------
def validate_password(password: str) -> bool:
    """
    Password must contain:
    - Minimum 8 characters
    - One uppercase letter
    - One lowercase letter
    - One number
    """
    if not password or len(password) < 8:
        return False

    if not re.search(r"[A-Z]", password):
        return False

    if not re.search(r"[a-z]", password):
        return False

    if not re.search(r"\d", password):
        return False

    return True


# -----------------------------------
# Name Validator
# -----------------------------------
def validate_name(name: str) -> bool:
    """
    Validates person name
    """
    if not name:
        return False

    name = name.strip()

    return len(name) >= 2 and len(name) <= 100


# -----------------------------------
# Skills / Interests Validator
# -----------------------------------
def validate_list_field(field: List[str], min_items: int = 1, max_items: int = 50) -> bool:
    """
    Validates skills, interests, expertise, tech stack lists
    """
    if not isinstance(field, list):
        return False

    if len(field) < min_items or len(field) > max_items:
        return False

    for item in field:
        if not isinstance(item, str):
            return False

        if len(item.strip()) == 0:
            return False

    return True


# -----------------------------------
# URL Validator
# -----------------------------------
def validate_url(url: str) -> bool:
    """
    Validates URL format
    """
    if not url:
        return False

    pattern = r"^(https?:\/\/)?([\w\-])+\.{1}([a-zA-Z]{2,63})([\/\w\.-]*)*\/?$"
    return re.match(pattern, url) is not None


# -----------------------------------
# Numeric Validator
# -----------------------------------
def validate_positive_number(value: Any) -> bool:
    """
    Validates positive numeric values
    """
    try:
        return float(value) >= 0
    except (ValueError, TypeError):
        return False


# -----------------------------------
# ID Validator
# -----------------------------------
def validate_id(value: Any) -> bool:
    """
    Validates database IDs
    """
    try:
        return int(value) > 0
    except (ValueError, TypeError):
        return False


# -----------------------------------
# Text Length Validator
# -----------------------------------
def validate_text_length(text: str, min_length: int = 0, max_length: int = 1000) -> bool:
    """
    Validates text field length
    """
    if not isinstance(text, str):
        return False

    return min_length <= len(text.strip()) <= max_length


# -----------------------------------
# Startup Stage Validator
# -----------------------------------
VALID_STARTUP_STAGES = [
    "Ideation",
    "Prototype",
    "MVP",
    "Early Revenue",
    "Growth",
    "Scaling"
]


def validate_startup_stage(stage: str) -> bool:
    """
    Validates startup stage
    """
    return stage in VALID_STARTUP_STAGES


# -----------------------------------
# Generic Required Field Validator
# -----------------------------------
def validate_required_fields(data: dict, required_fields: List[str]) -> List[str]:
    """
    Returns list of missing fields
    """
    missing = []

    for field in required_fields:
        if field not in data or data[field] is None:
            missing.append(field)

    return missing