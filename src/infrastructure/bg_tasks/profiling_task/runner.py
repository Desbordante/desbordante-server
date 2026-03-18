from uuid import UUID

from src.infrastructure.bg_tasks.profiling_task.task import profiling_task
from src.schemas.dataset_schemas import DatasetForTaskSchema
from src.schemas.task_schemas.base_schemas import OneOfTaskParams


class ProfilingTaskRunner:
    def run(
        self,
        *,
        params: OneOfTaskParams,
        datasets: list[DatasetForTaskSchema],
        task_id: UUID,
    ) -> None:
        profiling_task.apply_async(
            kwargs={
                "params": params,
                "datasets": datasets,
            },
            task_id=str(task_id),
        )
