from datetime import timedelta
from typing import Tuple

from src.domain.auth.config import settings
from src.domain.auth.utils import create_token
from src.models.user_models import UserModel
from src.schemas.auth_schemas import (
    AccessTokenPayloadSchema,
    RefreshTokenPayloadSchema,
    TokenPairSchema,
)


class CreateTokensUseCase:
    def __call__(self, *, user: UserModel) -> Tuple[TokenPairSchema, TokenPairSchema]:
        access_token_pair = create_token(
            schema=AccessTokenPayloadSchema,
            payload={"id": user.id},
            expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
        )
        refresh_token_pair = create_token(
            schema=RefreshTokenPayloadSchema,
            payload={"id": user.id},
            expires_delta=timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS),
        )
        return access_token_pair, refresh_token_pair
