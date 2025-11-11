from typing import Any

from src.schemas.auth_schemas import OAuthProvider


def extract_oauth_id(userinfo: dict[str, Any], provider: OAuthProvider) -> str:
    """Extract OAuth user ID from userinfo based on provider."""
    if provider == OAuthProvider.GITHUB:
        # GitHub returns numeric ID, convert to string
        return str(userinfo["id"])
    elif provider == OAuthProvider.GOOGLE:
        # Google returns "sub" field
        return str(userinfo["sub"])
    else:
        raise ValueError(f"Unknown OAuth provider: {provider}")
