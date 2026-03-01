from typing import Annotated, Any

from fastapi import APIRouter, Depends, status

from src.api.dependencies import AuthenticatedActorDep, PaginationParamsDep
from src.api.user.dependencies import GetUserDatasetsUseCaseDep
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
    get_user_datasets: GetUserDatasetsUseCaseDep,
    pagination: PaginationParamsDep,
    query_params: DatasetQueryParamsDep,
    actor: AuthenticatedActorDep,
) -> Any:
    return await get_user_datasets(
        user_id=actor.user_id,
        pagination=pagination,
        query_params=query_params,
    )
