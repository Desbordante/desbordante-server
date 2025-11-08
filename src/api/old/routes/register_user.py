from typing import Annotated

from fastapi import APIRouter, Form, Response, status

from src.api.dependencies import SendConfirmationEmailUseCaseDep
from src.api.old.dependencies import CreateTokensUseCaseDep, RegisterUserUseCaseDep
from src.api.old.utils import set_auth_cookies
from src.schemas.auth_schemas import AuthResponseSchema, RegisterUserSchema
from src.schemas.base_schemas import ApiErrorSchema
from src.schemas.user_schemas import UserSchema

router = APIRouter()


@router.post(
    "/register/",
    response_model=AuthResponseSchema,
    status_code=status.HTTP_201_CREATED,
    summary="Register new user",
    description="Create new user account with email and password",
    responses={
        status.HTTP_409_CONFLICT: {"model": ApiErrorSchema},
    },
)
async def register_user(
    response: Response,
    form_data: Annotated[RegisterUserSchema, Form()],
    register_user: RegisterUserUseCaseDep,
    create_tokens: CreateTokensUseCaseDep,
    send_confirmation_email: SendConfirmationEmailUseCaseDep,
) -> AuthResponseSchema:
    user = await register_user(data=form_data)
    access_token_pair, refresh_token_pair = create_tokens(user=user)
    set_auth_cookies(response, access_token_pair, refresh_token_pair)

    await send_confirmation_email(to_email=user.email)

    return AuthResponseSchema(
        access_token=access_token_pair.token,
        user=UserSchema.model_validate(user),
    )
