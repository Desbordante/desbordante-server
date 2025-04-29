from src.domain.account.tasks import send_confirmation_email
from src.models.user_models import UserModel


class SendConfirmationEmailUseCase:
    def __init__(
        self,
        *,
        user: UserModel,
    ):
        self.user = user

    async def __call__(self) -> None:
        send_confirmation_email.delay(to_email=self.user.email)
