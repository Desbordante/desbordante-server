from typing import Any

from fastapi import APIRouter, status

from src.api.dependencies import AuthenticatedActorDep
from src.api.user.dependencies import GetUserStatsUseCaseDep
from src.schemas.base_schemas import ApiErrorSchema
from src.schemas.user_schemas import UserStatsSchema

router = APIRouter()


@router.get(
    "/me/stats/",
    response_model=UserStatsSchema,
    status_code=status.HTTP_200_OK,
    summary="Get current user stats",
    description="Returns statistics about the currently authenticated user",
    responses={
        status.HTTP_401_UNAUTHORIZED: {"model": ApiErrorSchema},
    },
)
async def get_my_stats(
    get_user_stats: GetUserStatsUseCaseDep, actor: AuthenticatedActorDep
) -> Any:
    return await get_user_stats(user_id=actor.user_id)
