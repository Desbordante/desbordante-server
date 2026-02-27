"""Tests for TaskPolicy, organized by actor role."""

from src.domain.authorization.entities import Actor
from tests.unit.infrastructure.authorization.conftest import make_task


class TestAnonymousActorTaskPermissions:
    """Anonymous user can only read public tasks and create from public tasks."""

    def test_can_read_public_task(
        self,
        task_policy,
        anonymous_actor: Actor,
    ) -> None:
        """Anonymous user can read public tasks."""
        task = make_task(owner_id=1, is_public=True)
        assert task_policy.can_read(anonymous_actor, task) is True

    def test_cannot_read_private_task(
        self,
        task_policy,
        anonymous_actor: Actor,
    ) -> None:
        """Anonymous user cannot read private tasks."""
        task = make_task(owner_id=1, is_public=False)
        assert task_policy.can_read(anonymous_actor, task) is False

    def test_can_create_from_public_task(
        self,
        task_policy,
        anonymous_actor: Actor,
    ) -> None:
        """Anonymous user can create tasks from public tasks."""
        task = make_task(owner_id=1, is_public=True)
        assert task_policy.can_create(anonymous_actor, task) is True

    def test_cannot_create_from_private_task(
        self,
        task_policy,
        anonymous_actor: Actor,
    ) -> None:
        """Anonymous user cannot create tasks from private tasks."""
        task = make_task(owner_id=1, is_public=False)
        assert task_policy.can_create(anonymous_actor, task) is False


class TestUserActorTaskPermissions:
    """Regular user can read public and own tasks, create from own private."""

    def test_can_read_own_task(
        self,
        task_policy,
        user_actor: Actor,
    ) -> None:
        """User can read their own private tasks."""
        task = make_task(owner_id=1, is_public=False)
        assert task_policy.can_read(user_actor, task) is True

    def test_can_read_public_task_of_others(
        self,
        task_policy,
        user_actor: Actor,
    ) -> None:
        """User can read public tasks owned by others."""
        task = make_task(owner_id=999, is_public=True)
        assert task_policy.can_read(user_actor, task) is True

    def test_cannot_read_private_task_of_others(
        self,
        task_policy,
        user_actor: Actor,
    ) -> None:
        """User cannot read private tasks owned by others."""
        task = make_task(owner_id=999, is_public=False)
        assert task_policy.can_read(user_actor, task) is False

    def test_can_create_from_own_private_task(
        self,
        task_policy,
        user_actor: Actor,
    ) -> None:
        """User can create tasks from their own private tasks."""
        task = make_task(owner_id=1, is_public=False)
        assert task_policy.can_create(user_actor, task) is True

    def test_cannot_create_from_own_public_task(
        self,
        task_policy,
        user_actor: Actor,
    ) -> None:
        """User cannot create tasks from their own public tasks."""
        task = make_task(owner_id=1, is_public=True)
        assert task_policy.can_create(user_actor, task) is False

    def test_cannot_create_from_others_task(
        self,
        task_policy,
        user_actor: Actor,
    ) -> None:
        """User cannot create tasks from tasks owned by others."""
        task = make_task(owner_id=999, is_public=False)
        assert task_policy.can_create(user_actor, task) is False


class TestAdminActorTaskPermissions:
    """Admin can do everything with tasks."""

    def test_can_read_any_task(
        self,
        task_policy,
        admin_actor: Actor,
    ) -> None:
        """Admin can read any task including private ones owned by others."""
        task = make_task(owner_id=999, is_public=False)
        assert task_policy.can_read(admin_actor, task) is True

    def test_can_create_from_any_task(
        self,
        task_policy,
        admin_actor: Actor,
    ) -> None:
        """Admin can create tasks from any task context."""
        task = make_task(owner_id=999, is_public=False)
        assert task_policy.can_create(admin_actor, task) is True
