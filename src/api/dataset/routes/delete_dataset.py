from typing import Any
from uuid import UUID

from fastapi import APIRouter, status

from src.api.dataset.dependencies import DeleteDatasetUseCaseDep
from src.schemas.base_schemas import ApiErrorSchema

router = APIRouter()


@router.delete(
    "/{id}/",
    response_model=None,
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete dataset",
    description="Delete user dataset by id",
    responses={
        status.HTTP_401_UNAUTHORIZED: {"model": ApiErrorSchema},
        status.HTTP_404_NOT_FOUND: {"model": ApiErrorSchema},
    },
)
async def delete_dataset(
    id: UUID,
    delete_dataset: DeleteDatasetUseCaseDep,
) -> Any:
    return await delete_dataset(id=id)
