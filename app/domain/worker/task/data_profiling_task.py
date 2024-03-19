import logging

from app.db.session import get_session
from app.worker import worker
from app.domain.task.abstract_task import AnyConf, AnyRes
from app.domain.task.primitive_factory import PrimitiveName, PrimitiveFactory
from app.domain.task.task_factory import AnyAlgoName
from app.domain.worker.task.resource_intensive_task import ResourceIntensiveTask
from pydantic import UUID4
import pandas as pd
from celery.signals import task_failure, task_prerun, task_postrun


@worker.task(base=ResourceIntensiveTask, ignore_result=True, max_retries=0)
def data_profiling_task(
    primitive_name: PrimitiveName,
    algo_name: AnyAlgoName,
    file_id: UUID4,
    config: AnyConf,
) -> AnyRes:
    task_factory = PrimitiveFactory.get_by_name(primitive_name)
    task_cls = task_factory.get_by_name(algo_name)

    df = pd.read_csv(
        "tests/datasets/university_fd.csv", sep=",", header=0
    )  # TODO: Replace with actual file (by file_id) in future

    task = task_cls(df)
    result = task.execute(config)
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
    with get_session(with_pool=False) as session:
        session

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
    with get_session(with_pool=False) as session:
        session

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
    with get_session(with_pool=False) as session:
        session
    # TODO: Update Task in database and set status to "failed" or similar

    logging.critical(
        f"From task_failure_notifier ==> Task failed successfully! 😅, {sender}"
    )
