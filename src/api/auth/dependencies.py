from functools import lru_cache
from typing import Annotated

from authlib.integrations.starlette_client import OAuth, StarletteOAuth2App
from fastapi import Depends

from src.domain.auth.config import settings


@lru_cache()
def get_oauth() -> OAuth:
    oauth = OAuth()

    oauth.register(
        name="github",
        client_id=settings.GITHUB_CLIENT_ID,
        client_secret=settings.GITHUB_CLIENT_SECRET,
        authorize_url="https://github.com/login/oauth/authorize",
        access_token_url="https://github.com/login/oauth/access_token",
        userinfo_endpoint="https://api.github.com/user",
        client_kwargs={"scope": "openid"},
    )

    oauth.register(
        name="google",
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


async def get_github_client(oauth: OAuthDep) -> StarletteOAuth2App:
    github: StarletteOAuth2App | None = oauth.create_client("github")

    assert github is not None, "GitHub client not found"

    return github


GitHubClientDep = Annotated[StarletteOAuth2App, Depends(get_github_client)]


async def get_google_client(oauth: OAuthDep) -> StarletteOAuth2App:
    google: StarletteOAuth2App | None = oauth.create_client("google")

    assert google is not None, "Google client not found"

    return google


GoogleClientDep = Annotated[StarletteOAuth2App, Depends(get_google_client)]
