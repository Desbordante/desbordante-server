import pytest
from pytest_mock import MockerFixture

from src.schemas.auth_schemas import AuthCredsSchema, AuthProvider, AuthUserInfoSchema
from src.usecases.auth.authenticate_via_provider import AuthenticateViaProviderUseCase
from src.usecases.auth.get_or_create_user_via_provider import (
    GetOrCreateUserViaProviderUseCase,
)
from src.usecases.auth.register_user_via_provider import RegisterUserViaProviderUseCase

from tests.unit.usecases.auth.constants import (
    FAKE_ACCOUNT_ID,
    FAKE_EMAIL,
    FAKE_SESSION_TOKEN,
)


@pytest.fixture
def auth_service_mock(mocker: MockerFixture):
    mock = mocker.Mock()
    mock.get_userinfo = mocker.AsyncMock()
    return mock


@pytest.fixture
def fake_user(mocker: MockerFixture):
    return mocker.Mock()


@pytest.fixture
def get_or_create_user_mock(mocker: MockerFixture, fake_user):
    return mocker.AsyncMock(return_value=fake_user)


@pytest.fixture
def create_session_mock(mocker: MockerFixture):
    return mocker.AsyncMock(return_value=FAKE_SESSION_TOKEN)


@pytest.fixture
def verified_user_info() -> AuthUserInfoSchema:
    return AuthUserInfoSchema(
        account_id=FAKE_ACCOUNT_ID,
        email=FAKE_EMAIL,
        is_verified=True,
    )


@pytest.fixture
def unverified_user_info() -> AuthUserInfoSchema:
    return AuthUserInfoSchema(
        account_id=FAKE_ACCOUNT_ID,
        email=FAKE_EMAIL,
        is_verified=False,
    )


@pytest.fixture
def auth_creds() -> AuthCredsSchema:
    return AuthCredsSchema(
        provider=AuthProvider.GITHUB,
        account_id=FAKE_ACCOUNT_ID,
        email=FAKE_EMAIL,
    )


@pytest.fixture
def authenticate_via_provider_use_case(
    auth_service_mock,
    get_or_create_user_mock,
    create_session_mock,
) -> AuthenticateViaProviderUseCase:
    return AuthenticateViaProviderUseCase(
        auth_service=auth_service_mock,
        get_or_create_user_via_provider=get_or_create_user_mock,
        create_session=create_session_mock,
    )


# --- GetOrCreateUserViaProviderUseCase fixtures ---


@pytest.fixture
def auth_account_crud_mock(mocker: MockerFixture):
    mock = mocker.Mock()
    mock.get_by = mocker.AsyncMock()
    return mock


@pytest.fixture
def register_user_via_provider_mock(mocker: MockerFixture, fake_user):
    return mocker.AsyncMock(return_value=fake_user)


@pytest.fixture
def get_or_create_user_via_provider_use_case(
    auth_account_crud_mock,
    register_user_via_provider_mock,
) -> GetOrCreateUserViaProviderUseCase:
    return GetOrCreateUserViaProviderUseCase(
        register_user_via_provider=register_user_via_provider_mock,
        auth_account_crud=auth_account_crud_mock,
    )


# --- RegisterUserViaProviderUseCase fixtures ---


@pytest.fixture
def user_crud_mock(mocker: MockerFixture):
    mock = mocker.Mock()
    mock.create = mocker.AsyncMock()
    return mock


@pytest.fixture
def register_user_via_provider_use_case(
    user_crud_mock,
) -> RegisterUserViaProviderUseCase:
    return RegisterUserViaProviderUseCase(user_crud=user_crud_mock)
