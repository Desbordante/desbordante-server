from typing import Annotated, Any

from fastapi import APIRouter, Depends, status

from src.api.dependencies import PaginationParamsDep
from src.api.user.dependencies import GetMyDatasetsUseCaseDep
from src.schemas.base_schemas import ApiErrorSchema, PaginatedResult
from src.schemas.dataset_schemas import DatasetQueryParamsSchema, PrivateDatasetSchema

router = APIRouter()

DatasetQueryParamsDep = Annotated[
    DatasetQueryParamsSchema, Depends(DatasetQueryParamsSchema)
]


@router.get(
    "/me/datasets/",
    response_model=PaginatedResult[PrivateDatasetSchema],
    status_code=status.HTTP_200_OK,
    summary="Get my private datasets",
    description="Get list of current user's private datasets",
    responses={
        status.HTTP_401_UNAUTHORIZED: {"model": ApiErrorSchema},
    },
)
async def get_my_datasets(
    get_my_datasets: GetMyDatasetsUseCaseDep,
    pagination: PaginationParamsDep,
    query_params: DatasetQueryParamsDep,
) -> Any:
    return await get_my_datasets(
        pagination=pagination,
        query_params=query_params,
    )
