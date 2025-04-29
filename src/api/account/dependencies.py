from typing import Annotated

from fastapi import Depends

from src.api.dependencies import UserCrudDep, VerificationDep
from src.models.user_models import UserModel
from src.usecases.account.confirm_email import ConfirmEmailUseCase
from src.usecases.account.send_confirmation_email import SendConfirmationEmailUseCase

NotVerifiedUserDep = Annotated[
    UserModel, Depends(VerificationDep(should_be_verified=False))
]


async def get_send_confirmation_email_use_case(
    user: NotVerifiedUserDep,
) -> SendConfirmationEmailUseCase:
    return SendConfirmationEmailUseCase(user=user)


SendConfirmationEmailUseCaseDep = Annotated[
    SendConfirmationEmailUseCase, Depends(get_send_confirmation_email_use_case)
]


async def get_confirm_email_use_case(
    user_crud: UserCrudDep,
) -> ConfirmEmailUseCase:
    return ConfirmEmailUseCase(user_crud=user_crud)


ConfirmEmailUseCaseDep = Annotated[
    ConfirmEmailUseCase, Depends(get_confirm_email_use_case)
]
