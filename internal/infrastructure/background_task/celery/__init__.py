from celery import Celery

from internal.infrastructure.data_storage import settings

worker = Celery(
    __name__,
    broker=settings.rabbitmq_dsn.unicode_string(),
    include=["internal.infrastructure.background_task.celery.task"],
)

worker.config_from_object("internal.infrastructure.background_task.celery.config")
