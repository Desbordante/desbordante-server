from uuid import UUID

from src.domain.task.tasks import profile_task
from src.schemas.dataset_schemas import DatasetForTaskSchema
from src.schemas.task_schemas.base_schemas import OneOfTaskParams


class ProfilingTaskWorker:
    def run(
        self,
        *,
        params: OneOfTaskParams,
        datasets: list[DatasetForTaskSchema],
        task_id: UUID,
    ) -> None:
        profile_task.apply_async(
            kwargs={
                "params": params,
                "datasets": datasets,
            },
            task_id=str(task_id),
        )
