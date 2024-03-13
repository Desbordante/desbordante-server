from celery import Celery

from app.settings import settings

worker = Celery(
    __name__,
    broker=settings.rabbitmq_dsn.unicode_string(),
    include=["app.domain.worker.task"],
)
worker.config_from_object("app.settings.celery_config")
