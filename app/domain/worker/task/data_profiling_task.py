import logging
from typing import Any

from app.db.session import no_pooling
from app.domain.file.dataset import DatasetORM
from app.domain.task import OneOfTaskConfig
from app.domain.task import match_task_by_primitive_name
from app.worker import worker
from app.domain.worker.task.resource_intensive_task import ResourceIntensiveTask
from pydantic import UUID4
import pandas as pd
from celery.signals import task_failure, task_prerun, task_postrun


@worker.task(base=ResourceIntensiveTask, ignore_result=True, max_retries=0)
def data_profiling_task(
    dataset_id: UUID4,
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
    sender,
    task_id,
    task,
    args,
    kwargs,
    **_,
):
    # TODO: Create Task in database and set status to "running" or similar
    with no_pooling():
        ...
    logging.critical(
        f"From task_prerun_notifier ==> Running just before add() executes, {sender}"
    )


@task_postrun.connect(sender=data_profiling_task)
def task_postrun_notifier(
    sender,
    task_id,
    task,
    args,
    kwargs,
    retval,
    **_,
):
    with no_pooling():
        ...

    # TODO: Update Task in database and set status to "completed" or similar
    logging.critical(f"From task_postrun_notifier ==> Ok, done!, {sender}")


@task_failure.connect(sender=data_profiling_task)
def task_failure_notifier(
    sender,
    task_id,
    exception,
    args,
    kwargs,
    traceback,
    einfo,
    **_,
):
    with no_pooling():
        ...
    # TODO: Update Task in database and set status to "failed" or similar

    logging.critical(
        f"From task_failure_notifier ==> Task failed successfully! 😅, {sender}"
    )
