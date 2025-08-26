from typing import Any
from uuid import UUID

from src.crud.task_crud import TaskCrud
from src.models.task_models import TaskModel, TaskResultModel
from src.schemas.base_schemas import TaskErrorSchema
from src.schemas.task_schemas.base_schemas import AfdTaskResult, OneOfTaskResult
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

    return AfdTaskResult(primitive_name=task.params.primitive_name)
