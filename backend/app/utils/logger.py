import logging
import sys
from logging.handlers import RotatingFileHandler
from pathlib import Path


# -----------------------------------
# Create logs directory if not exists
# -----------------------------------
LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)

LOG_FILE = LOG_DIR / "renkei.log"


# -----------------------------------
# Log format
# -----------------------------------
LOG_FORMAT = "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


# -----------------------------------
# Configure logger
# -----------------------------------
def setup_logger(name: str = "renkei") -> logging.Logger:
    """
    Creates and returns a configured logger instance.
    """

    logger = logging.getLogger(name)

    # Prevent duplicate handlers
    if logger.hasHandlers():
        return logger

    logger.setLevel(logging.INFO)

    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_formatter = logging.Formatter(LOG_FORMAT, datefmt=DATE_FORMAT)
    console_handler.setFormatter(console_formatter)

    # File handler with rotation
    file_handler = RotatingFileHandler(
        LOG_FILE,
        maxBytes=5 * 1024 * 1024,  # 5 MB
        backupCount=5
    )
    file_handler.setLevel(logging.INFO)
    file_formatter = logging.Formatter(LOG_FORMAT, datefmt=DATE_FORMAT)
    file_handler.setFormatter(file_formatter)

    # Add handlers
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger


# -----------------------------------
# Default logger instance
# -----------------------------------
logger = setup_logger()


# -----------------------------------
# Helper logging functions
# -----------------------------------
def log_info(message: str):
    logger.info(message)


def log_warning(message: str):
    logger.warning(message)


def log_error(message: str):
    logger.error(message)


def log_debug(message: str):
    logger.debug(message)