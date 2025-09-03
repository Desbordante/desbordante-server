from abc import ABC
from typing import Any, Sequence, TypedDict, Unpack
from uuid import UUID

from sqlalchemy import (
    ColumnElement,
    ColumnExpressionArgument,
    asc,
    desc,
    exc,
    func,
    select,
)
from sqlalchemy.ext.asyncio import AsyncSession

from src.exceptions import ResourceAlreadyExistsException, ResourceNotFoundException
from src.models.base_models import BaseModel
from src.schemas.base_schemas import (
    FiltersParamsSchema,
    OrderingDirection,
    PaginatedResult,
    PaginationParamsSchema,
)


class BaseFindProps[T: int | UUID](TypedDict, total=False):
    id: T


class BaseUpdateProps(TypedDict, total=False): ...


class BaseCrud[
    ModelType: BaseModel,
    IdType: int | UUID = UUID,
](ABC):
    model: type[ModelType]
    _session: AsyncSession

    def __init__(self, *, session: AsyncSession):
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

    def _make_filters(
        self, filters_params: FiltersParamsSchema
    ) -> Sequence[ColumnExpressionArgument[bool] | None]:
        return []

    def _get_ordering_field(self, order_by: str) -> ColumnElement[ModelType]:
        return getattr(self.model, order_by)

    async def get_many(
        self,
        *,
        pagination: PaginationParamsSchema,
        query_params: Any,
        **kwargs: Unpack[BaseFindProps[IdType]],
    ) -> PaginatedResult[ModelType]:
        query = select(
            self.model,
            func.count().over().label("total_count"),
        ).filter_by(**kwargs)

        filters = [
            filter
            for filter in self._make_filters(query_params.filters)
            if filter is not None
        ]
        query = query.where(*filters)

        if query_params.ordering.order_by is not None:
            ordering_field = self._get_ordering_field(query_params.ordering.order_by)

            query = query.order_by(
                asc(ordering_field)
                if query_params.ordering.direction == OrderingDirection.Asc
                else desc(ordering_field)
            )

        query = query.limit(pagination.limit).offset(pagination.offset)

        result = await self._session.execute(query)

        rows = result.all()

        return PaginatedResult(
            items=[row[0] for row in rows],
            total_count=rows[0][1] if rows else 0,
            limit=pagination.limit,
            offset=pagination.offset,
        )

    async def update(
        self, *, entity: ModelType, **kwargs: Unpack[BaseUpdateProps]
    ) -> ModelType:
        for key, value in kwargs.items():
            if isinstance(value, list):
                self._session.add_all(value)  # type: ignore
            else:
                setattr(entity, key, value)

        await self._session.commit()
        await self._session.refresh(entity)
        return entity

    async def delete(self, *, entity: ModelType) -> None:
        await self._session.delete(entity)
        await self._session.commit()
