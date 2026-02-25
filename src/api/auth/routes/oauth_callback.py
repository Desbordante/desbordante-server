from fastapi import APIRouter, Path, Request, status
from fastapi.responses import RedirectResponse

from src.api.auth.dependencies import AuthenticateViaProviderUseCaseDep
from src.api.auth.utils import set_session_cookie
from src.domain.auth.config import settings
from src.infrastructure.rate_limit.config import settings as rate_limit_settings
from src.infrastructure.rate_limit.limiter import limiter
from src.schemas.auth_schemas import AuthProvider

router = APIRouter()


@router.get(
    "/{provider}/callback/",
    status_code=status.HTTP_302_FOUND,
    summary="Auth provider callback",
    description="Callback endpoint for auth provider authentication",
)
@limiter.limit(rate_limit_settings.AUTH_RATE_LIMIT)
@limiter.limit(rate_limit_settings.AUTH_RATE_LIMIT_HOURLY)
async def provider_callback(
    request: Request,  # Used by rate limiter, don't remove
    authenticate_via_provider: AuthenticateViaProviderUseCaseDep,
    provider: AuthProvider = Path(..., description="Auth provider name"),
) -> RedirectResponse:
    session_id = await authenticate_via_provider(provider=provider)

    response = RedirectResponse(
        url=settings.AUTH_SUCCESS_REDIRECT_URL, status_code=status.HTTP_302_FOUND
    )

    set_session_cookie(response, session_id)

    return response
