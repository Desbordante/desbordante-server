from abc import ABC
from typing import TypedDict, Unpack
from uuid import UUID

from sqlalchemy import exc, select
from sqlalchemy.ext.asyncio import AsyncSession

from _app.exceptions.exceptions import ResourceNotFoundException
from src.exceptions import ResourceAlreadyExistsException
from src.models.base_models import BaseModel


class BaseFindProps[T: int | UUID](TypedDict, total=False):
    id: T


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
            raise ResourceNotFoundException(f"{self.model.__name__} not found")
