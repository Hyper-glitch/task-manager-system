import logging
from typing import Any

from src.config import settings

logger = logging.getLogger(settings.project)


def send_email_notification(*args: Any, **kwargs: Any) -> None:
    logger.info("Mocked sending email notification")
