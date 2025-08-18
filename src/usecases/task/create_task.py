import logging
from typing import Protocol
from uuid import UUID

from src.exceptions import BadRequestException
from src.models.dataset_models import DatasetModel
from src.models.task_models import TaskModel
from src.models.user_models import UserModel
from src.schemas.dataset_schemas import (
    DatasetType,
    TaskStatus,
)
from src.schemas.task_schemas.base_schemas import OneOfTaskParams

logger = logging.getLogger(__name__)


class TaskCrud(Protocol):
    async def create(self, entity: TaskModel) -> TaskModel: ...


class DatasetCrud(Protocol):
    async def get_by_ids(
        self, *, ids: list[UUID], owner_id: int, type: DatasetType, status: TaskStatus
    ) -> list[DatasetModel]: ...


class CreateTaskUseCase:
    def __init__(
        self,
        *,
        task_crud: TaskCrud,
        dataset_crud: DatasetCrud,
        user: UserModel,
    ):
        self.task_crud = task_crud
        self.dataset_crud = dataset_crud
        self.user = user

    async def __call__(self, *, params: OneOfTaskParams) -> TaskModel:
        dataset_ids = list(params.datasets.model_dump().values())

        datasets = await self.dataset_crud.get_by_ids(
            ids=dataset_ids,
            owner_id=self.user.id,
            type=DatasetType.Tabular,  # TODO: add other types
            status=TaskStatus.Success,
        )

        if len(datasets) != len(dataset_ids):
            raise BadRequestException(
                "Some datasets were not found or have invalid type"
            )

        task_entity = TaskModel(
            initiator_id=self.user.id,
            params=params,
            datasets=datasets,
        )

        return await self.task_crud.create(task_entity)
