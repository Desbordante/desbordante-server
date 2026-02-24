from fastapi import APIRouter, Path, Request, status
from fastapi.responses import RedirectResponse

from src.api.auth.dependencies import AuthenticateViaOAuthUseCaseDep
from src.api.auth.utils import set_session_cookie
from src.domain.auth.config import settings
from src.infrastructure.rate_limit.config import settings as rate_limit_settings
from src.infrastructure.rate_limit.limiter import limiter
from src.schemas.auth_schemas import OAuthProvider

router = APIRouter()


@router.get(
    "/{provider}/callback/",
    status_code=status.HTTP_302_FOUND,
    summary="OAuth callback",
    description="Callback endpoint for OAuth authentication",
)
@limiter.limit(rate_limit_settings.AUTH_RATE_LIMIT)
@limiter.limit(rate_limit_settings.AUTH_RATE_LIMIT_HOURLY)
async def oauth_callback(
    request: Request,  # Used by rate limiter, don't remove
    authenticate_via_oauth: AuthenticateViaOAuthUseCaseDep,
    provider: OAuthProvider = Path(..., description="OAuth provider name"),
) -> RedirectResponse:
    session_id = await authenticate_via_oauth(provider=provider)

    response = RedirectResponse(
        url=settings.OAUTH_SUCCESS_REDIRECT_URL, status_code=status.HTTP_302_FOUND
    )

    set_session_cookie(response, session_id)

    return response
