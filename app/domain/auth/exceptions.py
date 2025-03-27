from app.exceptions import UnauthorizedException
from app.exceptions.exceptions import ForbiddenException


class IncorrectCredentialsException(UnauthorizedException):
    def __init__(self):
        super().__init__("Incorrect username or password")


class CredentialsException(UnauthorizedException):
    def __init__(self):
        super().__init__("Could not validate credentials")


class NotAdminException(ForbiddenException):
    def __init__(self):
        super().__init__("Access denied")
