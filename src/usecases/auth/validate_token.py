from datetime import datetime, timezone
from typing import Type

from jwt import PyJWTError

from src.domain.auth.exceptions import CredentialsException
from src.domain.auth.utils import decode_token
from src.schemas.auth_schemas import TokenPayloadSchema


class ValidateTokenUseCase:
    def __call__[T: TokenPayloadSchema](
        self, *, schema: Type[T], token: str | None
    ) -> T:
        if not token:
            raise CredentialsException()

        try:
            token_data = decode_token(schema=schema, token=token)

            if token_data.exp <= datetime.now(timezone.utc):
                raise CredentialsException()

        except (PyJWTError, ValueError):
            raise CredentialsException()

        return token_data
