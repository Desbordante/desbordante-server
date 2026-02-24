from unittest.mock import patch

import pytest

from src.infrastructure.auth.userinfo_mapper import (
    OAUTH_ID_FIELDS,
    extract_oauth_id,
)
from src.schemas.auth_schemas import OAuthProvider


@pytest.mark.parametrize(
    "userinfo,provider,expected",
    [
        ({"id": 12345, "login": "testuser"}, OAuthProvider.GITHUB, "12345"),
        ({"id": 999}, OAuthProvider.GITHUB, "999"),
        (
            {"sub": "google-abc-123", "email": "test@example.com"},
            OAuthProvider.GOOGLE,
            "google-abc-123",
        ),
    ],
)
def test_extract_oauth_id_returns_correct_field(
    userinfo: dict, provider: OAuthProvider, expected: str
) -> None:
    assert extract_oauth_id(userinfo, provider) == expected


@patch("src.infrastructure.auth.userinfo_mapper.OAUTH_ID_FIELDS", {})
def test_extract_oauth_id_raises_for_unknown_provider() -> None:
    with pytest.raises(ValueError, match="Unknown or invalid OAuth provider"):
        extract_oauth_id({"id": "123"}, OAuthProvider.GITHUB)


@pytest.mark.parametrize(
    "userinfo,provider",
    [
        ({"login": "test"}, OAuthProvider.GITHUB),
        ({"email": "test@example.com"}, OAuthProvider.GOOGLE),
    ],
)
def test_extract_oauth_id_raises_when_field_missing_in_userinfo(
    userinfo: dict, provider: OAuthProvider
) -> None:
    with pytest.raises(ValueError, match="Unknown or invalid OAuth provider"):
        extract_oauth_id(userinfo, provider)


def test_oauth_id_fields_contains_all_providers() -> None:
    assert OAuthProvider.GITHUB in OAUTH_ID_FIELDS
    assert OAuthProvider.GOOGLE in OAUTH_ID_FIELDS
    assert OAUTH_ID_FIELDS[OAuthProvider.GITHUB] == "id"
    assert OAUTH_ID_FIELDS[OAuthProvider.GOOGLE] == "sub"
