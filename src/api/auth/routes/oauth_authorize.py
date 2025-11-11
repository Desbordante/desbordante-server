from fastapi import APIRouter, Path, Request, status
from fastapi.responses import RedirectResponse

from src.api.auth.dependencies import OAuthAuthorizeUseCaseDep
from src.schemas.auth_schemas import OAuthProvider

router = APIRouter()


@router.get(
    "/{provider}/authorize/",
    status_code=status.HTTP_302_FOUND,
    summary="Redirect to OAuth authorize URL",
    description="Redirect to OAuth authorize URL for the given provider",
)
async def oauth_authorize(
    request: Request,
    redirect_to_authorize_url: OAuthAuthorizeUseCaseDep,
    provider: OAuthProvider = Path(..., description="OAuth provider name"),
) -> RedirectResponse:
    redirect_uri = str(request.url_for("oauth_callback", provider=provider.value))
    return await redirect_to_authorize_url(
        provider=provider, request=request, redirect_uri=redirect_uri
    )
