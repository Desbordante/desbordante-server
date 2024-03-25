from uuid import UUID
from fastapi import APIRouter, HTTPException
from pydantic import UUID4
from app.domain.worker.task.data_profiling_task import data_profiling_task
from app.domain.task import OneOfTaskConfig

router = APIRouter(prefix="/task")


@router.post("")
def set_task(
    file_id: UUID4,
    config: OneOfTaskConfig,
) -> UUID4:
    async_result = data_profiling_task.delay(file_id, config)
    return UUID(async_result.id, version=4)


@router.get("/{task_id}")
def retrieve_task(task_id: UUID4) -> None:
    raise HTTPException(418, "Not implemented yet")
