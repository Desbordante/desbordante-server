import http
from typing import Mapping

from fastapi import status


class BaseAppException(Exception):
    def __init__(
        self,
        detail: str | None = None,
        status_code: int = 500,
        headers: Mapping[str, str] | None = None,
    ) -> None:
        if detail is None:
            detail = http.HTTPStatus(status_code).phrase
        self.status_code = status_code
        self.detail = detail
        self.headers = headers

    def __str__(self) -> str:
        return f"{self.status_code}: {self.detail}"

    def __repr__(self) -> str:
        class_name = self.__class__.__name__
        return f"{class_name}(status_code={self.status_code!r}, detail={self.detail!r})"


class ResourceNotFoundException(BaseAppException):
    """Raised when a requested resource is not found"""

    def __init__(self, message: str):
        super().__init__(message, status_code=status.HTTP_404_NOT_FOUND)


class ValidationException(BaseAppException):
    """Raised when input validation fails"""

    def __init__(self, message: str):
        super().__init__(message, status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)


class UnauthorizedException(BaseAppException):
    """Raised when user is not authorized"""

    def __init__(self, message: str):
        super().__init__(
            message,
            status_code=status.HTTP_401_UNAUTHORIZED,
            headers={"WWW-Authenticate": "Bearer"},
        )


class ForbiddenException(BaseAppException):
    """Raised when user is authenticated but doesn't have required permissions"""

    def __init__(self, message: str):
        super().__init__(
            message,
            status_code=status.HTTP_403_FORBIDDEN,
        )


class ResourceAlreadyExistsException(BaseAppException):
    """Raised when attempting to create a resource that already exists"""

    def __init__(self, message: str):
        super().__init__(message, status_code=status.HTTP_409_CONFLICT)


class TooManyRequestsException(BaseAppException):
    """Raised when too many requests are made"""

    def __init__(self, message: str):
        super().__init__(message, status_code=status.HTTP_429_TOO_MANY_REQUESTS)


class ConflictException(BaseAppException):
    """Raised when a conflict occurs"""

    def __init__(self, message: str):
        super().__init__(message, status_code=status.HTTP_409_CONFLICT)


class PayloadTooLargeException(BaseAppException):
    """Raised when the payload is too large"""

    def __init__(self, message: str):
        super().__init__(message, status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE)


class BadRequestException(BaseAppException):
    """Raised when a bad request is made"""

    def __init__(self, message: str):
        super().__init__(message, status_code=status.HTTP_400_BAD_REQUEST)
