import os
import logging
from logging.handlers import RotatingFileHandler


def setup_logger(name="tmm-ai"):

    # Configurable via env
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()
    LOG_DIR = os.getenv("LOG_DIR", "logs")


    os.makedirs(LOG_DIR, exist_ok=True)

    LOG_FILE = os.path.join(LOG_DIR, "app.log")


    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
    )


    # File Handler
    file_handler = RotatingFileHandler(
        LOG_FILE,
        maxBytes=5 * 1024 * 1024,   # 5MB
        backupCount=5,
        encoding="utf-8"
    )
    file_handler.setFormatter(formatter)


    # Console Handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)


    logger = logging.getLogger(name)
    logger.setLevel(LOG_LEVEL)


    # Prevent duplicate handlers (uvicorn reload safe)
    if not logger.handlers:

        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

        # Prevent double logging to root
        logger.propagate = False


    return logger
