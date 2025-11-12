from typing import Any

from fastapi import APIRouter, Path, status

from src.api.user.dependencies import UpdateUserStatusUseCaseDep
from src.schemas.base_schemas import ApiErrorSchema
from src.schemas.user_schemas import UpdateUserStatusSchema, UserSchema

router = APIRouter()


@router.patch(
    "/{user_id}/status/",
    status_code=status.HTTP_200_OK,
    response_model=UserSchema,
    summary="Update user status",
    description="Update user status (ban/unban) - admin only. Banning a user clears all their active sessions.",
    responses={
        status.HTTP_401_UNAUTHORIZED: {"model": ApiErrorSchema},
        status.HTTP_403_FORBIDDEN: {"model": ApiErrorSchema},
        status.HTTP_404_NOT_FOUND: {"model": ApiErrorSchema},
    },
)
async def update_user_status(
    update_user_status_use_case: UpdateUserStatusUseCaseDep,
    status_data: UpdateUserStatusSchema,
    user_id: int = Path(..., description="User id"),
) -> Any:
    user = await update_user_status_use_case(
        user_id=user_id, is_banned=status_data.is_banned
    )
    return user
