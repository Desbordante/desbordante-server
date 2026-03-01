from uuid import UUID

from src.domain.task.value_objects import OneOfTaskConfig
from src.infrastructure.task.profiling_task import profiling_task


class ProfilingTaskWorker:
    def set(self, *, task_id: UUID, dataset_id: UUID, config: OneOfTaskConfig) -> None:
        profiling_task.delay(
            task_id=task_id,
            dataset_id=dataset_id,
            config=config,
        )
