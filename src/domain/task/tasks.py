import asyncio
from io import BytesIO
from typing import Any
from uuid import UUID

import pandas as pd
from celery.exceptions import SoftTimeLimitExceeded, TimeLimitExceeded, WorkerLostError
from celery.signals import task_failure, task_postrun, task_prerun

from src.crud.dataset_crud import DatasetCrud
from src.crud.task_crud import TaskCrud
from src.db.session import scoped_session
from src.domain.task.resource_intensive_task import ResourceIntensiveTask
from src.domain.task.utils import match_task_by_primitive_name
from src.infrastructure.storage.client import create_s3_storage
from src.models.dataset_models import DatasetModel
from src.models.task_models import TaskModel
from src.schemas.base_schemas import TaskStatus
from src.schemas.dataset_schemas import TabularDatasetParams
from src.schemas.task_schemas.base_schemas import (
    OneOfTaskConfig,
    OneOfTaskResult,
    TaskFailureReason,
)
from src.worker import worker


def update_object_sync(id: UUID, **kwargs: Any) -> TaskModel:
    loop = asyncio.get_event_loop()
    return loop.run_until_complete(update_object_async(id, **kwargs))


async def update_object_async(id: UUID, **kwargs: Any) -> TaskModel:
    async with scoped_session() as session:
        crud = TaskCrud(session=session)
        entity = await crud.get_by(id=id)
        return await crud.update(entity=entity, **kwargs)
    raise RuntimeError("Failed to get database session")


def get_dataset_by_id(dataset_id: UUID) -> DatasetModel:
    async def _get_dataset_by_id(dataset_id: UUID) -> DatasetModel:
        async with scoped_session() as session:
            crud = DatasetCrud(session=session)
            return await crud.get_by(id=dataset_id)

    loop = asyncio.get_event_loop()
    return loop.run_until_complete(_get_dataset_by_id(dataset_id))


@worker.task(base=ResourceIntensiveTask, ignore_result=True, max_retries=0)
def data_profiling_task(
    task_id: UUID,
    dataset_id: UUID,
    config: OneOfTaskConfig,
) -> Any:
    dataset = get_dataset_by_id(dataset_id)
    task = update_object_sync(id=task_id)

    dataset = task.dataset

    storage = create_s3_storage()
    data = storage.download_sync(path=dataset.path)

    params = TabularDatasetParams.model_validate(dataset.params)

    df = pd.read_csv(
        BytesIO(data),
        sep=params.separator,
        header=0 if params.has_header else None,
    )

    task = match_task_by_primitive_name(config.primitive_name)
    result = task.execute(df, config)  # type: ignore
    return result


@task_prerun.connect(sender=data_profiling_task)
def task_prerun_notifier(
    kwargs,
    **_,
):
    db_task_id: UUID = kwargs["task_id"]
    update_object_sync(id=db_task_id, status=TaskStatus.PROCESSING)


@task_postrun.connect(sender=data_profiling_task)
def task_postrun_notifier(
    kwargs,
    retval: OneOfTaskResult,
    **_,
):
    db_task_id: UUID = kwargs["task_id"]
    update_object_sync(
        id=db_task_id, status=TaskStatus.SUCCESS, result=retval.model_dump()
    )


@task_failure.connect(sender=data_profiling_task)
def task_failure_notifier(
    kwargs,
    exception: Exception,
    traceback,
    **_,
):
    # TODO: test all possible exceptions
    task_failure_reason = TaskFailureReason.OTHER
    if isinstance(exception, (TimeLimitExceeded, SoftTimeLimitExceeded)):
        task_failure_reason = TaskFailureReason.TIME_LIMIT_EXCEEDED
    if isinstance(exception, MemoryError):
        task_failure_reason = TaskFailureReason.MEMORY_LIMIT_EXCEEDED
    if isinstance(exception, WorkerLostError):
        task_failure_reason = TaskFailureReason.WORKER_KILLED_BY_SIGNAL

    db_task_id: UUID = kwargs["task_id"]
    update_object_sync(
        id=db_task_id,
        status=TaskStatus.FAILED,
        raised_exception_name=exception.__class__.__name__,
        failure_reason=task_failure_reason,
        traceback=traceback,
    )
