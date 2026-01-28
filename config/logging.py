import os
import logging
from logging.handlers import RotatingFileHandler


def setup_logger():

    LOG_DIR = "logs"
    os.makedirs(LOG_DIR, exist_ok=True)

    LOG_FILE = os.path.join(LOG_DIR, "app.log")

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
    )

    file_handler = RotatingFileHandler(
        LOG_FILE,
        maxBytes=5 * 1024 * 1024,   # 5 MB
        backupCount=5
    )
    file_handler.setFormatter(formatter)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)

    # Prevent duplicate logs
    if not root_logger.handlers:
        root_logger.addHandler(file_handler)
        root_logger.addHandler(console_handler)

    logger = logging.getLogger("tmm-ai")

    return logger
