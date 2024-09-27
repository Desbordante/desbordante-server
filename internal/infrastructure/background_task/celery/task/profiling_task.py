from typing import Any
from uuid import UUID

import traceback as tb

from celery.signals import task_failure, task_prerun, task_postrun
from celery.exceptions import SoftTimeLimitExceeded, TimeLimitExceeded, WorkerLostError

from internal.domain.task.value_objects import (
    OneOfTaskConfig,
    TaskStatus,
    OneOfTaskResult,
    TaskFailureReason,
)
from internal.infrastructure.background_task.celery import worker
from internal.infrastructure.background_task.celery.task.di import (
    get_profile_task_use_case,
    get_update_task_info_use_case,
)
from internal.infrastructure.background_task.celery.task.resource_intensive_task import (
    ResourceIntensiveTask,
)


@worker.task(base=ResourceIntensiveTask, ignore_result=True, max_retries=0)
def profiling_task(
    task_id: UUID,
    dataset_id: UUID,
    config: OneOfTaskConfig,
) -> Any:

    profile_task = get_profile_task_use_case()

    result = profile_task(dataset_id=dataset_id, config=config)
    return result


@task_prerun.connect(sender=profiling_task)
def task_prerun_notifier(
    kwargs,
    **_,
) -> None:

    update_task_info = get_update_task_info_use_case()
    db_task_id: UUID = kwargs["task_id"]

    update_task_info(task_id=db_task_id, task_status=TaskStatus.RUNNING)


@task_postrun.connect(sender=profiling_task)
def task_postrun_notifier(
    kwargs,
    retval: OneOfTaskResult,
    **_,
):

    update_task_info = get_update_task_info_use_case()
    db_task_id: UUID = kwargs["task_id"]

    update_task_info(
        task_id=db_task_id,
        task_status=TaskStatus.COMPLETED,
        result=retval,
    )


@task_failure.connect(sender=profiling_task)
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

    formatted_traceback = "".join(
        tb.format_exception(type(exception), exception, exception.__traceback__)
    )

    update_task_info = get_update_task_info_use_case()
    db_task_id: UUID = kwargs["task_id"]

    update_task_info(
        task_id=db_task_id,
        task_status=TaskStatus.FAILED,
        raised_exception_name=exception.__class__.__name__,
        failure_reason=task_failure_reason,
        traceback=formatted_traceback,
    )
