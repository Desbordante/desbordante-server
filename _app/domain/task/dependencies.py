from typing import Annotated

from fastapi import Depends

from _app.dependencies.dependencies import SessionDep
from _app.domain.task.models import Task
from _app.domain.task.service import TaskService
from _app.repository.repository import BaseRepository


def get_task_service(session: SessionDep) -> TaskService:
    return TaskService(repository=BaseRepository(model=Task, session=session))


TaskServiceDep = Annotated[TaskService, Depends(get_task_service)]
