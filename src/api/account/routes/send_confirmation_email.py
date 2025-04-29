from fastapi import APIRouter, status

from src.api.account.dependencies import (
    NotVerifiedUserDep,
)
from src.api.dependencies import SendConfirmationEmailUseCaseDep
from src.schemas.base_schemas import ApiErrorSchema

router = APIRouter()


@router.post(
    "/confirm",
    response_model=None,
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Send confirmation email",
    description="Send confirmation email to user's email",
    responses={
        status.HTTP_401_UNAUTHORIZED: {"model": ApiErrorSchema},
        status.HTTP_403_FORBIDDEN: {"model": ApiErrorSchema},
    },
)
async def send_confirmation_email(
    user: NotVerifiedUserDep,
    send_confirmation_email: SendConfirmationEmailUseCaseDep,
) -> None:
    await send_confirmation_email(to_email=user.email)

    return None
