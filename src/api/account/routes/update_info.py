from typing import Annotated, Any

from fastapi import APIRouter, Form, status

from src.api.account.dependencies import UpdateInfoUseCaseDep
from src.schemas.account_schemas import UpdateUserInfoSchema
from src.schemas.base_schemas import ApiErrorSchema
from src.schemas.user_schemas import UserSchema

router = APIRouter()


@router.patch(
    "/",
    response_model=UserSchema,
    status_code=status.HTTP_200_OK,
    summary="Update user's info",
    description="Update user's account info.",
    responses={
        status.HTTP_401_UNAUTHORIZED: {"model": ApiErrorSchema},
    },
)
async def update_info(
    update_info: UpdateInfoUseCaseDep,
    form_data: Annotated[UpdateUserInfoSchema, Form()],
) -> Any:
    user = await update_info(data=form_data)
    return user
