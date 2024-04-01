from uuid import UUID
from fastapi import APIRouter, HTTPException
from pydantic import UUID4
from app.domain.file.dataset import DatasetORM
from app.domain.worker.task.data_profiling_task import data_profiling_task
from app.domain.task import OneOfTaskConfig
from sqlalchemy_mixins.activerecord import ModelNotFoundError

router = APIRouter(prefix="/task")


@router.post("")
def set_task(
    dataset_id: UUID4,
    config: OneOfTaskConfig,
) -> UUID4:
    try:
        DatasetORM.find_or_fail(dataset_id)
    except ModelNotFoundError:
        raise HTTPException(404, "Dataset not found")

    async_result = data_profiling_task.delay(dataset_id, config)
    return UUID(async_result.id, version=4)


@router.get("/{task_id}")
def retrieve_task(task_id: UUID4) -> None:
    raise HTTPException(418, "Not implemented yet")
