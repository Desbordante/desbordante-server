from uuid import UUID
from fastapi import APIRouter, HTTPException
from app.domain.file.dataset import DatasetORM
from app.domain.task.task import TaskModel, TaskORM, TaskStatus
from app.domain.worker.task.data_profiling_task import data_profiling_task
from app.domain.task import OneOfTaskConfig
from sqlalchemy_mixins.activerecord import ModelNotFoundError

router = APIRouter(prefix="/task")


@router.post("")
def set_task(
    dataset_id: UUID,
    config: OneOfTaskConfig,
) -> UUID:
    try:
        DatasetORM.find_or_fail(dataset_id)
    except ModelNotFoundError:
        raise HTTPException(404, "Dataset not found")

    task_orm = TaskORM.create(
        status=TaskStatus.CREATED,
        config=config.model_dump(),
        dataset_id=dataset_id,
    )
    task_id = task_orm.id  # type: ignore

    data_profiling_task.delay(
        task_id=task_id,
        dataset_id=dataset_id,
        config=config,
    )

    return task_id


@router.get("/{task_id}")
def retrieve_task(task_id: UUID) -> TaskModel:
    try:
        task_orm = TaskORM.find_or_fail(task_id)
        return TaskModel.model_validate(task_orm)
    except ModelNotFoundError:
        raise HTTPException(404, "Task not found")
