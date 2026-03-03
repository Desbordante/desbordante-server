from typing import Any

from fastapi import APIRouter, Depends, Path, status

from src.api.dependencies import get_admin_actor
from src.api.user.dependencies import GetUserByIdUseCaseDep
from src.schemas.base_schemas import ApiErrorSchema
from src.schemas.user_schemas import UserSchema

router = APIRouter()


@router.get(
    "/{user_id}/",
    response_model=UserSchema,
    status_code=status.HTTP_200_OK,
    summary="Get user info by ID (admin only)",
    description="Returns information about a specific user (admin only)",
    responses={
        status.HTTP_401_UNAUTHORIZED: {"model": ApiErrorSchema},
        status.HTTP_403_FORBIDDEN: {"model": ApiErrorSchema},
        status.HTTP_404_NOT_FOUND: {"model": ApiErrorSchema},
    },
    dependencies=[Depends(get_admin_actor)],
)
async def get_user_by_id(
    get_user_by_id: GetUserByIdUseCaseDep,
    user_id: int = Path(..., description="User id"),
) -> Any:
    return await get_user_by_id(user_id=user_id)
