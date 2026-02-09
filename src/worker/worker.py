from celery import Celery

from src.worker.config import settings

worker = Celery(
    __name__,
    broker=settings.rabbitmq_dsn.unicode_string(),
    include=[
        "src.domain.task.tasks",
    ],
)
worker.config_from_object("src.worker.celery_config")
