from typing import Any
from uuid import UUID

from src.crud.task_crud import TaskCrud
from src.domain.dataset.storage import storage
from src.domain.task.primitives.utils import get_primitive_class_by_name
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

    params = primitive_class.validate_params(task.params)

    primitive = primitive_class(algo_name=params.config.algo_name)

    downloaded_datasets = [
        primitive_class.downloaded_dataset_class.model_validate(
            {
                "id": dataset.id,
                "data": storage.download_file_sync(path=dataset.path),
                "params": dataset.params,
                "info": dataset.info,
            }
        )
        for dataset in task.datasets
    ]

    primitive_datasets = primitive_class.datasets_config_class.model_validate(
        {
            key: next((d for d in downloaded_datasets if d.id == id))
            for key, id in params.datasets.model_dump().items()
        }
    )

    return primitive.execute(config=params.config, datasets=primitive_datasets)
