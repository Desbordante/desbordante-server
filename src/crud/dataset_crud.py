from typing import TypedDict, Unpack
from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.crud.base_crud import BaseCrud
from src.models.dataset_models import DatasetModel


class DatasetFindProps(TypedDict, total=False):
    id: UUID


class DatasetUpdateProps(TypedDict, total=False):
    pass


class DatasetCrud(BaseCrud[DatasetModel, UUID]):
    def __init__(self, session: AsyncSession):
        super().__init__(model=DatasetModel, session=session)

    async def get_by(self, **kwargs: Unpack[DatasetFindProps]) -> DatasetModel:
        return await super().get_by(**kwargs)

    async def update(
        self, *, entity: DatasetModel, **kwargs: Unpack[DatasetUpdateProps]
    ) -> DatasetModel:
        return await super().update(entity=entity, **kwargs)

    async def get_user_datasets_size(self, *, owner_id: int) -> int:
        query = select(func.sum(self.model.size)).where(
            self.model.owner_id == owner_id,
        )
        result = await self._session.execute(query)
        return result.scalar() or 0
