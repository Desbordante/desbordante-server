from typing import Annotated, Any

from fastapi import APIRouter, Depends, status

from src.api.dependencies import PaginationParamsDep
from src.api.user.dependencies import GetUserDatasetsUseCaseDep
from src.schemas.base_schemas import ApiErrorSchema, PaginatedResult
from src.schemas.dataset_schemas import DatasetQueryParamsSchema, DatasetSchema

router = APIRouter()

DatasetQueryParamsDep = Annotated[
    DatasetQueryParamsSchema, Depends(DatasetQueryParamsSchema)
]


@router.get(
    "/{user_id}/datasets/",
    response_model=PaginatedResult[DatasetSchema],
    status_code=status.HTTP_200_OK,
    summary="Get user's datasets",
    description="Get list of specific user's datasets (admin only)",
    responses={
        status.HTTP_401_UNAUTHORIZED: {"model": ApiErrorSchema},
        status.HTTP_403_FORBIDDEN: {"model": ApiErrorSchema},
    },
)
async def get_user_datasets(
    user_id: int,
    get_user_datasets: GetUserDatasetsUseCaseDep,
    pagination: PaginationParamsDep,
    query_params: DatasetQueryParamsDep,
) -> Any:
    return await get_user_datasets(
        user_id=user_id,
        pagination=pagination,
        query_params=query_params,
    )
