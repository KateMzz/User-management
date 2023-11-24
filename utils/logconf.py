import logging

from settings import settings

logging.basicConfig(
    level=settings.LOGGING_LEVEL, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(settings.LOGGER_NAME)
