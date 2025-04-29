from typing import Annotated, Any

from fastapi import APIRouter, Form, status

from src.api.account.dependencies import ChangePasswordUseCaseDep
from src.schemas.account_schemas import ChangePasswordSchema
from src.schemas.base_schemas import ApiErrorSchema
from src.schemas.user_schemas import UserSchema

router = APIRouter()


@router.put(
    "/password",
    response_model=UserSchema,
    status_code=status.HTTP_200_OK,
    summary="Change password",
    description="Change user's password.",
    responses={
        status.HTTP_401_UNAUTHORIZED: {"model": ApiErrorSchema},
        status.HTTP_422_UNPROCESSABLE_ENTITY: {"model": ApiErrorSchema},
    },
)
async def change_password(
    change_password: ChangePasswordUseCaseDep,
    form_data: Annotated[ChangePasswordSchema, Form()],
) -> Any:
    user = await change_password(data=form_data)
    return user
