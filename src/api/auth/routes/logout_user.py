from fastapi import APIRouter, Response, status

from src.api.constants import ACCESS_TOKEN_KEY, REFRESH_TOKEN_KEY

router = APIRouter()


@router.post(
    "/logout/",
    response_model=None,
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Logout user",
    description="Clear authentication cookies",
)
async def logout_user(
    response: Response,
) -> None:
    response.delete_cookie(key=ACCESS_TOKEN_KEY)
    response.delete_cookie(key=REFRESH_TOKEN_KEY)
    return None
