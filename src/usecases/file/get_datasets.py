from typing import List, Protocol

from sqlalchemy import Select, and_, asc, desc, func, select
from sqlalchemy.sql.elements import ColumnElement

from src.models.file_models import DatasetModel, FileModel
from src.models.user_models import UserModel
from src.schemas.file_schemas import (
    DatasetFilterSchema,
    DatasetOrderingSchema,
    DatasetSortField,
    SortDirection,
)


class DatasetCrud(Protocol):
    async def get_many(
        self, *, limit: int, offset: int, query: Select[tuple[DatasetModel]]
    ) -> list[DatasetModel]: ...


class GetDatasetsUseCase:
    def __init__(
        self,
        *,
        dataset_crud: DatasetCrud,
        user: UserModel,
    ):
        self.dataset_crud = dataset_crud
        self.user = user

    async def __call__(
        self,
        *,
        limit: int = 100,
        offset: int = 0,
        filters: DatasetFilterSchema | None = None,
        ordering: DatasetOrderingSchema | None = None,
    ) -> list[DatasetModel]:
        # Base query joining dataset with file and filtering by owner
        query = (
            select(DatasetModel)
            .join(FileModel, DatasetModel.file_id == FileModel.id)
            .where(FileModel.owner_id == self.user.id)
        )

        # Apply filters if provided
        if filters:
            filter_conditions: List[ColumnElement[bool]] = []

            # File size filters
            if filters.min_size is not None:
                filter_conditions.append(FileModel.byte_size >= filters.min_size)
            if filters.max_size is not None:
                filter_conditions.append(FileModel.byte_size <= filters.max_size)

            # Date filters
            if filters.created_after is not None:
                filter_conditions.append(
                    DatasetModel.created_at >= filters.created_after
                )
            if filters.created_before is not None:
                filter_conditions.append(
                    DatasetModel.created_at <= filters.created_before
                )

            # Search by name
            if filters.search:
                search_term = f"%{filters.search}%"
                filter_conditions.append(
                    func.lower(FileModel.name).like(func.lower(search_term))
                )

            # Apply all filters
            if filter_conditions:
                query = query.where(and_(*filter_conditions))

        # Apply ordering if provided
        if ordering:
            # Handle different sort fields
            if ordering.field == DatasetSortField.NAME:
                order_by = FileModel.name
            elif ordering.field == DatasetSortField.SIZE:
                order_by = FileModel.byte_size
            elif ordering.field == DatasetSortField.CREATED_AT:
                order_by = DatasetModel.created_at
            else:
                # Default to created_at
                order_by = DatasetModel.created_at

            # Apply direction
            if ordering.direction == SortDirection.DESC:
                query = query.order_by(desc(order_by))
            else:
                query = query.order_by(asc(order_by))
        else:
            # Default ordering by created_at desc (newest first)
            query = query.order_by(desc(DatasetModel.created_at))

        # Apply pagination
        query = query.limit(limit).offset(offset)

        return await self.dataset_crud.get_many(limit=limit, offset=offset, query=query)
