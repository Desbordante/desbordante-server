import pytest

from src.models.auth_models import AuthAccountModel
from src.models.user_models import UserModel
from src.schemas.auth_schemas import AuthCredsSchema, AuthProvider
from src.usecases.auth.register_user_via_provider import RegisterUserViaProviderUseCase

from tests.unit.usecases.auth.constants import (
    FAKE_ACCOUNT_ID,
    FAKE_ACCOUNT_ID_GOOGLE,
    FAKE_EMAIL,
    FAKE_EMAIL_ALT,
)

pytestmark = pytest.mark.asyncio


async def test_register_user_via_provider_success(
    register_user_via_provider_use_case: RegisterUserViaProviderUseCase,
    user_crud_mock,
    auth_creds,
    fake_user,
) -> None:
    user_crud_mock.create.return_value = fake_user

    result = await register_user_via_provider_use_case(creds=auth_creds)

    assert result == fake_user
    user_crud_mock.create.assert_awaited_once()
    call_args = user_crud_mock.create.await_args
    user_model = call_args.kwargs["entity"]
    assert isinstance(user_model, UserModel)
    assert user_model.email == FAKE_EMAIL
    assert len(user_model.auth_accounts) == 1
    assert isinstance(user_model.auth_accounts[0], AuthAccountModel)
    assert user_model.auth_accounts[0].provider == AuthProvider.GITHUB
    assert user_model.auth_accounts[0].account_id == FAKE_ACCOUNT_ID


async def test_register_user_via_provider_creates_user_with_correct_creds(
    register_user_via_provider_use_case: RegisterUserViaProviderUseCase,
    user_crud_mock,
) -> None:
    creds = AuthCredsSchema(
        provider=AuthProvider.GOOGLE,
        account_id=FAKE_ACCOUNT_ID_GOOGLE,
        email=FAKE_EMAIL_ALT,
    )

    await register_user_via_provider_use_case(creds=creds)

    user_model = user_crud_mock.create.await_args.kwargs["entity"]
    assert user_model.email == FAKE_EMAIL_ALT
    assert user_model.auth_accounts[0].provider == AuthProvider.GOOGLE
    assert user_model.auth_accounts[0].account_id == FAKE_ACCOUNT_ID_GOOGLE
