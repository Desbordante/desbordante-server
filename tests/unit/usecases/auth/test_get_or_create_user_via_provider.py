import pytest
from pytest_mock import MockerFixture

from src.exceptions import ResourceNotFoundException
from src.schemas.auth_schemas import AuthCredsSchema, AuthProvider
from src.usecases.auth.get_or_create_user_via_provider import (
    GetOrCreateUserViaProviderUseCase,
)

from tests.unit.usecases.auth.constants import (
    AUTH_ACCOUNT_NOT_FOUND_MESSAGE,
    FAKE_ACCOUNT_ID,
    FAKE_ACCOUNT_ID_GOOGLE,
    FAKE_EMAIL_ALT,
)

pytestmark = pytest.mark.asyncio


async def test_get_or_create_user_returns_existing_user_when_account_found(
    mocker: MockerFixture,
    get_or_create_user_via_provider_use_case: GetOrCreateUserViaProviderUseCase,
    auth_account_crud_mock,
    register_user_via_provider_mock,
    auth_creds,
    fake_user,
) -> None:
    auth_account = mocker.Mock()
    auth_account.owner = fake_user
    auth_account_crud_mock.get_by.return_value = auth_account

    result = await get_or_create_user_via_provider_use_case(creds=auth_creds)

    assert result == fake_user
    auth_account_crud_mock.get_by.assert_awaited_once_with(
        provider=AuthProvider.GITHUB,
        account_id=FAKE_ACCOUNT_ID,
    )
    register_user_via_provider_mock.assert_not_called()


async def test_get_or_create_user_registers_new_user_when_account_not_found(
    get_or_create_user_via_provider_use_case: GetOrCreateUserViaProviderUseCase,
    auth_account_crud_mock,
    register_user_via_provider_mock,
    auth_creds,
    fake_user,
) -> None:
    auth_account_crud_mock.get_by.side_effect = ResourceNotFoundException(
        AUTH_ACCOUNT_NOT_FOUND_MESSAGE
    )

    result = await get_or_create_user_via_provider_use_case(creds=auth_creds)

    assert result == fake_user
    auth_account_crud_mock.get_by.assert_awaited_once_with(
        provider=AuthProvider.GITHUB,
        account_id=FAKE_ACCOUNT_ID,
    )
    register_user_via_provider_mock.assert_awaited_once_with(creds=auth_creds)


async def test_get_or_create_user_passes_creds_to_register(
    get_or_create_user_via_provider_use_case: GetOrCreateUserViaProviderUseCase,
    auth_account_crud_mock,
    register_user_via_provider_mock,
    auth_creds,
) -> None:
    auth_account_crud_mock.get_by.side_effect = ResourceNotFoundException(
        AUTH_ACCOUNT_NOT_FOUND_MESSAGE
    )
    creds_google = AuthCredsSchema(
        provider=AuthProvider.GOOGLE,
        account_id=FAKE_ACCOUNT_ID_GOOGLE,
        email=FAKE_EMAIL_ALT,
    )

    await get_or_create_user_via_provider_use_case(creds=creds_google)

    register_user_via_provider_mock.assert_awaited_once_with(creds=creds_google)
