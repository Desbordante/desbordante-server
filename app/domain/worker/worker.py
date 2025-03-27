from celery import Celery

from app.domain.worker.config import settings

worker = Celery(
    __name__,
    broker=settings.rabbitmq_dsn.unicode_string(),
    include=["app.domain.worker.task"],
)
