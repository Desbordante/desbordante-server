from typing import Any

from fastapi import APIRouter, Path, status

from src.api.user.dependencies import UnbanUserUseCaseDep
from src.schemas.base_schemas import ApiErrorSchema
from src.schemas.user_schemas import UserSchema

router = APIRouter()


@router.post(
    "/{user_id}/unban/",
    status_code=status.HTTP_200_OK,
    response_model=UserSchema,
    summary="Unban user",
    description="Unban user by ID (admin only)",
    responses={
        status.HTTP_401_UNAUTHORIZED: {"model": ApiErrorSchema},
        status.HTTP_403_FORBIDDEN: {"model": ApiErrorSchema},
        status.HTTP_404_NOT_FOUND: {"model": ApiErrorSchema},
    },
)
async def unban_user(
    unban_user_use_case: UnbanUserUseCaseDep,
    user_id: int = Path(..., description="User id"),
) -> Any:
    user = await unban_user_use_case(user_id=user_id)
    return user
