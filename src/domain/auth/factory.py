from authlib.integrations.starlette_client import OAuth, StarletteOAuth2App

from src.domain.auth.config import settings
from src.schemas.auth_schemas import OAuthProvider


class OAuthClientFactory:
    """Factory for creating OAuth clients."""

    def __init__(self):
        self.oauth = OAuth()

        self.oauth.register(
            name=OAuthProvider.GITHUB,
            client_id=settings.GITHUB_CLIENT_ID,
            client_secret=settings.GITHUB_CLIENT_SECRET,
            authorize_url="https://github.com/login/oauth/authorize",
            access_token_url="https://github.com/login/oauth/access_token",
            userinfo_endpoint="https://api.github.com/user",
            client_kwargs={"scope": "openid"},
        )

        self.oauth.register(
            name=OAuthProvider.GOOGLE,
            client_id=settings.GOOGLE_CLIENT_ID,
            client_secret=settings.GOOGLE_CLIENT_SECRET,
            authorize_url="https://accounts.google.com/o/oauth2/v2/auth",
            access_token_url="https://oauth2.googleapis.com/token",
            userinfo_endpoint="https://www.googleapis.com/oauth2/v2/userinfo",
            server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
            client_kwargs={"scope": "openid"},
        )

    def create(self, provider: OAuthProvider) -> StarletteOAuth2App:
        client = self.oauth.create_client(provider.value)

        if client is None:
            raise ValueError(f"OAuth provider '{provider.value}' not found")

        return client
