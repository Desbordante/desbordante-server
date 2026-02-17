from fastapi import APIRouter, Path, Request, status
from fastapi.responses import RedirectResponse

from src.api.auth.dependencies import (
    CreateUserSessionUseCaseDep,
    GetOAuthUserInfoUseCaseDep,
    GetOrCreateUserViaOAuthUseCaseDep,
)
from src.domain.auth.config import settings
from src.infrastructure.rate_limit.config import settings as rate_limit_settings
from src.infrastructure.rate_limit.limiter import limiter
from src.models.user_models import UserModel
from src.schemas.auth_schemas import OAuthCredsSchema, OAuthProvider

router = APIRouter()


class UserAdapter:
    def __init__(self, user: UserModel):
        self.id = user.id
        self.is_admin = user.is_admin
        self.is_banned = user.is_banned


@router.get(
    "/{provider}/callback/",
    status_code=status.HTTP_302_FOUND,
    summary="OAuth callback",
    description="Callback endpoint for OAuth authentication",
)
@limiter.limit(rate_limit_settings.AUTH_RATE_LIMIT)
@limiter.limit(rate_limit_settings.AUTH_RATE_LIMIT_HOURLY)
async def oauth_callback(
    request: Request,
    get_oauth_user_info: GetOAuthUserInfoUseCaseDep,
    get_or_create_user_via_oauth: GetOrCreateUserViaOAuthUseCaseDep,
    create_session: CreateUserSessionUseCaseDep,
    provider: OAuthProvider = Path(..., description="OAuth provider name"),
) -> RedirectResponse:
    oauth_user_info = await get_oauth_user_info(provider=provider, request=request)

    creds = OAuthCredsSchema(provider=provider, oauth_id=oauth_user_info.id)

    user = await get_or_create_user_via_oauth(creds=creds)

    await create_session(request=request, user=UserAdapter(user=user))

    return RedirectResponse(
        url=settings.OAUTH_SUCCESS_REDIRECT_URL, status_code=status.HTTP_302_FOUND
    )
