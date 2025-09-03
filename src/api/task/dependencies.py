from typing import Annotated
from uuid import UUID

from fastapi import Depends

from src.api.dependencies import (
    AuthorizedUserDep,
    DatasetCrudDep,
    SessionDep,
    TaskCrudDep,
)
from src.crud.task_result_crud.task_result_crud import TaskResultCrud
from src.models.task_models import TaskModel
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


async def get_task(get_task: GetTaskUseCaseDep, id: UUID) -> TaskModel:
    return await get_task(id=id)


TaskDep = Annotated[TaskModel, Depends(get_task)]


async def get_task_result_crud(
    session: SessionDep,
    task: TaskDep,
) -> TaskResultCrud:
    return TaskResultCrud(session=session, primitive_name=task.params.primitive_name)


TaskResultCrudDep = Annotated[TaskResultCrud, Depends(get_task_result_crud)]


async def get_get_task_results_use_case(
    task_result_crud: TaskResultCrudDep,
) -> GetTaskResultsUseCase:
    return GetTaskResultsUseCase(task_result_crud=task_result_crud)


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
