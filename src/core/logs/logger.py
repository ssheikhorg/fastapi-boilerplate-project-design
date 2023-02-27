import logging
import sys
from logging.handlers import TimedRotatingFileHandler
from pathlib import Path
from typing import Any

FORMATTER = logging.Formatter("%(asctime)s - %(name)s - %(message)s - %(levelname)s")
LOG_DIR = Path(__file__).resolve().parent.parent.parent / "logs/tmp"
LOG_DIR.mkdir(exist_ok=True)


def get_console_handler() -> logging.StreamHandler:
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(FORMATTER)
    return console_handler


def get_file_handler(name: str) -> TimedRotatingFileHandler:
    file_handler = TimedRotatingFileHandler(LOG_DIR / f"{name}.log", when="midnight", backupCount=7)
    file_handler.setFormatter(FORMATTER)
    return file_handler


def get_logger(logger_name: str) -> Any:
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(get_console_handler())
    logger.addHandler(get_file_handler(logger_name))
    logger.propagate = False
    return logger
