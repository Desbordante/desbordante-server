from typing import Any
from uuid import UUID

from fastapi import APIRouter, status

from src.api.dataset.dependencies import DeleteDatasetUseCaseDep
from src.api.dependencies import AuthenticatedActorDep
from src.schemas.base_schemas import ApiErrorSchema

router = APIRouter()


@router.delete(
    "/{dataset_id}/",
    response_model=None,
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete dataset",
    description="Delete dataset by id",
    responses={
        status.HTTP_401_UNAUTHORIZED: {"model": ApiErrorSchema},
        status.HTTP_403_FORBIDDEN: {"model": ApiErrorSchema},
        status.HTTP_404_NOT_FOUND: {"model": ApiErrorSchema},
    },
)
async def delete_dataset(
    dataset_id: UUID,
    delete_dataset: DeleteDatasetUseCaseDep,
    actor: AuthenticatedActorDep,
) -> Any:
    return await delete_dataset(
        id=dataset_id,
        actor=actor,
    )
