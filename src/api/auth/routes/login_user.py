from typing import Annotated

from fastapi import APIRouter, Form, Response, status

from src.api.auth.dependencies import AuthenticateUserUseCaseDep, CreateTokensUseCaseDep
from src.api.auth.utils import set_auth_cookies
from src.schemas.auth_schemas import AuthenticateUserSchema, AuthResponseSchema
from src.schemas.base_schemas import ApiErrorSchema
from src.schemas.user_schemas import UserSchema

router = APIRouter()


@router.post(
    "/login/",
    response_model=AuthResponseSchema,
    status_code=status.HTTP_200_OK,
    summary="Login user",
    description="Authenticate user with email and password, set auth cookies and return tokens",
    responses={
        status.HTTP_401_UNAUTHORIZED: {"model": ApiErrorSchema},
    },
)
async def login_user(
    response: Response,
    form_data: Annotated[AuthenticateUserSchema, Form()],
    authenticate_user: AuthenticateUserUseCaseDep,
    create_tokens: CreateTokensUseCaseDep,
) -> AuthResponseSchema:
    user = await authenticate_user(data=form_data)
    access_token_pair, refresh_token_pair = create_tokens(user=user)
    set_auth_cookies(response, access_token_pair, refresh_token_pair)

    return AuthResponseSchema(
        access_token=access_token_pair.token,
        user=UserSchema.model_validate(user),
    )
