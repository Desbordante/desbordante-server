from celery import Celery

from app.settings import settings

taskq = Celery(
    __name__,
    broker=settings.rabbitmq_dsn.unicode_string(),
    include=["app.background_tasks"],
)
taskq.config_from_object("app.settings.celery_config")
