from typing import TypedDict, Unpack
from uuid import UUID

from sqlalchemy import Select
from sqlalchemy.ext.asyncio import AsyncSession

from src.crud.base_crud import BaseCrud
from src.models.file_models import DatasetModel


class DatasetFindProps(TypedDict, total=False):
    id: UUID


class DatasetUpdateProps(TypedDict, total=False):
    pass


class DatasetCrud(BaseCrud[DatasetModel, UUID]):
    def __init__(self, session: AsyncSession):
        super().__init__(model=DatasetModel, session=session)

    async def get_by(self, **kwargs: Unpack[DatasetFindProps]) -> DatasetModel:
        return await super().get_by(**kwargs)

    async def get_many(
        self,
        *,
        limit: int = 100,
        offset: int = 0,
        query: Select[tuple[DatasetModel]] | None = None,
        **kwargs: Unpack[DatasetFindProps],
    ) -> list[DatasetModel]:
        return await super().get_many(limit=limit, offset=offset, query=query, **kwargs)

    async def update(
        self, *, entity: DatasetModel, **kwargs: Unpack[DatasetUpdateProps]
    ) -> DatasetModel:
        return await super().update(entity=entity, **kwargs)
