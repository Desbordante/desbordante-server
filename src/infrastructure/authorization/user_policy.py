from src.domain.authorization.entities import Actor, User


class UserPolicy:
    """Access policy for users."""

    def can_read(self, actor: Actor, user: User) -> bool:
        if actor.is_admin:
            return True
        return actor.user_id == user.id

    def can_ban(self, actor: Actor, user: User) -> bool:
        if actor.user_id == user.id:
            return False

        if user.is_admin:
            return False

        return actor.is_admin
