from fastapi import APIRouter, Response, status

from src.api.auth.dependencies import (
    CreateTokensUseCaseDep,
    GetUserByIdUseCaseDep,
    RefreshTokenPayloadDep,
)
from src.api.auth.utils import set_auth_cookies
from src.schemas.auth_schemas import AuthResponseSchema
from src.schemas.base_schemas import ApiErrorSchema
from src.schemas.user_schemas import UserSchema

router = APIRouter()


@router.post(
    "/refresh",
    response_model=AuthResponseSchema,
    status_code=status.HTTP_200_OK,
    summary="Refresh access token",
    description="Get new access token using refresh token from cookies",
    responses={
        status.HTTP_401_UNAUTHORIZED: {"model": ApiErrorSchema},
    },
)
async def refresh_token(
    response: Response,
    refresh_token_payload: RefreshTokenPayloadDep,
    get_user_by_id: GetUserByIdUseCaseDep,
    create_tokens: CreateTokensUseCaseDep,
) -> AuthResponseSchema:
    user = await get_user_by_id(id=refresh_token_payload.id)
    access_token_pair, refresh_token_pair = create_tokens(user=user)
    set_auth_cookies(response, access_token_pair, refresh_token_pair)

    return AuthResponseSchema(
        access_token=access_token_pair.token,
        user=UserSchema.model_validate(user),
    )
