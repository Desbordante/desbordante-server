from src.exceptions import UnauthorizedException


class IncorrectCredentialsException(UnauthorizedException):
    def __init__(self):
        super().__init__("Incorrect username or password")


class CredentialsException(UnauthorizedException):
    def __init__(self):
        super().__init__("Could not validate credentials")
