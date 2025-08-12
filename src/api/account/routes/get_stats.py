from typing import Any

from fastapi import APIRouter, status

from src.api.account.dependencies import GetStatsUseCaseDep
from src.schemas.account_schemas import AccountStatsSchema
from src.schemas.base_schemas import ApiErrorSchema

router = APIRouter()


@router.get(
    "/stats/",
    response_model=AccountStatsSchema,
    status_code=status.HTTP_200_OK,
    summary="Get current user's account stats",
    description="Returns statistics about the currently authenticated user",
    responses={
        status.HTTP_401_UNAUTHORIZED: {"model": ApiErrorSchema},
    },
)
async def get_stats(get_stats: GetStatsUseCaseDep) -> Any:
    return await get_stats()
