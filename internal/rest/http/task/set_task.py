from uuid import UUID

from fastapi import APIRouter, Depends

from internal.domain.task.value_objects import OneOfTaskConfig
from internal.rest.http.task.di import get_set_task_use_case
from internal.usecase.task import SetTask

router = APIRouter()

@router.post("/set")
def set_task(
    dataset_id: UUID,
    config: OneOfTaskConfig,

    set_task_use_case: SetTask = Depends(get_set_task_use_case)
) -> UUID:

    task_id = set_task_use_case(
        dataset_id=dataset_id,
        config=config,
    )

    return task_id
