from celery import Celery

taskq = Celery(
    __name__,
    broker="amqp://guest:guest@localhost:5672",
    include=["app.tasks"],
)
