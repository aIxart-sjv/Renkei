from passlib.context import CryptContext
import secrets
import string


# =========================
# PASSWORD HASHING CONTEXT
# =========================

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)


# =========================
# HASH PASSWORD
# =========================

def hash_password(password: str) -> str:
    """
    Hash plain password securely

    Never store plain passwords in database
    """

    return pwd_context.hash(password)


# =========================
# VERIFY PASSWORD
# =========================

def verify_password(
    plain_password: str,
    hashed_password: str
) -> bool:
    """
    Verify plain password against hashed password
    """

    return pwd_context.verify(
        plain_password,
        hashed_password
    )


# =========================
# GENERATE SECURE TOKEN
# =========================

def generate_secure_token(
    length: int = 32
) -> str:
    """
    Generate cryptographically secure random token

    Used for:
    - password reset tokens
    - email verification
    """

    alphabet = string.ascii_letters + string.digits

    return "".join(
        secrets.choice(alphabet)
        for _ in range(length)
    )


# =========================
# GENERATE NUMERIC OTP
# =========================

def generate_otp(
    length: int = 6
) -> str:
    """
    Generate numeric OTP code

    Used for:
    - verification
    - 2FA
    """

    digits = string.digits

    return "".join(
        secrets.choice(digits)
        for _ in range(length)
    )


# =========================
# PASSWORD STRENGTH CHECK
# =========================

def validate_password_strength(
    password: str
) -> bool:
    """
    Basic password strength validation

    Requirements:
    - minimum 8 characters
    """

    if len(password) < 8:
        return False

    return True


# =========================
# CONSTANT TIME STRING COMPARE
# =========================

def constant_time_compare(
    val1: str,
    val2: str
) -> bool:
    """
    Prevent timing attacks
    """

    return secrets.compare_digest(val1, val2)