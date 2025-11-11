from typing import Protocol

from src.models.user_models import UserModel


class UserCrud(Protocol):
    async def update_is_active(self, *, user_id: int, is_active: bool) -> UserModel: ...


class SessionManager(Protocol):
    async def clear_all_user_sessions(self, *, user_id: int) -> int: ...


class BanUserUseCase:
    def __init__(
        self,
        *,
        user_crud: UserCrud,
        session_manager: SessionManager,
    ):
        self.user_crud = user_crud
        self.session_manager = session_manager

    async def __call__(self, *, user_id: int) -> UserModel:
        """
        Ban user and clear all their active sessions.
        """
        user = await self.user_crud.update_is_active(user_id=user_id, is_active=False)

        await self.session_manager.clear_all_user_sessions(user_id=user_id)

        return user
