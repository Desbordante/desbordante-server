from typing import Any

from fastapi import APIRouter, status

from src.api.account.dependencies import ConfirmEmailUseCaseDep
from src.schemas.base_schemas import ApiErrorSchema
from src.schemas.user_schemas import UserSchema

router = APIRouter()


@router.put(
    "/email/verify/",
    response_model=UserSchema,
    status_code=status.HTTP_200_OK,
    summary="Confirm email",
    description="Confirm user's email by token.",
    responses={
        status.HTTP_403_FORBIDDEN: {"model": ApiErrorSchema},
        status.HTTP_404_NOT_FOUND: {"model": ApiErrorSchema},
        status.HTTP_422_UNPROCESSABLE_ENTITY: {"model": ApiErrorSchema},
    },
)
async def confirm_email(
    token: str,
    confirm_email: ConfirmEmailUseCaseDep,
) -> Any:
    user = await confirm_email(token=token)
    return user
