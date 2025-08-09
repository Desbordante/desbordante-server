from typing import Any

from fastapi import APIRouter, status

from src.api.dataset.dependencies import GetDatasetsUseCaseDep
from src.api.dependencies import PaginationParamsDep
from src.schemas.base_schemas import ApiErrorSchema
from src.schemas.dataset_schemas import DatasetSchema

router = APIRouter()


@router.get(
    "/",
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
) -> Any:
    datasets = await get_datasets(pagination=pagination)

    return datasets
