from typing import TypedDict, Unpack
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from src.crud.base_crud import BaseCrud
from src.models.task_models import TaskModel


class TaskFindProps(TypedDict, total=False):
    id: UUID
    initiator_id: int


class TaskUpdateProps(TypedDict, total=False):
    pass


class TaskCrud(BaseCrud[TaskModel, UUID]):
    model = TaskModel

    def __init__(self, session: AsyncSession):
        super().__init__(session=session)

    async def get_by(self, **kwargs: Unpack[TaskFindProps]) -> TaskModel:
        return await super().get_by(**kwargs)

    async def update(
        self, *, entity: TaskModel, **kwargs: Unpack[TaskUpdateProps]
    ) -> TaskModel:
        return await super().update(entity=entity, **kwargs)
