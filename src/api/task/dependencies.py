from typing import Annotated

from fastapi import Depends

from src.api.dependencies import TaskCrudDep, UserSessionDep
from src.usecases.task.get_task import GetTaskUseCase


async def get_get_task_use_case(
    task_crud: TaskCrudDep,
    user: UserSessionDep,
) -> GetTaskUseCase:
    return GetTaskUseCase(task_crud=task_crud, user=user)


GetTaskUseCaseDep = Annotated[GetTaskUseCase, Depends(get_get_task_use_case)]
