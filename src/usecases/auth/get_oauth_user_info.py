from typing import Protocol

from fastapi import Request

from src.schemas.auth_schemas import OAuthProvider, OAuthUserInfoSchema


class OAuthPort(Protocol):
    """Port for OAuth operations."""

    async def get_user_info(
        self, *, provider: OAuthProvider, request: Request
    ) -> OAuthUserInfoSchema: ...


class GetOAuthUserInfoUseCase:
    """Use case for getting OAuth user info from callback."""

    def __init__(self, oauth_adapter: OAuthPort):
        self.oauth_adapter = oauth_adapter

    async def __call__(
        self, *, provider: OAuthProvider, request: Request
    ) -> OAuthUserInfoSchema:
        return await self.oauth_adapter.get_user_info(
            provider=provider, request=request
        )
