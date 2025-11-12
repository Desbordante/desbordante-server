from typing import Any
from uuid import UUID

from fastapi import APIRouter, status

from src.api.dataset.dependencies import GetDatasetUseCaseDep
from src.api.dependencies import OptionalUserSessionDep
from src.schemas.base_schemas import ApiErrorSchema
from src.schemas.dataset_schemas import DatasetSchema

router = APIRouter()


@router.get(
    "/{id}/",
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
    id: UUID,
    get_dataset: GetDatasetUseCaseDep,
    optional_session: OptionalUserSessionDep,
) -> Any:
    return await get_dataset(
        id=id,
        current_user_id=optional_session.id if optional_session else None,
        is_admin=optional_session.is_admin if optional_session else False,
    )
