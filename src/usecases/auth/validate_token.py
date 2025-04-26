from datetime import datetime, timezone
from typing import Type

import jwt

from src.domain.auth.config import settings
from src.domain.auth.exceptions import CredentialsException
from src.schemas.auth_schemas import TokenPayloadSchema


class ValidateTokenUseCase:
    def __call__[T: TokenPayloadSchema](
        self, *, schema: Type[T], token: str | None
    ) -> T:
        if not token:
            raise CredentialsException()

        try:
            payload = jwt.decode(
                token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
            )
            token_data = schema.model_validate(payload)

            if token_data.exp <= datetime.now(timezone.utc):
                raise CredentialsException()

        except (jwt.PyJWTError, ValueError):
            raise CredentialsException()

        return token_data
