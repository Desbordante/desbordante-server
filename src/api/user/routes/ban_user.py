from typing import Any

from fastapi import APIRouter, Path, status

from src.api.user.dependencies import BanUserUseCaseDep
from src.schemas.base_schemas import ApiErrorSchema
from src.schemas.user_schemas import UserSchema

router = APIRouter()


@router.post(
    "/{user_id}/ban/",
    status_code=status.HTTP_200_OK,
    response_model=UserSchema,
    summary="Ban user",
    description="Ban user by ID and clear all their active sessions (admin only)",
    responses={
        status.HTTP_401_UNAUTHORIZED: {"model": ApiErrorSchema},
        status.HTTP_403_FORBIDDEN: {"model": ApiErrorSchema},
        status.HTTP_404_NOT_FOUND: {"model": ApiErrorSchema},
    },
)
async def ban_user(
    ban_user_use_case: BanUserUseCaseDep,
    user_id: int = Path(..., description="User id"),
) -> Any:
    user = await ban_user_use_case(user_id=user_id)
    return user
