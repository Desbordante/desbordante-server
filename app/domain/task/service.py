from uuid import UUID

from app.domain.task.models import Task
from app.domain.task.schemas.schemas import TaskCreate
from app.domain.worker.task import data_profiling_task
from app.repository import BaseRepository


class TaskService:
    def __init__(self, repository: BaseRepository[Task]):
        self._repository = repository

    def create_task(self, config: TaskCreate) -> Task:
        task_model = Task(config=config.serializable_dict())

        task = self._repository.create(task_model)

        data_profiling_task.delay(task_id=task.id, config=config.serializable_dict())

        return task

    def get_by_id(self, id: UUID) -> Task:
        task = self._repository.get_by_id(id)
        return task
