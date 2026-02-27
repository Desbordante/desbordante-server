"""Tests for UserPolicy, organized by actor role."""

from src.domain.authorization.entities import Actor
from tests.unit.infrastructure.authorization.conftest import make_user


class TestAnonymousActorUserPermissions:
    """Anonymous user has no user-related permissions."""

    def test_cannot_read_user_profile(
        self,
        user_policy,
        anonymous_actor: Actor,
    ) -> None:
        """Anonymous user cannot read any user profile."""
        user = make_user(id=1, is_admin=False)
        assert user_policy.can_read(anonymous_actor, user) is False

    def test_cannot_ban_user(
        self,
        user_policy,
        anonymous_actor: Actor,
    ) -> None:
        """Anonymous user cannot ban anyone."""
        user = make_user(id=1, is_admin=False)
        assert user_policy.can_ban(anonymous_actor, user) is False


class TestUserActorUserPermissions:
    """Regular user can only read own profile, cannot ban anyone."""

    def test_can_read_own_profile(
        self,
        user_policy,
        user_actor: Actor,
    ) -> None:
        """User can read their own profile."""
        user = make_user(id=1, is_admin=False)
        assert user_policy.can_read(user_actor, user) is True

    def test_cannot_read_others_profile(
        self,
        user_policy,
        user_actor: Actor,
    ) -> None:
        """User cannot read profiles of other users."""
        user = make_user(id=999, is_admin=False)
        assert user_policy.can_read(user_actor, user) is False

    def test_cannot_ban_anyone(
        self,
        user_policy,
        user_actor: Actor,
    ) -> None:
        """Regular user cannot ban anyone."""
        user = make_user(id=999, is_admin=False)
        assert user_policy.can_ban(user_actor, user) is False


class TestAdminActorUserPermissions:
    """Admin can read any user and ban regular users, but not self or other admins."""

    def test_can_read_any_user(
        self,
        user_policy,
        admin_actor: Actor,
    ) -> None:
        """Admin can read any user profile."""
        user = make_user(id=999, is_admin=False)
        assert user_policy.can_read(admin_actor, user) is True

    def test_can_ban_regular_user(
        self,
        user_policy,
        admin_actor: Actor,
    ) -> None:
        """Admin can ban regular users."""
        user = make_user(id=999, is_admin=False)
        assert user_policy.can_ban(admin_actor, user) is True

    def test_cannot_ban_self(
        self,
        user_policy,
        admin_actor: Actor,
    ) -> None:
        """Admin cannot ban themselves."""
        user = make_user(id=2, is_admin=True)  # same id as admin_actor
        assert user_policy.can_ban(admin_actor, user) is False

    def test_cannot_ban_other_admin(
        self,
        user_policy,
        admin_actor: Actor,
    ) -> None:
        """Admin cannot ban another admin."""
        user = make_user(id=999, is_admin=True)
        assert user_policy.can_ban(admin_actor, user) is False
