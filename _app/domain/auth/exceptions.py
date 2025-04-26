from _app.exceptions import UnauthorizedException
from _app.exceptions.exceptions import ForbiddenException


class IncorrectCredentialsException(UnauthorizedException):
    def __init__(self):
        super().__init__("Incorrect username or password")


class CredentialsException(UnauthorizedException):
    def __init__(self):
        super().__init__("Could not validate credentials")


class NotAdminException(ForbiddenException):
    def __init__(self):
        super().__init__("Access denied")
