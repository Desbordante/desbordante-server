"""Mapping OAuth provider userinfo responses to canonical format."""

from src.schemas.auth_schemas import OAuthProvider

OAUTH_ID_FIELDS: dict[OAuthProvider, str] = {
    OAuthProvider.GITHUB: "id",
    OAuthProvider.GOOGLE: "sub",
}


def extract_oauth_id(userinfo: dict, provider: OAuthProvider) -> str:
    """Extract OAuth user ID from userinfo based on provider."""
    field = OAUTH_ID_FIELDS.get(provider)
    if not field or field not in userinfo:
        raise ValueError(f"Unknown or invalid OAuth provider: {provider}")
    return str(userinfo[field])
