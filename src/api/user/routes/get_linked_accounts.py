from typing import Any

from fastapi import APIRouter, status

from src.api.user.dependencies import GetLinkedAccountsUseCaseDep
from src.schemas.auth_schemas import AuthAccountSchema
from src.schemas.base_schemas import ApiErrorSchema

router = APIRouter()


@router.get(
    "/me/linked-accounts/",
    response_model=list[AuthAccountSchema],
    status_code=status.HTTP_200_OK,
    summary="Get linked accounts",
    description="Returns list of OAuth accounts linked to the current user",
    responses={
        status.HTTP_401_UNAUTHORIZED: {"model": ApiErrorSchema},
    },
)
async def get_linked_accounts(
    get_linked_accounts_use_case: GetLinkedAccountsUseCaseDep,
) -> Any:
    return await get_linked_accounts_use_case()
