from typing import Any

from fastapi import APIRouter, Path, Request, status

from src.api.auth.dependencies import GetOAuthClientDep
from src.schemas.auth_schemas import OAuthProvider

router = APIRouter()


@router.get(
    "/{provider}/callback/",
    response_model=dict[str, Any],
    status_code=status.HTTP_200_OK,
    summary="OAuth callback",
    description="Callback endpoint for OAuth authentication",
)
async def oauth_callback(
    request: Request,
    get_oauth_client: GetOAuthClientDep,
    provider: OAuthProvider = Path(..., description="OAuth provider name"),
) -> dict[str, Any]:
    oauth_client = get_oauth_client(provider)
    token = await oauth_client.authorize_access_token(request)

    user = token.get("userinfo")
    if user is None:
        user = await oauth_client.userinfo(token=token)

    return user
