from typing import Annotated

from fastapi import APIRouter, Form, Response, status

from src.api.auth.dependencies import (
    CreateTokensUseCaseDep,
    ResetPasswordUseCaseDep,
)
from src.api.auth.utils import set_auth_cookies
from src.schemas.auth_schemas import AuthResponseSchema, ResetPasswordSchema
from src.schemas.base_schemas import ApiErrorSchema
from src.schemas.user_schemas import UserSchema

router = APIRouter()


@router.put(
    "/password-reset/",
    response_model=AuthResponseSchema,
    status_code=status.HTTP_200_OK,
    summary="Reset password",
    description="Reset password for user",
    responses={
        status.HTTP_404_NOT_FOUND: {"model": ApiErrorSchema},
    },
)
async def reset_password(
    response: Response,
    token: str,
    form_data: Annotated[ResetPasswordSchema, Form()],
    reset_password: ResetPasswordUseCaseDep,
    create_tokens: CreateTokensUseCaseDep,
) -> AuthResponseSchema:
    user = await reset_password(token=token, data=form_data)

    access_token_pair, refresh_token_pair = create_tokens(user=user)
    set_auth_cookies(response, access_token_pair, refresh_token_pair)

    return AuthResponseSchema(
        access_token=access_token_pair.token,
        user=UserSchema.model_validate(user),
    )
