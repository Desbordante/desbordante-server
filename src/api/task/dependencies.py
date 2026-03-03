from typing import Annotated

from fastapi import Depends

from src.api.dependencies import (
    DatasetCrudDep,
    DatasetPolicyDep,
    TaskCrudDep,
    TaskPolicyDep,
)
from src.infrastructure.task.profiling_task_worker import ProfilingTaskWorker
from src.usecases.task.create_task import CreateTaskUseCase
from src.usecases.task.get_task import GetTaskUseCase


async def get_get_task_use_case(
    task_crud: TaskCrudDep,
    task_policy: TaskPolicyDep,
) -> GetTaskUseCase:
    return GetTaskUseCase(task_crud=task_crud, task_policy=task_policy)


GetTaskUseCaseDep = Annotated[GetTaskUseCase, Depends(get_get_task_use_case)]


async def get_profiling_task_worker() -> ProfilingTaskWorker:
    return ProfilingTaskWorker()


ProfilingTaskWorkerDep = Annotated[
    ProfilingTaskWorker, Depends(get_profiling_task_worker)
]


async def get_create_task_use_case(
    task_crud: TaskCrudDep,
    dataset_crud: DatasetCrudDep,
    dataset_policy: DatasetPolicyDep,
    task_policy: TaskPolicyDep,
    profiling_task_worker: ProfilingTaskWorkerDep,
) -> CreateTaskUseCase:
    return CreateTaskUseCase(
        task_crud=task_crud,
        dataset_crud=dataset_crud,
        profiling_task_worker=profiling_task_worker,
        dataset_policy=dataset_policy,
        task_policy=task_policy,
    )


CreateTaskUseCaseDep = Annotated[CreateTaskUseCase, Depends(get_create_task_use_case)]
