from fastapi import APIRouter, Request, status
from fastapi.responses import RedirectResponse

from src.api.auth.dependencies import GitHubClientDep

router = APIRouter()


@router.get(
    "/github/authorize/",
    status_code=status.HTTP_307_TEMPORARY_REDIRECT,
    summary="GitHub OAuth authorize",
    description="Authorize endpoint for GitHub OAuth authentication",
)
async def github_authorize(
    request: Request, github: GitHubClientDep
) -> RedirectResponse:
    redirect_uri = request.url_for("github_callback")
    return await github.authorize_redirect(request, redirect_uri)
