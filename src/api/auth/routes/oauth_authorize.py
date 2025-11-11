from fastapi import APIRouter, Path, Request, status
from fastapi.responses import RedirectResponse

from src.api.auth.dependencies import GetOAuthClientDep
from src.schemas.auth_schemas import OAuthProvider

router = APIRouter()


@router.get(
    "/{provider}/authorize/",
    status_code=status.HTTP_302_FOUND,
    summary="OAuth authorize",
    description="Authorize endpoint for OAuth authentication",
)
async def oauth_authorize(
    request: Request,
    get_oauth_client: GetOAuthClientDep,
    provider: OAuthProvider = Path(..., description="OAuth provider name"),
) -> RedirectResponse:
    oauth_client = get_oauth_client(provider)

    redirect_uri = request.url_for("oauth_callback", provider=provider.value)

    return await oauth_client.authorize_redirect(request, redirect_uri)
