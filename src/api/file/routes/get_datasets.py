from typing import Any

from fastapi import APIRouter, status

from src.api.dependencies import PaginationParamsDep
from src.api.file.dependencies import GetDatasetsUseCaseDep
from src.schemas.base_schemas import ApiErrorSchema
from src.schemas.file_schemas import (
    DatasetSchema,
)

router = APIRouter()


@router.get(
    "/datasets",
    response_model=list[DatasetSchema],
    status_code=status.HTTP_200_OK,
    summary="Get datasets",
    description="Get user datasets",
    responses={
        status.HTTP_401_UNAUTHORIZED: {"model": ApiErrorSchema},
    },
)
async def get_datasets(
    pagination: PaginationParamsDep,
    get_datasets: GetDatasetsUseCaseDep,
) -> Any:
    datasets = await get_datasets(limit=pagination.limit, offset=pagination.offset)

    return datasets
