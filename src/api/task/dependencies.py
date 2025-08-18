from typing import Annotated

from fastapi import Depends

from src.api.dependencies import AuthorizedUserDep, DatasetCrudDep, TaskCrudDep
from src.usecases.task.create_task import CreateTaskUseCase


async def get_create_task_use_case(
    task_crud: TaskCrudDep,
    dataset_crud: DatasetCrudDep,
    user: AuthorizedUserDep,
) -> CreateTaskUseCase:
    return CreateTaskUseCase(task_crud=task_crud, dataset_crud=dataset_crud, user=user)


CreateTaskUseCaseDep = Annotated[CreateTaskUseCase, Depends(get_create_task_use_case)]
