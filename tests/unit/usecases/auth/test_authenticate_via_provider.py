import pytest

from src.exceptions import ForbiddenException
from src.schemas.auth_schemas import AuthCredsSchema, AuthProvider
from src.usecases.auth.authenticate_via_provider import AuthenticateViaProviderUseCase
from tests.unit.usecases.auth.constants import (
    FAKE_ACCOUNT_ID,
    FAKE_EMAIL,
    FAKE_SESSION_TOKEN,
    FORBIDDEN_EMAIL_NOT_VERIFIED_MESSAGE,
)

pytestmark = pytest.mark.asyncio


async def test_authenticate_via_provider_success(
    authenticate_via_provider_use_case: AuthenticateViaProviderUseCase,
    auth_service_mock,
    get_or_create_user_mock,
    create_session_mock,
    verified_user_info,
    fake_user,
) -> None:
    auth_service_mock.get_userinfo.return_value = verified_user_info

    result = await authenticate_via_provider_use_case(provider=AuthProvider.GITHUB)

    assert result == FAKE_SESSION_TOKEN
    auth_service_mock.get_userinfo.assert_awaited_once_with(
        provider=AuthProvider.GITHUB
    )
    get_or_create_user_mock.assert_awaited_once_with(
        creds=AuthCredsSchema(
            provider=AuthProvider.GITHUB,
            account_id=FAKE_ACCOUNT_ID,
            email=FAKE_EMAIL,
        )
    )
    create_session_mock.assert_awaited_once_with(user=fake_user)


async def test_authenticate_via_provider_raises_forbidden_when_email_not_verified(
    authenticate_via_provider_use_case: AuthenticateViaProviderUseCase,
    auth_service_mock,
    get_or_create_user_mock,
    create_session_mock,
    unverified_user_info,
) -> None:
    auth_service_mock.get_userinfo.return_value = unverified_user_info

    with pytest.raises(ForbiddenException) as exc_info:
        await authenticate_via_provider_use_case(provider=AuthProvider.GITHUB)

    assert exc_info.value.detail == FORBIDDEN_EMAIL_NOT_VERIFIED_MESSAGE
    auth_service_mock.get_userinfo.assert_awaited_once_with(
        provider=AuthProvider.GITHUB
    )
    get_or_create_user_mock.assert_not_called()
    create_session_mock.assert_not_called()


async def test_authenticate_via_provider_passes_correct_creds_to_get_or_create_user(
    authenticate_via_provider_use_case: AuthenticateViaProviderUseCase,
    auth_service_mock,
    get_or_create_user_mock,
    verified_user_info,
) -> None:
    auth_service_mock.get_userinfo.return_value = verified_user_info

    await authenticate_via_provider_use_case(provider=AuthProvider.GOOGLE)

    call_args = get_or_create_user_mock.await_args
    creds = call_args.kwargs["creds"]
    assert creds == AuthCredsSchema(
        provider=AuthProvider.GOOGLE,
        account_id=FAKE_ACCOUNT_ID,
        email=FAKE_EMAIL,
    )


async def test_authenticate_via_provider_passes_user_to_create_session(
    authenticate_via_provider_use_case: AuthenticateViaProviderUseCase,
    auth_service_mock,
    get_or_create_user_mock,
    create_session_mock,
    verified_user_info,
    fake_user,
) -> None:
    auth_service_mock.get_userinfo.return_value = verified_user_info

    await authenticate_via_provider_use_case(provider=AuthProvider.GITHUB)

    create_session_mock.assert_awaited_once_with(user=fake_user)
