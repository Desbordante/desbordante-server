from src.exceptions import ValidationException


class TokenException(ValidationException):
    def __init__(self, message: str = "Invalid token"):
        super().__init__(message)
