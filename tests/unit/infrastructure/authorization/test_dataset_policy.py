"""Tests for DatasetPolicy, organized by actor role."""

from src.domain.authorization.entities import Actor
from tests.unit.infrastructure.authorization.conftest import make_dataset


class TestAnonymousActorDatasetPermissions:
    """Anonymous user can only read public datasets."""

    def test_can_read_public_dataset(
        self,
        dataset_policy,
        anonymous_actor: Actor,
    ) -> None:
        """Anonymous user can read public datasets."""
        dataset = make_dataset(owner_id=1, is_public=True)
        assert dataset_policy.can_read(anonymous_actor, dataset) is True

    def test_cannot_read_private_dataset(
        self,
        dataset_policy,
        anonymous_actor: Actor,
    ) -> None:
        """Anonymous user cannot read private datasets."""
        dataset = make_dataset(owner_id=1, is_public=False)
        assert dataset_policy.can_read(anonymous_actor, dataset) is False

    def test_cannot_create_from_dataset(
        self,
        dataset_policy,
        anonymous_actor: Actor,
    ) -> None:
        """Anonymous user cannot create tasks from datasets."""
        dataset = make_dataset(owner_id=1, is_public=True)
        assert dataset_policy.can_create(anonymous_actor, dataset) is False

    def test_cannot_delete_dataset(
        self,
        dataset_policy,
        anonymous_actor: Actor,
    ) -> None:
        """Anonymous user cannot delete datasets."""
        dataset = make_dataset(owner_id=1, is_public=True)
        assert dataset_policy.can_delete(anonymous_actor, dataset) is False


class TestUserActorDatasetPermissions:
    """Regular user can read public and own datasets, create from own private, delete own."""

    def test_can_read_own_dataset(
        self,
        dataset_policy,
        user_actor: Actor,
    ) -> None:
        """User can read their own private datasets."""
        dataset = make_dataset(owner_id=1, is_public=False)
        assert dataset_policy.can_read(user_actor, dataset) is True

    def test_can_read_public_dataset_of_others(
        self,
        dataset_policy,
        user_actor: Actor,
    ) -> None:
        """User can read public datasets owned by others."""
        dataset = make_dataset(owner_id=999, is_public=True)
        assert dataset_policy.can_read(user_actor, dataset) is True

    def test_cannot_read_private_dataset_of_others(
        self,
        dataset_policy,
        user_actor: Actor,
    ) -> None:
        """User cannot read private datasets owned by others."""
        dataset = make_dataset(owner_id=999, is_public=False)
        assert dataset_policy.can_read(user_actor, dataset) is False

    def test_can_create_from_own_private_dataset(
        self,
        dataset_policy,
        user_actor: Actor,
    ) -> None:
        """User can create tasks from their own private datasets."""
        dataset = make_dataset(owner_id=1, is_public=False)
        assert dataset_policy.can_create(user_actor, dataset) is True

    def test_cannot_create_from_own_public_dataset(
        self,
        dataset_policy,
        user_actor: Actor,
    ) -> None:
        """User cannot create tasks from their own public datasets."""
        dataset = make_dataset(owner_id=1, is_public=True)
        assert dataset_policy.can_create(user_actor, dataset) is False

    def test_cannot_create_from_others_dataset(
        self,
        dataset_policy,
        user_actor: Actor,
    ) -> None:
        """User cannot create tasks from datasets owned by others."""
        dataset = make_dataset(owner_id=999, is_public=False)
        assert dataset_policy.can_create(user_actor, dataset) is False

    def test_can_delete_own_dataset(
        self,
        dataset_policy,
        user_actor: Actor,
    ) -> None:
        """User can delete their own datasets."""
        dataset = make_dataset(owner_id=1, is_public=True)
        assert dataset_policy.can_delete(user_actor, dataset) is True

    def test_cannot_delete_others_dataset(
        self,
        dataset_policy,
        user_actor: Actor,
    ) -> None:
        """User cannot delete datasets owned by others."""
        dataset = make_dataset(owner_id=999, is_public=False)
        assert dataset_policy.can_delete(user_actor, dataset) is False


class TestAdminActorDatasetPermissions:
    """Admin can do everything with datasets."""

    def test_can_read_any_dataset(
        self,
        dataset_policy,
        admin_actor: Actor,
    ) -> None:
        """Admin can read any dataset including private ones owned by others."""
        dataset = make_dataset(owner_id=999, is_public=False)
        assert dataset_policy.can_read(admin_actor, dataset) is True

    def test_can_create_from_any_dataset(
        self,
        dataset_policy,
        admin_actor: Actor,
    ) -> None:
        """Admin can create tasks from any dataset."""
        dataset = make_dataset(owner_id=999, is_public=False)
        assert dataset_policy.can_create(admin_actor, dataset) is True

    def test_can_delete_any_dataset(
        self,
        dataset_policy,
        admin_actor: Actor,
    ) -> None:
        """Admin can delete any dataset."""
        dataset = make_dataset(owner_id=999, is_public=False)
        assert dataset_policy.can_delete(admin_actor, dataset) is True
