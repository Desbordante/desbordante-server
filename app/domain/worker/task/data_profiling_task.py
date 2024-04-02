from typing import Any
from uuid import UUID

from app.db.session import no_pooling
from app.domain.file.dataset import DatasetORM
from app.domain.task import OneOfTaskConfig, OneOfTaskResult
from app.domain.task import match_task_by_primitive_name
from app.domain.task.task import TaskFailureReason, TaskORM, TaskStatus
from app.worker import worker
from app.domain.worker.task.resource_intensive_task import ResourceIntensiveTask
import pandas as pd
from celery.signals import task_failure, task_prerun, task_postrun
from celery.exceptions import SoftTimeLimitExceeded, TimeLimitExceeded, WorkerLostError


@worker.task(base=ResourceIntensiveTask, ignore_result=True, max_retries=0)
def data_profiling_task(
    task_id: UUID,
    dataset_id: UUID,
    config: OneOfTaskConfig,
) -> Any:
    with no_pooling():
        dataset_orm: DatasetORM = (
            DatasetORM.with_joined(DatasetORM.file)  # type: ignore
            .where(DatasetORM.id == dataset_id)
            .first()
        )

    df = pd.read_csv(
        dataset_orm.file.path_to_file,
        sep=dataset_orm.separator,
        header=dataset_orm.header,
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
    with no_pooling():
        task_orm = TaskORM.find_or_fail(db_task_id)
        task_orm.update(status=TaskStatus.RUNNING)  # type: ignore


@task_postrun.connect(sender=data_profiling_task)
def task_postrun_notifier(
    kwargs,
    retval: OneOfTaskResult,
    **_,
):
    db_task_id: UUID = kwargs["task_id"]
    with no_pooling():
        task_orm = TaskORM.find_or_fail(db_task_id)  # type: ignore
        task_orm.update(
            status=TaskStatus.COMPLETED,  # type: ignore
            result=retval.model_dump(),
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
    with no_pooling():
        task_orm = TaskORM.find_or_fail(db_task_id)  # type: ignore
        task_orm.update(
            status=TaskStatus.FAILED,  # type: ignore
            raised_exception_name=exception.__class__.__name__,  # type: ignore
            failure_reason=task_failure_reason,  # type: ignore
            traceback=traceback,
        )
