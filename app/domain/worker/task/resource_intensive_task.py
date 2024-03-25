from celery import Task
import resource
from app.settings import settings


class ResourceIntensiveTask(Task):
    # There are default Celery time limits, see: https://docs.celeryq.dev/en/stable/userguide/workers.html#time-limits
    time_limit = settings.worker_hard_time_limit_in_seconds
    soft_time_limit = settings.worker_soft_time_limit_in_seconds

    # There are custom memory limits using `resource` module
    hard_memory_limit = settings.worker_hard_memory_limit
    soft_memory_limit = settings.worker_soft_memory_limit

    def before_start(self, task_id, args, kwargs) -> None:
        resource.setrlimit(
            resource.RLIMIT_AS, (self.soft_memory_limit, self.hard_memory_limit)
        )
