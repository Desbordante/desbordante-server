"""Factory for creating OAuth registry with registered providers."""

from authlib.integrations.starlette_client import OAuth

from src.domain.auth.config import settings
from src.schemas.auth_schemas import OAuthProvider


def create_oauth_registry() -> OAuth:
    """Create and configure OAuth instance with all providers."""
    oauth = OAuth()
    oauth.register(
        name=OAuthProvider.GITHUB,
        client_id=settings.GITHUB_CLIENT_ID,
        client_secret=settings.GITHUB_CLIENT_SECRET,
        authorize_url="https://github.com/login/oauth/authorize",
        access_token_url="https://github.com/login/oauth/access_token",
        userinfo_endpoint="https://api.github.com/user",
    )
    oauth.register(
        name=OAuthProvider.GOOGLE,
        client_id=settings.GOOGLE_CLIENT_ID,
        client_secret=settings.GOOGLE_CLIENT_SECRET,
        authorize_url="https://accounts.google.com/o/oauth2/v2/auth",
        access_token_url="https://oauth2.googleapis.com/token",
        userinfo_endpoint="https://www.googleapis.com/oauth2/v2/userinfo",
        server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
        client_kwargs={"scope": "openid"},
    )
    return oauth
