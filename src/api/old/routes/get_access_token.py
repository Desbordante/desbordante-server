from typing import Annotated

from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm

from src.api.old.dependencies import AuthenticateUserUseCaseDep, CreateTokensUseCaseDep
from src.schemas.auth_schemas import AuthenticateUserSchema
from src.schemas.base_schemas import ApiErrorSchema, BaseSchema

router = APIRouter()


class TokenResponseSchema(BaseSchema):
    access_token: str
    token_type: str = "bearer"


@router.post(
    "/token",
    response_model=TokenResponseSchema,
    status_code=status.HTTP_200_OK,
    summary="Get access token (API docs only)",
    description="Get access token using OAuth2 password flow. This endpoint is for Swagger/OpenAPI documentation testing only.",
    responses={
        status.HTTP_401_UNAUTHORIZED: {"model": ApiErrorSchema},
    },
)
async def get_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    authenticate_user: AuthenticateUserUseCaseDep,
    create_tokens: CreateTokensUseCaseDep,
) -> TokenResponseSchema:
    user = await authenticate_user(
        data=AuthenticateUserSchema(
            email=form_data.username,
            password=form_data.password,
        )
    )
    access_token_pair, _ = create_tokens(user=user)

    return TokenResponseSchema(
        access_token=access_token_pair.token,
    )
