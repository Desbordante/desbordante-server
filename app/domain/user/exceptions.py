from app.exceptions import (
    ValidationException,
    ResourceNotFoundException,
)


class UserNotFoundException(ResourceNotFoundException):
    def __init__(self, field: str, value: str):
        super().__init__(f"User with {field} {value} not found")


class UserAlreadyExistsException(ValidationException):
    def __init__(self, email: str):
        super().__init__(f"User with email {email} already exists")
