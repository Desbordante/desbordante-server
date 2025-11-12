from fastapi import APIRouter, Request, status

from src.api.auth.dependencies import DestroySessionUseCaseDep

router = APIRouter()


@router.post(
    "/logout/",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Logout",
    description="Destroy current user session",
)
async def logout(
    request: Request,
    destroy_session: DestroySessionUseCaseDep,
) -> None:
    await destroy_session(request=request)
