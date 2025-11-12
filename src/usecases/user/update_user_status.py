from typing import Protocol

from src.models.user_models import UserModel


class UserCrud(Protocol):
    async def update_is_banned(self, *, user_id: int, is_banned: bool) -> UserModel: ...


class SessionManager(Protocol):
    async def clear_all_user_sessions(self, *, user_id: int) -> int: ...


class UpdateUserStatusUseCase:
    def __init__(
        self,
        *,
        user_crud: UserCrud,
        session_manager: SessionManager,
    ):
        self.user_crud = user_crud
        self.session_manager = session_manager

    async def __call__(self, *, user_id: int, is_banned: bool) -> UserModel:
        """
        Update user status (ban/unban) and clear all their active sessions if banned.
        """
        user = await self.user_crud.update_is_banned(
            user_id=user_id, is_banned=is_banned
        )

        if is_banned:
            await self.session_manager.clear_all_user_sessions(user_id=user_id)

        return user
