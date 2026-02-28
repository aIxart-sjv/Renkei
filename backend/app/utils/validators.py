import re
from typing import Optional, List


# =========================
# EMAIL VALIDATOR
# =========================

EMAIL_REGEX = re.compile(
    r"^[\w\.-]+@[\w\.-]+\.\w+$"
)


def validate_email(email: str) -> bool:
    """
    Validate email format
    """

    if not email:
        return False

    return bool(
        EMAIL_REGEX.match(email)
    )


# =========================
# USERNAME VALIDATOR
# =========================

USERNAME_REGEX = re.compile(
    r"^[a-zA-Z0-9_\-]{3,100}$"
)


def validate_username(username: str) -> bool:
    """
    Validate username format
    """

    if not username:
        return False

    return bool(
        USERNAME_REGEX.match(username)
    )


# =========================
# PASSWORD VALIDATOR
# =========================

def validate_password(password: str) -> bool:
    """
    Basic password validation
    """

    if not password:
        return False

    if len(password) < 6:
        return False

    return True


# =========================
# ENTITY TYPE VALIDATOR
# =========================

VALID_ENTITY_TYPES = {
    "student",
    "mentor",
    "alumni",
    "startup"
}


def validate_entity_type(entity_type: str) -> bool:

    return entity_type in VALID_ENTITY_TYPES


# =========================
# CONNECTION TYPE VALIDATOR
# =========================

VALID_CONNECTION_TYPES = {
    "mentorship",
    "collaboration",
    "startup_member",
    "startup_founder",
    "advisor"
}


def validate_connection_type(
    connection_type: str
) -> bool:

    return connection_type in VALID_CONNECTION_TYPES


# =========================
# SCORE VALIDATOR
# =========================

def validate_score(
    score: Optional[float],
    min_value: float = 0.0,
    max_value: float = 100.0
) -> bool:
    """
    Validate score range
    """

    if score is None:
        return False

    return min_value <= score <= max_value


# =========================
# VECTOR VALIDATOR
# =========================

def validate_vector(
    vector: Optional[List[float]],
    expected_dim: Optional[int] = None
) -> bool:
    """
    Validate ML embedding vector
    """

    if not vector:
        return False

    if not isinstance(vector, list):
        return False

    if expected_dim and len(vector) != expected_dim:
        return False

    return all(
        isinstance(x, (float, int))
        for x in vector
    )


# =========================
# TEXT VALIDATOR
# =========================

def validate_text(
    text: Optional[str],
    min_length: int = 0,
    max_length: int = 5000
) -> bool:
    """
    Validate text field
    """

    if text is None:
        return False

    length = len(text)

    return min_length <= length <= max_length


# =========================
# URL VALIDATOR
# =========================

URL_REGEX = re.compile(
    r"^(https?:\/\/)?"
    r"([\w\-])+\.{1}"
    r"([a-zA-Z]{2,63})"
    r"([\w\-\._~:/?#[\]@!$&'()*+,;=]*)$"
)


def validate_url(
    url: Optional[str]
) -> bool:

    if not url:
        return True

    return bool(
        URL_REGEX.match(url)
    )


# =========================
# SKILLS VALIDATOR
# =========================

def validate_skills(
    skills: Optional[str]
) -> bool:
    """
    Validate skills text
    """

    if not skills:
        return False

    if len(skills) > 2000:
        return False

    return True


# =========================
# LIST VALIDATOR
# =========================

def validate_non_empty_list(
    items: Optional[List]
) -> bool:

    return isinstance(items, list) and len(items) > 0


# =========================
# POSITIVE INTEGER VALIDATOR
# =========================

def validate_positive_int(
    value: Optional[int]
) -> bool:

    return isinstance(value, int) and value >= 0


# =========================
# SAFE ENTITY ID VALIDATOR
# =========================

def validate_entity_id(
    entity_id: Optional[int]
) -> bool:

    return validate_positive_int(entity_id)