from fastapi import APIRouter, Path, Request, status
from fastapi.responses import RedirectResponse

from src.api.auth.dependencies import AuthServiceDep
from src.infrastructure.rate_limit.config import settings as rate_limit_settings
from src.infrastructure.rate_limit.limiter import limiter
from src.schemas.auth_schemas import AuthProvider

router = APIRouter()


@router.get(
    "/{provider}/authorize/",
    status_code=status.HTTP_302_FOUND,
    summary="Redirect to auth provider authorize URL",
    description="Redirect to auth provider authorize URL for the given provider",
)
@limiter.limit(rate_limit_settings.AUTH_RATE_LIMIT)
@limiter.limit(rate_limit_settings.AUTH_RATE_LIMIT_HOURLY)
async def provider_authorize(
    request: Request,
    auth_service: AuthServiceDep,
    provider: AuthProvider = Path(..., description="Auth provider name"),
) -> RedirectResponse:
    redirect_uri = str(request.url_for("provider_callback", provider=provider.value))
    return await auth_service.get_authorization_redirect(
        provider=provider, redirect_uri=redirect_uri
    )
