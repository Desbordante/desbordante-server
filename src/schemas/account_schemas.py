from src.schemas.security_schemas import TokenPayloadSchema


class EmailTokenPayloadSchema(TokenPayloadSchema):
    email: str


class ConfirmationTokenPayloadSchema(EmailTokenPayloadSchema):
    type: str = "confirmation"
