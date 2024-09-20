from uuid import UUID

from fastapi import APIRouter, Depends
from pydantic import BaseModel

from internal.domain.task.value_objects import TaskStatus, OneOfTaskConfig, OneOfTaskResult, TaskFailureReason
from internal.rest.http.task.di import get_retrieve_task_use_case
from internal.usecase.task import RetrieveTask

router = APIRouter()


class ResponseSchema(BaseModel):
    status: TaskStatus
    config: OneOfTaskConfig
    dataset_id: UUID
    result: OneOfTaskResult | None
    raised_exception_name: str | None
    failure_reason: TaskFailureReason | None
    traceback: str | None


@router.get("/{task_id}")
def retrieve_task(
        task_id: UUID,
        retrieve_task_use_case: RetrieveTask = Depends(get_retrieve_task_use_case)
) -> ResponseSchema:

    task = retrieve_task_use_case(task_id=task_id)

    return ResponseSchema(
        status=task.status,
        dataset_id=task.dataset_id,
        config=task.config,
        result=task.result,
        raised_exception_name=task.raised_exception_name,
        failure_reason=task.failure_reason,
        traceback=task.traceback,
    )
