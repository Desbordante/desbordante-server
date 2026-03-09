from typing import Annotated
from uuid import UUID

from fastapi import Depends, Request

from src.api.dependencies import (
    ActorDep,
    DatasetCrudDep,
    DatasetPolicyDep,
    SessionDep,
    TaskCrudDep,
    TaskPolicyDep,
)
from src.crud.task_result_crud.task_result_crud import TaskResultCrud
from src.infrastructure.task.profiling_task_worker import ProfilingTaskWorker
from src.models.task_models import TaskModel
from src.schemas.task_schemas.base_schemas import (
    OneOfTaskResultFiltersSchema,
    TaskQueryParamsSchema,
    TaskResultQueryParamsSchema,
)
from src.schemas.task_schemas.utils import get_filters_schema_by_primitive_name
from src.usecases.task.create_task import CreateTaskUseCase
from src.usecases.task.get_task import GetTaskUseCase
from src.usecases.task.get_task_results import GetTaskResultsUseCase


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
    )


CreateTaskUseCaseDep = Annotated[CreateTaskUseCase, Depends(get_create_task_use_case)]


async def get_task(
    get_task: GetTaskUseCaseDep, task_id: UUID, actor: ActorDep
) -> TaskModel:
    return await get_task(id=task_id, actor=actor)


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


def parse_task_result_filters(
    request: Request,
    task: TaskDep,
    filters: OneOfTaskResultFiltersSchema | None = None,
):
    if filters:
        return filters

    query_params = dict(request.query_params)

    return get_filters_schema_by_primitive_name(
        task.params.primitive_name
    ).model_validate(query_params)


TaskResultQueryParamsDep = Annotated[
    TaskResultQueryParamsSchema[
        Annotated[OneOfTaskResultFiltersSchema, Depends(parse_task_result_filters)]
    ],
    Depends(),
]
