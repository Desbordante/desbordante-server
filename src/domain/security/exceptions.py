from src.exceptions import ForbiddenException, ValidationException


class InvalidTokenException(ValidationException):
    def __init__(self):
        super().__init__("Invalid token")


class ExpiredTokenException(ForbiddenException):
    def __init__(self):
        super().__init__("Token has expired")
