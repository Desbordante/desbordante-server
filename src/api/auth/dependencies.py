from functools import lru_cache
from typing import Annotated, Callable

from authlib.integrations.starlette_client import OAuth, StarletteOAuth2App
from fastapi import Depends

from src.domain.auth.config import settings
from src.schemas.auth_schemas import OAuthProvider


@lru_cache()
def get_oauth() -> OAuth:
    oauth = OAuth()

    oauth.register(
        name=OAuthProvider.GITHUB,
        client_id=settings.GITHUB_CLIENT_ID,
        client_secret=settings.GITHUB_CLIENT_SECRET,
        authorize_url="https://github.com/login/oauth/authorize",
        access_token_url="https://github.com/login/oauth/access_token",
        userinfo_endpoint="https://api.github.com/user",
        client_kwargs={"scope": "openid"},
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


OAuthDep = Annotated[OAuth, Depends(get_oauth)]


async def get_get_oauth_client(
    oauth: OAuthDep,
) -> Callable[[OAuthProvider], StarletteOAuth2App]:
    def get_oauth_client(provider: OAuthProvider) -> StarletteOAuth2App:
        client: StarletteOAuth2App | None = oauth.create_client(provider)

        assert client is not None, f"OAuth provider '{provider}' not found"

        return client

    return get_oauth_client


GetOAuthClientDep = Annotated[
    Callable[[OAuthProvider], StarletteOAuth2App], Depends(get_get_oauth_client)
]
