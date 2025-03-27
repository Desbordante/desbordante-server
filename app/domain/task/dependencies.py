from typing import Annotated

from fastapi import Depends

from app.dependencies.dependencies import SessionDep
from app.domain.task.models import Task
from app.domain.task.service import TaskService
from app.repository.repository import BaseRepository


def get_task_service(session: SessionDep) -> TaskService:
    return TaskService(repository=BaseRepository(model=Task, session=session))


TaskServiceDep = Annotated[TaskService, Depends(get_task_service)]
