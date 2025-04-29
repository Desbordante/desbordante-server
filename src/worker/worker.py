from celery import Celery

from src.worker.config import settings

worker = Celery(__name__, broker=settings.rabbitmq_dsn.unicode_string())

worker.autodiscover_tasks(packages=["src.domain.account"])
