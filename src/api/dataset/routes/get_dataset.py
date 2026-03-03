from typing import Any
from uuid import UUID

from fastapi import APIRouter, status

from src.api.dataset.dependencies import GetDatasetUseCaseDep
from src.api.dependencies import ActorDep
from src.schemas.base_schemas import ApiErrorSchema
from src.schemas.dataset_schemas import DatasetSchema

router = APIRouter()


@router.get(
    "/{dataset_id}/",
    response_model=DatasetSchema,
    status_code=status.HTTP_200_OK,
    summary="Get dataset",
    description="Get dataset by id (public datasets accessible to all, private datasets require ownership or admin)",
    responses={
        status.HTTP_401_UNAUTHORIZED: {"model": ApiErrorSchema},
        status.HTTP_403_FORBIDDEN: {"model": ApiErrorSchema},
        status.HTTP_404_NOT_FOUND: {"model": ApiErrorSchema},
    },
)
async def get_dataset(
    dataset_id: UUID,
    get_dataset: GetDatasetUseCaseDep,
    actor: ActorDep,
) -> Any:
    return await get_dataset(id=dataset_id, actor=actor)
