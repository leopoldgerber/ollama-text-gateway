import logging
import os
from logging.handlers import RotatingFileHandler

from dotenv import load_dotenv


load_dotenv()


def build_log_path() -> str:
    """Build log file path.
    Args:
        None: No arguments."""
    log_dir = os.getenv('LOG_DIR', 'logs')
    log_file_name = os.getenv('LOG_FILE_NAME', 'app.log')

    os.makedirs(log_dir, exist_ok=True)

    log_path = os.path.join(log_dir, log_file_name)
    return log_path


def get_log_level() -> int:
    """Get logger level.
    Args:
        None: No arguments."""
    log_level_name = os.getenv('LOG_LEVEL', 'INFO').upper()
    log_level = getattr(logging, log_level_name, logging.INFO)
    return log_level


def get_logger(logger_name: str) -> logging.Logger:
    """Create project logger.
    Args:
        logger_name (str): Logger name."""
    logger = logging.getLogger(logger_name)

    if logger.handlers:
        return logger

    log_level = get_log_level()
    log_path = build_log_path()

    formatter = logging.Formatter(
        '%(asctime)s | %(levelname)s | %(name)s | %(message)s'
    )

    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(log_level)
    stream_handler.setFormatter(formatter)

    file_handler = RotatingFileHandler(
        filename=log_path,
        maxBytes=1_048_576,
        backupCount=5,
        encoding='utf-8',
    )
    file_handler.setLevel(log_level)
    file_handler.setFormatter(formatter)

    logger.setLevel(log_level)
    logger.addHandler(stream_handler)
    logger.addHandler(file_handler)
    logger.propagate = False

    return logger
