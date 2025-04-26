from datetime import datetime, timedelta, timezone
from typing import Any, Tuple, Type

import jwt

from src.domain.auth.config import settings
from src.models.user_models import UserModel
from src.schemas.auth_schemas import (
    AccessTokenPayloadSchema,
    RefreshTokenPayloadSchema,
    TokenPairSchema,
    TokenPayloadSchema,
)


class CreateTokensUseCase:
    def _create_token[T: TokenPayloadSchema](
        self, *, schema: Type[T], payload: dict[str, Any], expires_delta: timedelta
    ) -> TokenPairSchema:
        expire = datetime.now(timezone.utc) + expires_delta
        to_encode = schema.model_validate({**payload, "exp": expire}).model_dump()
        token = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
        return TokenPairSchema(
            token=token,
            expires=expire,
        )

    def __call__(self, *, user: UserModel) -> Tuple[TokenPairSchema, TokenPairSchema]:
        access_token_pair = self._create_token(
            schema=AccessTokenPayloadSchema,
            payload={"id": user.id},
            expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
        )
        refresh_token_pair = self._create_token(
            schema=RefreshTokenPayloadSchema,
            payload={"id": user.id},
            expires_delta=timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS),
        )
        return access_token_pair, refresh_token_pair
