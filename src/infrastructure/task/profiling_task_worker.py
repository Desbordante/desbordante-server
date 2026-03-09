from uuid import UUID

from src.infrastructure.task.profiling_task import profiling_task
from src.schemas.task_schemas.base_schemas import OneOfTaskParams


class ProfilingTaskWorker:
    def set(self, *, task_id: UUID, dataset_id: UUID, config: OneOfTaskParams) -> None:
        profiling_task.delay(
            task_id=task_id,
            dataset_id=dataset_id,
            config=config,
        )
