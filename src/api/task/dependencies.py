from typing import Annotated

from fastapi import Depends

from src.api.dependencies import (
    AuthorizedUserDep,
    DatasetCrudDep,
    TaskCrudDep,
    TaskResultCrudDep,
)
from src.schemas.task_schemas.base_schemas import (
    TaskQueryParamsSchema,
    TaskResultQueryParamsSchema,
)
from src.usecases.task.create_task import CreateTaskUseCase
from src.usecases.task.get_task import GetTaskUseCase
from src.usecases.task.get_task_results import GetTaskResultsUseCase
from src.usecases.task.get_tasks import GetTasksUseCase


async def get_create_task_use_case(
    task_crud: TaskCrudDep,
    dataset_crud: DatasetCrudDep,
    user: AuthorizedUserDep,
) -> CreateTaskUseCase:
    return CreateTaskUseCase(task_crud=task_crud, dataset_crud=dataset_crud, user=user)


CreateTaskUseCaseDep = Annotated[CreateTaskUseCase, Depends(get_create_task_use_case)]


async def get_get_tasks_use_case(
    task_crud: TaskCrudDep,
    user: AuthorizedUserDep,
) -> GetTasksUseCase:
    return GetTasksUseCase(task_crud=task_crud, user=user)


GetTasksUseCaseDep = Annotated[GetTasksUseCase, Depends(get_get_tasks_use_case)]


async def get_get_task_use_case(
    task_crud: TaskCrudDep,
    user: AuthorizedUserDep,
) -> GetTaskUseCase:
    return GetTaskUseCase(task_crud=task_crud, user=user)


GetTaskUseCaseDep = Annotated[GetTaskUseCase, Depends(get_get_task_use_case)]


async def get_get_task_results_use_case(
    task_result_crud: TaskResultCrudDep,
    user: AuthorizedUserDep,
) -> GetTaskResultsUseCase:
    return GetTaskResultsUseCase(task_result_crud=task_result_crud, user=user)


GetTaskResultsUseCaseDep = Annotated[
    GetTaskResultsUseCase, Depends(get_get_task_results_use_case)
]

TaskQueryParamsDep = Annotated[
    TaskQueryParamsSchema,
    Depends(TaskQueryParamsSchema),
]

TaskResultQueryParamsDep = Annotated[
    TaskResultQueryParamsSchema,
    Depends(TaskResultQueryParamsSchema),
]
