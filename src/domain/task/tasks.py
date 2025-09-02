from typing import Any
from uuid import UUID

from src.crud.task_crud import TaskCrud
from src.domain.task.primitives.utils import get_primitive_class_by_name
from src.domain.task.utils import download_dataset
from src.models.task_models import TaskModel, TaskResultModel
from src.schemas.base_schemas import TaskErrorSchema
from src.schemas.task_schemas.base_schemas import OneOfTaskResult
from src.worker.task import DatabaseTaskBase
from src.worker.worker import worker


class ProfileTaskTask(DatabaseTaskBase[TaskModel, UUID]):
    crud_class = TaskCrud

    def create_result_object(self, id: UUID, retval: OneOfTaskResult) -> Any:
        return TaskResultModel(
            task_id=id,
            result=retval,
        )

    def create_error_object(self, id: UUID, exc: Exception) -> Any:
        return TaskResultModel(
            task_id=id,
            result=TaskErrorSchema(error=str(exc)),
        )


@worker.task(name="tasks.profile_task", base=ProfileTaskTask, bind=True)
def profile_task(self: ProfileTaskTask, task_id: UUID) -> OneOfTaskResult:
    task = self.entity

    primitive_class = get_primitive_class_by_name(task.params.primitive_name)

    downloaded_datasets = {
        key: download_dataset(next((d for d in task.datasets if d.id == id)))
        for key, id in task.params.datasets.model_dump().items()
    }

    params = primitive_class.validate_params(
        {
            **task.params.model_dump(exclude={"datasets"}),
            "datasets": downloaded_datasets,
        }
    )

    primitive = primitive_class(algo_name=params.config.algo_name)

    return primitive.execute(params=params)
