from typing import Any, Sequence
from uuid import UUID

from src.crud.task_crud import TaskCrud
from src.domain.task.utils import download_dataset, get_primitive_class_by_name
from src.models.task_models import TaskModel
from src.models.task_result_models import TaskResultModel
from src.schemas.task_schemas.base_schemas import OneOfTaskResult
from src.worker.task import DatabaseTaskBase
from src.worker.worker import worker


class ProfileTaskTask(DatabaseTaskBase[TaskModel, UUID]):
    crud_class = TaskCrud
    result_field = "results"
    error_field = "info"

    def create_result_object(self, id: UUID, retval: Sequence[OneOfTaskResult]) -> Any:
        return [
            TaskResultModel(
                task_id=id,
                result=result,
            )
            for result in retval
        ]


@worker.task(name="tasks.profile_task", base=ProfileTaskTask, bind=True)
def profile_task(self: ProfileTaskTask, task_id: UUID) -> Sequence[OneOfTaskResult]:
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
