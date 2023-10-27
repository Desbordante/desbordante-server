from celery import Celery

from app.settings import get_settings

settings = get_settings()
taskq = Celery(
    __name__,
    broker=settings.rabbitmq_dsn.unicode_string(),
    include=["app.tasks"],
)
taskq.config_from_object("app.settings.celeryconfig")
