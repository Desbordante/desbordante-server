from typing import Annotated, Any

from fastapi import APIRouter, Depends, status

from src.api.dependencies import PaginationParamsDep
from src.api.public.dependencies import GetPublicDatasetsUseCaseDep
from src.schemas.base_schemas import ApiErrorSchema, PaginatedResult
from src.schemas.dataset_schemas import DatasetQueryParamsSchema, PublicDatasetSchema

router = APIRouter()

DatasetQueryParamsDep = Annotated[
    DatasetQueryParamsSchema, Depends(DatasetQueryParamsSchema)
]


@router.get(
    "/",
    response_model=PaginatedResult[PublicDatasetSchema],
    status_code=status.HTTP_200_OK,
    summary="Get public datasets",
    description="Get list of public datasets (accessible by anyone, including anonymous users)",
    responses={
        status.HTTP_400_BAD_REQUEST: {"model": ApiErrorSchema},
    },
)
async def get_public_datasets(
    get_public_datasets: GetPublicDatasetsUseCaseDep,
    pagination: PaginationParamsDep,
    query_params: DatasetQueryParamsDep,
) -> Any:
    return await get_public_datasets(
        pagination=pagination,
        query_params=query_params,
    )
