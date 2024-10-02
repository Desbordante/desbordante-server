from fastapi import Depends

from internal.uow import UnitOfWork
from internal.rest.http.di import get_unit_of_work, get_task_repo, get_dataset_repo
from internal.usecase.task import RetrieveTask, SetTask
from internal.usecase.task.retrieve_task import TaskRepo as RetrieveTaskRepo
from internal.usecase.task.set_task import (
    TaskRepo as SetTaskRepo,
    DatasetRepo as SetDatasetRepo,
)
from internal.worker.celery import ProfilingTaskWorker


def get_profiling_task_worker() -> ProfilingTaskWorker:
    return ProfilingTaskWorker()


def get_retrieve_task_use_case(
    unit_of_work: UnitOfWork = Depends(get_unit_of_work),
    task_repo: RetrieveTaskRepo = Depends(get_task_repo),
) -> RetrieveTask:
    return RetrieveTask(
        unit_of_work=unit_of_work,
        task_repo=task_repo,
    )


def get_set_task_use_case(
    unit_of_work: UnitOfWork = Depends(get_unit_of_work),
    task_repo: SetTaskRepo = Depends(get_task_repo),
    dataset_repo: SetDatasetRepo = Depends(get_dataset_repo),
    profiling_task_worker: ProfilingTaskWorker = Depends(get_profiling_task_worker),
) -> SetTask:
    return SetTask(
        unit_of_work=unit_of_work,
        task_repo=task_repo,
        dataset_repo=dataset_repo,
        profiling_task_worker=profiling_task_worker,
    )
