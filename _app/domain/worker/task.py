from io import BytesIO
from uuid import UUID

import pandas as pd
from celery.signals import task_failure, task_postrun, task_prerun
from sqlmodel import Session

from _app.db import engine
from _app.domain.file.dependencies import get_storage_client
from _app.domain.task.models import Task
from _app.domain.task.schemas.schemas import OneOfTaskConfig, OneOfTaskResult
from _app.domain.task.schemas.types import TaskStatus
from _app.domain.task.utils import match_task_by_primitive_name
from _app.domain.worker import worker
from _app.repository import BaseRepository


@worker.task(name="tasks.profiling", ignore_result=True, max_retries=0)
def data_profiling_task(
    task_id: UUID,
    paths: list[str],
    raw_config: OneOfTaskConfig,
) -> OneOfTaskResult:
    config = OneOfTaskConfig.model_validate(raw_config)
    storage = get_storage_client()

    tables = [pd.read_csv(BytesIO(storage.download_file(path))) for path in paths]

    # print('!!!', tables, raw_config)
    return match_task_by_primitive_name(raw_config["primitive_name"]).execute(
        tables=tables, task_config=raw_config
    )


@task_prerun.connect(sender=data_profiling_task)
def task_prerun_notifier(kwargs, **_):
    task_id: UUID = kwargs["task_id"]
    with Session(engine) as session:
        task_repository = BaseRepository(session=session, model=Task)
        task_repository.update_by_id(
            id=task_id,
            status=TaskStatus.RUNNING,
        )


# task_postrun is used instead of task_success because task_success signal
# does not provide kwargs parameter which is needed to access task_id
@task_postrun.connect(sender=data_profiling_task)
def task_postrun_notifier(retval: OneOfTaskResult | None, kwargs, **_):
    if not retval:
        return

    task_id: UUID = kwargs["task_id"]
    with Session(engine) as session:
        task_repository = BaseRepository(session=session, model=Task)

        task_repository.update_by_id(
            id=task_id,
            status=TaskStatus.COMPLETED,
            result=retval.model_dump(),
        )


@task_failure.connect(sender=data_profiling_task)
def task_failure_notifier(
    kwargs,
    exception: Exception,
    traceback,
    **_,
):
    task_id: UUID = kwargs["task_id"]
    with Session(engine) as session:
        task_repository = BaseRepository(session=session, model=Task)
        task_repository.update_by_id(
            id=task_id,
            status=TaskStatus.FAILED,
        )
