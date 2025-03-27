from io import BytesIO
from uuid import UUID

import pandas as pd
from celery.signals import task_failure, task_postrun, task_prerun
from sqlmodel import Session

from app.db import engine
from app.domain.storage import storage
from app.domain.task.models import Task
from app.domain.task.schemas.schemas import OneOfTaskConfig, OneOfTaskResult
from app.domain.task.schemas.types import TaskStatus
from app.domain.task.utils import match_task_by_primitive_name
from app.domain.worker import worker
from app.repository import BaseRepository


@worker.task(name="tasks.profiling", ignore_result=True, max_retries=0)
def data_profiling_task(
    task_id: UUID,
    paths: list[str],
    raw_config: dict,
) -> OneOfTaskResult:
    config = OneOfTaskConfig.model_validate(raw_config)

    tables = [pd.read_csv(BytesIO(storage.download_file(path))) for path in paths]

    return match_task_by_primitive_name(config.primitive_name).execute(
        tables=tables, task_config=config
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
def task_postrun_notifier(retval: dict | None, kwargs, **_):
    if not retval:
        return

    result = OneOfTaskResult.model_validate(retval)

    task_id: UUID = kwargs["task_id"]
    with Session(engine) as session:
        task_repository = BaseRepository(session=session, model=Task)

        task_repository.update_by_id(
            id=task_id,
            status=TaskStatus.COMPLETED,
            result=result.serializable_dict(),
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
