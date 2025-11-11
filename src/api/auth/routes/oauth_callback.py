from fastapi import APIRouter, Path, Request, status

from src.api.auth.dependencies import (
    GetOAuthUserInfoUseCaseDep,
    GetOrCreateUserViaOAuthUseCaseDep,
)
from src.schemas.auth_schemas import (
    OAuthCredentialsSchema,
    OAuthProvider,
    OAuthUserInfoSchema,
)

router = APIRouter()


@router.get(
    "/{provider}/callback/",
    response_model=OAuthUserInfoSchema,
    status_code=status.HTTP_200_OK,
    summary="OAuth callback",
    description="Callback endpoint for OAuth authentication",
)
async def oauth_callback(
    request: Request,
    get_oauth_user_info: GetOAuthUserInfoUseCaseDep,
    get_or_create_user_via_oauth: GetOrCreateUserViaOAuthUseCaseDep,
    provider: OAuthProvider = Path(..., description="OAuth provider name"),
) -> OAuthUserInfoSchema:
    oauth_user_info = await get_oauth_user_info(provider=provider, request=request)
    credentials = OAuthCredentialsSchema(provider=provider, oauth_id=oauth_user_info.id)
    user = await get_or_create_user_via_oauth(credentials=credentials)
    return OAuthUserInfoSchema(id=str(user.id))
