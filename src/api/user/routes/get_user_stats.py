from typing import Any

from fastapi import APIRouter, Path, status

from src.api.user.dependencies import GetUserStatsUseCaseDep
from src.schemas.base_schemas import ApiErrorSchema
from src.schemas.user_schemas import UserStatsSchema

router = APIRouter()


@router.get(
    "/{user_id}/stats/",
    response_model=UserStatsSchema,
    status_code=status.HTTP_200_OK,
    summary="Get user stats by ID",
    description="Returns statistics about a specific user",
    responses={
        status.HTTP_401_UNAUTHORIZED: {"model": ApiErrorSchema},
        status.HTTP_403_FORBIDDEN: {"model": ApiErrorSchema},
        status.HTTP_404_NOT_FOUND: {"model": ApiErrorSchema},
    },
)
async def get_user_stats(
    get_user_stats: GetUserStatsUseCaseDep,
    user_id: int = Path(..., description="User id"),
) -> Any:
    return await get_user_stats(user_id=user_id)
