from typing import Annotated

from fastapi import APIRouter, Form, status

from src.api.auth.dependencies import SendResetEmailUseCaseDep
from src.schemas.base_schemas import ApiErrorSchema

router = APIRouter()


@router.post(
    "/password-reset/",
    response_model=None,
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Send password reset email",
    description="Send password reset email to user's email",
    responses={
        status.HTTP_404_NOT_FOUND: {"model": ApiErrorSchema},
    },
)
async def send_reset_email(
    email: Annotated[str, Form()],
    send_reset_email: SendResetEmailUseCaseDep,
) -> None:
    await send_reset_email(to_email=email)

    return None
