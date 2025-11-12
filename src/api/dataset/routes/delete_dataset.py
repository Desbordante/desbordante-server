from typing import Any
from uuid import UUID

from fastapi import APIRouter, status

from src.api.dataset.dependencies import DeleteDatasetUseCaseDep
from src.api.dependencies import UserSessionDep
from src.schemas.base_schemas import ApiErrorSchema

router = APIRouter()


@router.delete(
    "/{id}/",
    response_model=None,
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete dataset",
    description="Delete dataset by id (public datasets: admin only, private datasets: owner or admin)",
    responses={
        status.HTTP_401_UNAUTHORIZED: {"model": ApiErrorSchema},
        status.HTTP_403_FORBIDDEN: {"model": ApiErrorSchema},
        status.HTTP_404_NOT_FOUND: {"model": ApiErrorSchema},
    },
)
async def delete_dataset(
    id: UUID,
    delete_dataset: DeleteDatasetUseCaseDep,
    user_session: UserSessionDep,
) -> Any:
    return await delete_dataset(
        id=id,
        current_user_id=user_session.id,
        is_admin=user_session.is_admin,
    )
