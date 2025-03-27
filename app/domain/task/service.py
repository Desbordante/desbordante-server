from typing import List
from uuid import UUID

from app.domain.file.models import File
from app.domain.task.models import Task
from app.domain.task.schemas.schemas import OneOfTaskConfig
from app.domain.worker.task import data_profiling_task
from app.repository import BaseRepository


class TaskService:
    def __init__(self, repository: BaseRepository[Task]):
        self._repository = repository

    def create_task(
        self,
        config: OneOfTaskConfig,
        files: list[File],
        initiator_id: int | None = None,
    ) -> Task:
        task_model = Task(
            config=config.serializable_dict(),
            initiator_id=initiator_id,
            files=files,
        )

        task = self._repository.create(task_model)

        data_profiling_task.delay(
            task_id=task.id,
            paths=[file.path for file in files],
            raw_config=config.serializable_dict(),
        )

        return task

    def get_by_id(self, id: UUID) -> Task:
        task = self._repository.get_by_id(id)
        return task

    def get_user_tasks(self, user_id: int) -> List[Task]:
        tasks = self._repository.get_many_by(field="initiator_id", value=user_id)
        return tasks
