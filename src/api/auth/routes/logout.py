from fastapi import APIRouter, status

from src.api.auth.dependencies import DestroySessionUseCaseDep

router = APIRouter()


@router.post(
    "/logout/",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Logout",
    description="Destroy current user session",
)
async def logout(
    destroy_session: DestroySessionUseCaseDep,
) -> None:
    await destroy_session()
