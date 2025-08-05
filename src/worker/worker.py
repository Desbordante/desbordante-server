from celery import Celery

from src.worker.config import settings

worker = Celery(
    __name__,
    broker=settings.rabbitmq_dsn.unicode_string(),
    include=[
        "src.domain.account.tasks",
        "src.domain.auth.tasks",
        "src.domain.file.tasks",
    ],
    beat_schedule={
        "cleanup-temporary-files": {
            "task": "tasks.cleanup_temporary_files",
            "schedule": settings.CLEANUP_TEMPORARY_FILES_SECONDS_INTERVAL,
        }
    },
)
