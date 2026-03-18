from typing import Any
from uuid import UUID

from pydantic import TypeAdapter

from src.crud.task_crud import TaskCrud
from src.domain.task.utils import download_dataset, get_primitive_class_by_name
from src.infrastructure.task.resource_intensive_task import ResourceIntensiveTask
from src.models.task_models import TaskModel
from src.models.task_result_models import TaskResultModel
from src.schemas.base_schemas import TaskStatus
from src.schemas.dataset_schemas import DatasetForTaskSchema
from src.schemas.task_schemas.base_schemas import (
    OneOfTaskParams,
    OneOfTaskResultItemSchema,
    OneOfTaskResultSchema,
)
from src.schemas.task_schemas.primitives.base_schemas import PrimitiveResultSchema
from src.worker.config import settings
from src.worker.profiling_task_backend import ProfilingTaskBackend
from src.worker.task import DatabaseTaskBase
from src.worker.worker import worker


class ProfileTaskTask(DatabaseTaskBase[TaskModel, UUID]):
    crud_class = TaskCrud
    result_field = "results"
    error_field = "result"

    def on_success(
        self,
        retval: PrimitiveResultSchema[OneOfTaskResultSchema, OneOfTaskResultItemSchema],
        task_id: str,
        args: tuple[Any, ...],
        kwargs: dict[str, Any],
    ) -> None:
        id = args[0]

        self._update_object_sync(
            id,
            **{
                self.status_field: TaskStatus.SUCCESS,
                self.result_field: [
                    TaskResultModel(
                        task_id=id,
                        result=result,
                    )
                    for result in retval.items
                ],
                "result": retval.result,
            },
        )


@worker.task(
    name="tasks.profile_task",
    backend=ProfilingTaskBackend(app=worker, url=settings.database_url),
    base=ResourceIntensiveTask,
    pydantic=True,
    bind=True,
)
def profile_task(
    self, *, params: OneOfTaskParams, datasets: list[DatasetForTaskSchema]
) -> PrimitiveResultSchema[OneOfTaskResultSchema, OneOfTaskResultItemSchema]:
    params = TypeAdapter(OneOfTaskParams).validate_python(params)
    datasets = TypeAdapter(list[DatasetForTaskSchema]).validate_python(datasets)

    primitive_class = get_primitive_class_by_name(params.primitive_name)

    downloaded_datasets = {
        key: download_dataset(next((d for d in datasets if d.id == id)))
        for key, id in params.datasets.model_dump().items()
    }

    params = primitive_class.validate_params(
        {
            **params.model_dump(exclude={"datasets"}),
            "datasets": downloaded_datasets,
        }
    )

    primitive = primitive_class(algo_name=params.config.algo_name)

    return primitive.execute(params=params)
