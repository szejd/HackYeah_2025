import logging

from app.config import APP_LOG_LEVEL


def setup_logging() -> None:
    """
    Set up logging configuration for the application.
    """
    logging.basicConfig(
        level=APP_LOG_LEVEL,
        format="%(asctime)s | %(name)s | %(levelname)s | %(message)s",
    )
