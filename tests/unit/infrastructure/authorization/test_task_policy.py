"""Tests for TaskPolicy, organized by actor role."""

from src.domain.authorization.entities import Actor

from tests.unit.infrastructure.authorization.constants import (
    ADMIN_USER_ID,
    OTHER_USER_ID,
    USER_ID,
)
from tests.unit.infrastructure.authorization.helpers import make_task


class TestAnonymousActorTaskPermissions:
    """Anonymous user can read public tasks and create public tasks."""

    def test_can_read_public_task(self, task_policy, anonymous_actor: Actor) -> None:
        """Anonymous user can read public tasks."""
        task = make_task(owner_id=USER_ID, is_public=True)
        assert task_policy.can_read(anonymous_actor, task) is True

    def test_cannot_read_private_task(
        self, task_policy, anonymous_actor: Actor
    ) -> None:
        """Anonymous user cannot read private tasks."""
        task = make_task(owner_id=USER_ID, is_public=False)
        assert task_policy.can_read(anonymous_actor, task) is False

    def test_cannot_read_own_task(self, task_policy, anonymous_actor: Actor) -> None:
        """Anonymous user has no own tasks."""
        task = make_task(owner_id=USER_ID, is_public=False)
        assert task_policy.can_read(anonymous_actor, task) is False

    def test_can_read_public_task_of_others(
        self, task_policy, anonymous_actor: Actor
    ) -> None:
        """Anonymous user can read public tasks of others."""
        task = make_task(owner_id=OTHER_USER_ID, is_public=True)
        assert task_policy.can_read(anonymous_actor, task) is True

    def test_cannot_read_private_task_of_others(
        self, task_policy, anonymous_actor: Actor
    ) -> None:
        """Anonymous user cannot read private tasks of others."""
        task = make_task(owner_id=OTHER_USER_ID, is_public=False)
        assert task_policy.can_read(anonymous_actor, task) is False

    def test_cannot_read_any_task(self, task_policy, anonymous_actor: Actor) -> None:
        """Anonymous user cannot read any private task."""
        task = make_task(owner_id=OTHER_USER_ID, is_public=False)
        assert task_policy.can_read(anonymous_actor, task) is False

    def test_cannot_create_task(self, task_policy, anonymous_actor: Actor) -> None:
        """Anonymous user cannot create private tasks."""
        task = make_task(owner_id=USER_ID, is_public=False)
        assert task_policy.can_create(anonymous_actor, task) is False

    def test_cannot_create_private_task(
        self, task_policy, anonymous_actor: Actor
    ) -> None:
        """Anonymous user cannot create private tasks."""
        task = make_task(owner_id=USER_ID, is_public=False)
        assert task_policy.can_create(anonymous_actor, task) is False

    def test_can_create_public_task(self, task_policy, anonymous_actor: Actor) -> None:
        """Anonymous user can create public tasks."""
        task = make_task(owner_id=USER_ID, is_public=True)
        assert task_policy.can_create(anonymous_actor, task) is True

    def test_cannot_create_task_for_others(
        self, task_policy, anonymous_actor: Actor
    ) -> None:
        """Anonymous user cannot create tasks for others."""
        task = make_task(owner_id=OTHER_USER_ID, is_public=False)
        assert task_policy.can_create(anonymous_actor, task) is False


