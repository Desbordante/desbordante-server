from typing import Any

from fastapi import APIRouter, Path, status

from src.api.user.dependencies import AdminSessionDep, GetUserByIdUseCaseDep
from src.schemas.base_schemas import ApiErrorSchema
from src.schemas.user_schemas import UserSchema

router = APIRouter()


@router.get(
    "/{user_id}/",
    response_model=UserSchema,
    status_code=status.HTTP_200_OK,
    summary="Get user info by ID",
    description="Returns information about a specific user",
    responses={
        status.HTTP_401_UNAUTHORIZED: {"model": ApiErrorSchema},
        status.HTTP_403_FORBIDDEN: {"model": ApiErrorSchema},
        status.HTTP_404_NOT_FOUND: {"model": ApiErrorSchema},
    },
)
async def get_user_by_id(
    get_user_by_id: GetUserByIdUseCaseDep,
    admin_session: AdminSessionDep,
    user_id: int = Path(..., description="User id"),
) -> Any:
    return await get_user_by_id(id=user_id)
