from typing import Any

from fastapi import APIRouter, Request, status

from src.api.auth.dependencies import GoogleClientDep

router = APIRouter()


@router.get(
    "/google/callback/",
    response_model=dict[str, Any],
    status_code=status.HTTP_200_OK,
    summary="Google OAuth callback",
    description="Callback endpoint for Google OAuth authentication",
)
async def google_callback(request: Request, google: GoogleClientDep) -> dict[str, Any]:
    token = await google.authorize_access_token(request)
    user = token["userinfo"]
    return user
