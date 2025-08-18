from typing import Annotated

from fastapi import Depends

from src.api.dependencies import AuthorizedUserDep, DatasetCrudDep, TaskCrudDep
from src.schemas.task_schemas.base_schemas import TaskQueryParamsSchema
from src.usecases.task.create_task import CreateTaskUseCase
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

TaskQueryParamsDep = Annotated[
    TaskQueryParamsSchema,
    Depends(TaskQueryParamsSchema),
]
