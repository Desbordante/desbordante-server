from fastapi import APIRouter, Response, status

from src.api.auth.dependencies import DestroySessionUseCaseDep
from src.api.auth.utils import clear_session_cookie
from src.api.dependencies import SessionIdDep

router = APIRouter()


@router.post(
    "/logout/",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Logout",
    description="Destroy current user session",
)
async def logout(
    destroy_session: DestroySessionUseCaseDep,
    session_id: SessionIdDep,
    response: Response,
) -> None:
    await destroy_session(session_id=session_id)

    clear_session_cookie(response)
