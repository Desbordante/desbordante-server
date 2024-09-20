from internal.dto.worker.task import ProfilingTaskCreateSchema
from internal.infrastructure.background_task.celery.task import profiling_task


class ProfilingTaskWorker:

    def set(self, task_info: ProfilingTaskCreateSchema) -> None:

        profiling_task.delay(
            task_id=task_info.task_id,
            dataset_id=task_info.dataset_id,
            config=task_info.config,
        )
