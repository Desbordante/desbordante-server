from src.domain.authorization.entities import Actor
from src.models.user_models import UserModel


class UserPolicy:
    """Access policy for users."""

    def can_read(self, actor: Actor, user: UserModel) -> bool:
        if actor.is_admin:
            return True
        return actor.user_id == user.id

    def can_ban(self, actor: Actor, user: UserModel) -> bool:
        if actor.user_id == user.id:
            return False

        if user.is_admin:
            return False

        return actor.is_admin
