from typing import Any

from fastapi import APIRouter, Path, Request, status

from src.api.auth.dependencies import OAuthCallbackUseCaseDep
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
    oauth_callback: OAuthCallbackUseCaseDep,
    provider: OAuthProvider = Path(..., description="OAuth provider name"),
) -> dict[str, Any]:
    user_info = await oauth_callback(provider=provider, request=request)
    return user_info
