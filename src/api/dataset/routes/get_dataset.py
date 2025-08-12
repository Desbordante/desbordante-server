from typing import Any
from uuid import UUID

from fastapi import APIRouter, status

from src.api.dataset.dependencies import GetDatasetUseCaseDep
from src.schemas.base_schemas import ApiErrorSchema
from src.schemas.dataset_schemas import DatasetSchema

router = APIRouter()


@router.get(
    "/{id}/",
    response_model=DatasetSchema,
    status_code=status.HTTP_200_OK,
    summary="Get dataset",
    description="Get user dataset by id",
    responses={
        status.HTTP_401_UNAUTHORIZED: {"model": ApiErrorSchema},
        status.HTTP_404_NOT_FOUND: {"model": ApiErrorSchema},
    },
)
async def get_dataset(
    id: UUID,
    get_dataset: GetDatasetUseCaseDep,
) -> Any:
    dataset = await get_dataset(id=id)

    return dataset
