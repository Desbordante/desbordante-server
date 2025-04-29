from typing import Type

from src.domain.auth.exceptions import CredentialsException
from src.domain.security.exceptions import ExpiredTokenException, InvalidTokenException
from src.domain.security.utils import decode_token
from src.schemas.auth_schemas import AuthTokenPayloadSchema


class ValidateTokenUseCase:
    def __call__[T: AuthTokenPayloadSchema](
        self, *, schema: Type[T], token: str | None
    ) -> T:
        if not token:
            raise CredentialsException()

        try:
            token_data = decode_token(schema=schema, token=token)

        except (InvalidTokenException, ExpiredTokenException):
            raise CredentialsException()

        return token_data
