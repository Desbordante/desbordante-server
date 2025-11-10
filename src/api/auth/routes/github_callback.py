from typing import Any

from fastapi import APIRouter, Request, status

from src.api.auth.dependencies import GitHubClientDep

router = APIRouter()


@router.get(
    "/github/callback/",
    response_model=dict[str, Any],
    status_code=status.HTTP_200_OK,
    summary="GitHub OAuth callback",
    description="Callback endpoint for GitHub OAuth authentication",
)
async def github_callback(request: Request, github: GitHubClientDep) -> dict[str, Any]:
    token = await github.authorize_access_token(request)
    user = await github.userinfo(token=token)
    return user
