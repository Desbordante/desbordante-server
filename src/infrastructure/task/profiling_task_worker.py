from uuid import UUID

from src.domain.task.tasks import profile_task


class ProfilingTaskWorker:
    def set(self, *, task_id: UUID) -> None:
        profile_task.delay(task_id)
