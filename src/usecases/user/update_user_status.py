from typing import Protocol, cast

from src.domain.authorization.entities import AuthenticatedActor, User
from src.exceptions import ForbiddenException
from src.models.user_models import UserModel


class UserCrud(Protocol):
    async def get_by(self, *, id: int) -> UserModel: ...
    async def update(self, *, entity: UserModel, is_banned: bool) -> UserModel: ...


class SessionManager(Protocol):
    async def destroy_all_user_sessions(self, *, user_id: int) -> None: ...


class UserPolicy(Protocol):
    def can_ban(self, actor: AuthenticatedActor, user: User) -> bool: ...


class UpdateUserStatusUseCase:
    def __init__(
        self,
        *,
        user_crud: UserCrud,
        session_manager: SessionManager,
        user_policy: UserPolicy,
    ):
        self._user_crud = user_crud
        self._session_manager = session_manager
        self._user_policy = user_policy

    async def __call__(
        self, *, actor: AuthenticatedActor, user_id: int, is_banned: bool
    ) -> UserModel:
        """
        Update user status (ban/unban) and clear all their active sessions if banned.
        """
        user = await self._user_crud.get_by(id=user_id)

        if not self._user_policy.can_ban(actor=actor, user=cast(User, user)):
            raise ForbiddenException("Access denied")

        user = await self._user_crud.update(entity=user, is_banned=is_banned)

        if is_banned:
            await self._session_manager.destroy_all_user_sessions(user_id=user_id)

        return user