class TestUserActorTaskPermissions:
    """Regular user can read public and own tasks, create private tasks."""

    def test_can_read_public_task(self, task_policy, user_actor: Actor) -> None:
        """User can read public tasks."""
        task = make_task(owner_id=USER_ID, is_public=True)
        assert task_policy.can_read(user_actor, task) is True

    def test_cannot_read_private_task(self, task_policy, user_actor: Actor) -> None:
        """User cannot read private tasks of others."""
        task = make_task(owner_id=OTHER_USER_ID, is_public=False)
        assert task_policy.can_read(user_actor, task) is False

    def test_can_read_own_task(self, task_policy, user_actor: Actor) -> None:
        """User can read their own private tasks."""
        task = make_task(owner_id=USER_ID, is_public=False)
        assert task_policy.can_read(user_actor, task) is True

    def test_can_read_public_task_of_others(
        self, task_policy, user_actor: Actor
    ) -> None:
        """User can read public tasks of others."""
        task = make_task(owner_id=OTHER_USER_ID, is_public=True)
        assert task_policy.can_read(user_actor, task) is True

    def test_cannot_read_private_task_of_others(
        self, task_policy, user_actor: Actor
    ) -> None:
        """User cannot read private tasks of others."""
        task = make_task(owner_id=OTHER_USER_ID, is_public=False)
        assert task_policy.can_read(user_actor, task) is False

    def test_cannot_read_any_task(self, task_policy, user_actor: Actor) -> None:
        """User cannot read any private task of others."""
        task = make_task(owner_id=OTHER_USER_ID, is_public=False)
        assert task_policy.can_read(user_actor, task) is False

    def test_cannot_create_task(self, task_policy, user_actor: Actor) -> None:
        """User cannot create public tasks."""
        task = make_task(owner_id=USER_ID, is_public=True)
        assert task_policy.can_create(user_actor, task) is False

    def test_can_create_private_task(self, task_policy, user_actor: Actor) -> None:
        """User can create private tasks."""
        task = make_task(owner_id=USER_ID, is_public=False)
        assert task_policy.can_create(user_actor, task) is True

    def test_cannot_create_public_task(self, task_policy, user_actor: Actor) -> None:
        """User cannot create public tasks."""
        task = make_task(owner_id=USER_ID, is_public=True)
        assert task_policy.can_create(user_actor, task) is False

    def test_cannot_create_task_for_others(
        self, task_policy, user_actor: Actor
    ) -> None:
        """User cannot create tasks for others."""
        task = make_task(owner_id=OTHER_USER_ID, is_public=False)
        assert task_policy.can_create(user_actor, task) is False


class TestAdminActorTaskPermissions:
    """Admin can do everything with tasks."""

    def test_can_read_public_task(self, task_policy, admin_actor: Actor) -> None:
        """Admin can read public tasks."""
        task = make_task(owner_id=USER_ID, is_public=True)
        assert task_policy.can_read(admin_actor, task) is True

    def test_can_read_private_task(self, task_policy, admin_actor: Actor) -> None:
        """Admin can read private tasks of others."""
        task = make_task(owner_id=OTHER_USER_ID, is_public=False)
        assert task_policy.can_read(admin_actor, task) is True

    def test_can_read_own_task(self, task_policy, admin_actor: Actor) -> None:
        """Admin can read their own tasks."""
        task = make_task(owner_id=ADMIN_USER_ID, is_public=False)
        assert task_policy.can_read(admin_actor, task) is True

    def test_can_read_public_task_of_others(
        self, task_policy, admin_actor: Actor
    ) -> None:
        """Admin can read public tasks of others."""
        task = make_task(owner_id=OTHER_USER_ID, is_public=True)
        assert task_policy.can_read(admin_actor, task) is True

    def test_can_read_private_task_of_others(
        self, task_policy, admin_actor: Actor
    ) -> None:
        """Admin can read private tasks of others."""
        task = make_task(owner_id=OTHER_USER_ID, is_public=False)
        assert task_policy.can_read(admin_actor, task) is True

    def test_can_read_any_task(self, task_policy, admin_actor: Actor) -> None:
        """Admin can read any task."""
        task = make_task(owner_id=OTHER_USER_ID, is_public=False)
        assert task_policy.can_read(admin_actor, task) is True

    def test_can_create_task(self, task_policy, admin_actor: Actor) -> None:
        """Admin can create tasks for self."""
        task = make_task(owner_id=ADMIN_USER_ID, is_public=False)
        assert task_policy.can_create(admin_actor, task) is True

    def test_can_create_private_task(self, task_policy, admin_actor: Actor) -> None:
        """Admin can create private tasks."""
        task = make_task(owner_id=ADMIN_USER_ID, is_public=False)
        assert task_policy.can_create(admin_actor, task) is True

    def test_can_create_public_task(self, task_policy, admin_actor: Actor) -> None:
        """Admin can create public tasks."""
        task = make_task(owner_id=ADMIN_USER_ID, is_public=True)
        assert task_policy.can_create(admin_actor, task) is True

    def test_cannot_create_task_for_others(
        self, task_policy, admin_actor: Actor
    ) -> None:
        """Admin cannot create tasks for others."""
        task = make_task(owner_id=OTHER_USER_ID, is_public=False)
        assert task_policy.can_create(admin_actor, task) is False
