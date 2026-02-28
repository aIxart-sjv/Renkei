import logging
import sys
from logging.handlers import RotatingFileHandler
from pathlib import Path


# =========================
# LOG DIRECTORY SETUP
# =========================

LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)

LOG_FILE = LOG_DIR / "renkei.log"


# =========================
# LOG FORMAT
# =========================

LOG_FORMAT = (
    "%(asctime)s | "
    "%(levelname)s | "
    "%(name)s | "
    "%(message)s"
)

DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


# =========================
# CREATE FORMATTER
# =========================

formatter = logging.Formatter(
    fmt=LOG_FORMAT,
    datefmt=DATE_FORMAT
)


# =========================
# CONSOLE HANDLER
# =========================

console_handler = logging.StreamHandler(sys.stdout)
console_handler.setFormatter(formatter)
console_handler.setLevel(logging.INFO)


# =========================
# FILE HANDLER (ROTATING)
# =========================

file_handler = RotatingFileHandler(
    LOG_FILE,
    maxBytes=10 * 1024 * 1024,  # 10 MB
    backupCount=5
)

file_handler.setFormatter(formatter)
file_handler.setLevel(logging.INFO)


# =========================
# ROOT LOGGER SETUP
# =========================

logging.basicConfig(
    level=logging.INFO,
    handlers=[
        console_handler,
        file_handler
    ]
)


# =========================
# GET LOGGER FUNCTION
# =========================

def get_logger(name: str) -> logging.Logger:
    """
    Get named logger for module

    Example:
        logger = get_logger(__name__)
        logger.info("Message")
    """

    logger = logging.getLogger(name)

    return logger


# =========================
# DEFAULT APP LOGGER
# =========================

logger = get_logger("renkei")


# =========================
# HELPER LOG FUNCTIONS
# =========================

def log_info(message: str):
    logger.info(message)


def log_warning(message: str):
    logger.warning(message)


def log_error(message: str):
    logger.error(message)


def log_debug(message: str):
    logger.debug(message)