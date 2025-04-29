from datetime import datetime
from typing import Annotated, Any

from fastapi import APIRouter, Depends, Query, status

from src.api.dependencies import PaginationParamsDep
from src.api.file.dependencies import GetDatasetsUseCaseDep
from src.schemas.base_schemas import ApiErrorSchema
from src.schemas.file_schemas import (
    DatasetFilterSchema,
    DatasetOrderingSchema,
    DatasetSchema,
    DatasetSortField,
    SortDirection,
)

router = APIRouter()


# Функция для парсинга параметров сортировки из query params
def parse_ordering_params(
    order_by: DatasetSortField | None = Query(None, description="Field to order by"),
    order_direction: SortDirection | None = Query(
        None, description="Order direction (asc or desc)"
    ),
) -> DatasetOrderingSchema | None:
    """Parse ordering parameters from query params"""
    if order_by:
        return DatasetOrderingSchema(
            field=order_by, direction=order_direction or SortDirection.ASC
        )
    return None


# Функция для парсинга параметров фильтрации из query params
def parse_filter_params(
    min_size: int | None = Query(None, description="Minimum file size in bytes", ge=0),
    max_size: int | None = Query(None, description="Maximum file size in bytes", ge=0),
    created_after: str | None = Query(
        None, description="Filter datasets created after this date (ISO format)"
    ),
    created_before: str | None = Query(
        None, description="Filter datasets created before this date (ISO format)"
    ),
    search: str | None = Query(None, description="Search term for file name"),
) -> DatasetFilterSchema:
    """Parse filter parameters from query params"""
    # Convert string dates to datetime objects if provided
    after_date = datetime.fromisoformat(created_after) if created_after else None
    before_date = datetime.fromisoformat(created_before) if created_before else None

    return DatasetFilterSchema(
        min_size=min_size,
        max_size=max_size,
        created_after=after_date,
        created_before=before_date,
        search=search,
    )


@router.get(
    "/datasets",
    response_model=list[DatasetSchema],
    status_code=status.HTTP_200_OK,
    summary="Get datasets",
    description="Get user datasets with filtering, ordering and searching capabilities",
    responses={
        status.HTTP_401_UNAUTHORIZED: {"model": ApiErrorSchema},
    },
)
async def get_datasets(
    pagination: PaginationParamsDep,
    get_datasets: GetDatasetsUseCaseDep,
    filters: Annotated[DatasetFilterSchema, Depends(parse_filter_params)],
    ordering: Annotated[DatasetOrderingSchema | None, Depends(parse_ordering_params)],
) -> Any:
    datasets = await get_datasets(
        limit=pagination.limit,
        offset=pagination.offset,
        filters=filters,
        ordering=ordering,
    )

    return datasets
