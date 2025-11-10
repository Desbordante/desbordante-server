from fastapi import APIRouter, Request, status
from fastapi.responses import RedirectResponse

from src.api.auth.dependencies import GoogleClientDep

router = APIRouter()


@router.get(
    "/google/authorize/",
    status_code=status.HTTP_307_TEMPORARY_REDIRECT,
    summary="Google OAuth authorize",
    description="Authorize endpoint for Google OAuth authentication",
)
async def google_authorize(
    request: Request, google: GoogleClientDep
) -> RedirectResponse:
    redirect_uri = request.url_for("google_callback")
    return await google.authorize_redirect(request, redirect_uri)
