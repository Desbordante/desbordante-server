from fastapi import APIRouter, Path, Request, status
from fastapi.responses import RedirectResponse
from starsessions import load_session

from src.api.auth.dependencies import GetOAuthAuthorizationRedirectUseCaseDep
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
    get_authorization_redirect: GetOAuthAuthorizationRedirectUseCaseDep,
    provider: OAuthProvider = Path(..., description="OAuth provider name"),
) -> RedirectResponse:
    await load_session(request)

    redirect_uri = str(request.url_for("oauth_callback", provider=provider.value))
    return await get_authorization_redirect(
        provider=provider, request=request, redirect_uri=redirect_uri
    )
