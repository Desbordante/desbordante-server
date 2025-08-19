from celery import Celery

from src.worker.config import settings

worker = Celery(
    __name__,
    broker=settings.rabbitmq_dsn.unicode_string(),
    include=[
        "src.domain.account.tasks",
        "src.domain.auth.tasks",
        "src.domain.dataset.tasks",
        "src.domain.task.tasks",
    ],
)
