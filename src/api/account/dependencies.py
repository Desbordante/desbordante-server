from typing import Annotated

from fastapi import Depends

from src.api.dependencies import UserCrudDep, VerificationDep
from src.models.user_models import UserModel
from src.usecases.account.confirm_email import ConfirmEmailUseCase

NotVerifiedUserDep = Annotated[
    UserModel, Depends(VerificationDep(should_be_verified=False))
]


async def get_confirm_email_use_case(
    user_crud: UserCrudDep,
) -> ConfirmEmailUseCase:
    return ConfirmEmailUseCase(user_crud=user_crud)


ConfirmEmailUseCaseDep = Annotated[
    ConfirmEmailUseCase, Depends(get_confirm_email_use_case)
]
