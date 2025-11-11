from typing import Any

from fastapi import APIRouter, Path, Request, status

from src.api.auth.dependencies import (
    CreateUserSessionUseCaseDep,
    GetOAuthUserInfoUseCaseDep,
    GetOrCreateUserViaOAuthUseCaseDep,
)
from src.schemas.auth_schemas import OAuthCredsSchema, OAuthProvider
from src.schemas.user_schemas import UserSchema

router = APIRouter()


@router.get(
    "/{provider}/callback/",
    response_model=UserSchema,
    status_code=status.HTTP_200_OK,
    summary="OAuth callback",
    description="Callback endpoint for OAuth authentication",
)
async def oauth_callback(
    request: Request,
    get_oauth_user_info: GetOAuthUserInfoUseCaseDep,
    get_or_create_user_via_oauth: GetOrCreateUserViaOAuthUseCaseDep,
    create_session: CreateUserSessionUseCaseDep,
    provider: OAuthProvider = Path(..., description="OAuth provider name"),
) -> Any:
    # 1. Get OAuth user info (session loaded in adapter)
    oauth_user_info = await get_oauth_user_info(provider=provider, request=request)

    # 2. Get or create user
    creds = OAuthCredsSchema(provider=provider, oauth_id=oauth_user_info.id)
    user = await get_or_create_user_via_oauth(creds=creds)

    # 3. Create session
    await create_session(user=user)

    return user
