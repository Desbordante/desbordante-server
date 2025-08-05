import logging

from src.worker.worker import worker

logger = logging.getLogger(__name__)


@worker.task(name="tasks.cleanup_temporary_files")
def cleanup_temporary_files() -> None:
    logger.info("Test")
