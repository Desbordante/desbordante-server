from typing import Any

from fastapi import APIRouter, status

from src.api.user.dependencies import CurrentUserDep
from src.schemas.base_schemas import ApiErrorSchema
from src.schemas.user_schemas import UserSchema

router = APIRouter()


@router.get(
    "/me/",
    response_model=UserSchema,
    status_code=status.HTTP_200_OK,
    summary="Get current user info",
    description="Returns information about the currently authenticated user",
    responses={
        status.HTTP_401_UNAUTHORIZED: {"model": ApiErrorSchema},
    },
)
async def get_me(
    user: CurrentUserDep,
) -> Any:
    return user
