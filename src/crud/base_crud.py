from abc import ABC
from typing import TypedDict, Unpack
from uuid import UUID

from sqlalchemy import Select, exc, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.exceptions import ResourceAlreadyExistsException, ResourceNotFoundException
from src.models.base_models import BaseModel
from src.schemas.base_schemas import PaginationParams


class BaseFindProps[T: int | UUID](TypedDict, total=False):
    id: T


class BaseUpdateProps(TypedDict, total=False): ...


class BaseCrud[
    ModelType: BaseModel,
    IdType: int | UUID = UUID,
](ABC):
    def __init__(self, *, model: type[ModelType], session: AsyncSession):
        self.model = model
        self._session = session

    async def create(self, entity: ModelType) -> ModelType:
        try:
            self._session.add(entity)
            await self._session.commit()
            await self._session.refresh(entity)
            return entity
        except exc.IntegrityError:
            await self._session.rollback()
            raise ResourceAlreadyExistsException(
                f"{self.model.__name__} already exists"
            )

    async def get_by(self, **kwargs: Unpack[BaseFindProps[IdType]]) -> ModelType:
        try:
            query = select(self.model).filter_by(**kwargs)
            result = await self._session.execute(query)
            return result.scalars().one()
        except exc.NoResultFound:
            raise ResourceNotFoundException(
                f"{self.model.__name__.replace('Model', '')} not found"
            )

    async def get_many(
        self,
        *,
        pagination: PaginationParams,
        query: Select[tuple[ModelType]] | None = None,
        **kwargs: Unpack[BaseFindProps[IdType]],
    ) -> list[ModelType]:
        if query is None:
            query = (
                select(self.model)
                .filter_by(**kwargs)
                .limit(pagination.limit)
                .offset(pagination.offset)
            )
        result = await self._session.execute(query)
        return list(result.scalars().all())

    async def update(
        self, *, entity: ModelType, **kwargs: Unpack[BaseUpdateProps]
    ) -> ModelType:
        for key, value in kwargs.items():
            setattr(entity, key, value)
        await self._session.commit()
        await self._session.refresh(entity)
        return entity

    async def delete(self, *, entity: ModelType) -> None:
        await self._session.delete(entity)
        await self._session.commit()
