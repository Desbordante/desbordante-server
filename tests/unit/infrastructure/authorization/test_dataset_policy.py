"""Tests for DatasetPolicy, organized by actor role."""

from src.domain.authorization.entities import Actor

from tests.unit.infrastructure.authorization.constants import (
    ADMIN_USER_ID,
    OTHER_USER_ID,
    USER_ID,
)
from tests.unit.infrastructure.authorization.helpers import make_dataset


class TestAnonymousActorDatasetPermissions:
    """Anonymous user can only read public datasets."""

    def test_can_read_public_dataset(
        self, dataset_policy, anonymous_actor: Actor
    ) -> None:
        """Anonymous user can read public datasets."""
        dataset = make_dataset(owner_id=USER_ID, is_public=True)
        assert dataset_policy.can_read(anonymous_actor, dataset) is True

    def test_cannot_read_private_dataset(
        self, dataset_policy, anonymous_actor: Actor
    ) -> None:
        """Anonymous user cannot read private datasets."""
        dataset = make_dataset(owner_id=USER_ID, is_public=False)
        assert dataset_policy.can_read(anonymous_actor, dataset) is False

    def test_cannot_read_own_dataset(
        self, dataset_policy, anonymous_actor: Actor
    ) -> None:
        """Anonymous user has no own datasets."""
        dataset = make_dataset(owner_id=USER_ID, is_public=False)
        assert dataset_policy.can_read(anonymous_actor, dataset) is False

    def test_can_read_public_dataset_of_others(
        self, dataset_policy, anonymous_actor: Actor
    ) -> None:
        """Anonymous user can read public datasets of others."""
        dataset = make_dataset(owner_id=OTHER_USER_ID, is_public=True)
        assert dataset_policy.can_read(anonymous_actor, dataset) is True

    def test_cannot_read_private_dataset_of_others(
        self, dataset_policy, anonymous_actor: Actor
    ) -> None:
        """Anonymous user cannot read private datasets of others."""
        dataset = make_dataset(owner_id=OTHER_USER_ID, is_public=False)
        assert dataset_policy.can_read(anonymous_actor, dataset) is False

    def test_cannot_read_any_dataset(
        self, dataset_policy, anonymous_actor: Actor
    ) -> None:
        """Anonymous user cannot read any private dataset."""
        dataset = make_dataset(owner_id=OTHER_USER_ID, is_public=False)
        assert dataset_policy.can_read(anonymous_actor, dataset) is False

    def test_cannot_upload_dataset(
        self, dataset_policy, anonymous_actor: Actor
    ) -> None:
        """Anonymous user cannot upload datasets."""
        dataset = make_dataset(owner_id=USER_ID, is_public=True)
        assert dataset_policy.can_create(anonymous_actor, dataset) is False

    def test_cannot_upload_private_dataset(
        self, dataset_policy, anonymous_actor: Actor
    ) -> None:
        """Anonymous user cannot upload private datasets."""
        dataset = make_dataset(owner_id=USER_ID, is_public=False)
        assert dataset_policy.can_create(anonymous_actor, dataset) is False

    def test_cannot_upload_public_dataset(
        self, dataset_policy, anonymous_actor: Actor
    ) -> None:
        """Anonymous user cannot upload public datasets."""
        dataset = make_dataset(owner_id=USER_ID, is_public=True)
        assert dataset_policy.can_create(anonymous_actor, dataset) is False

    def test_cannot_upload_dataset_for_others(
        self, dataset_policy, anonymous_actor: Actor
    ) -> None:
        """Anonymous user cannot upload datasets for others."""
        dataset = make_dataset(owner_id=OTHER_USER_ID, is_public=False)
        assert dataset_policy.can_create(anonymous_actor, dataset) is False

    def test_cannot_delete_own_dataset(
        self, dataset_policy, anonymous_actor: Actor
    ) -> None:
        """Anonymous user cannot delete datasets."""
        dataset = make_dataset(owner_id=USER_ID, is_public=True)
        assert dataset_policy.can_delete(anonymous_actor, dataset) is False

    def test_cannot_delete_others_dataset(
        self, dataset_policy, anonymous_actor: Actor
    ) -> None:
        """Anonymous user cannot delete datasets of others."""
        dataset = make_dataset(owner_id=OTHER_USER_ID, is_public=False)
        assert dataset_policy.can_delete(anonymous_actor, dataset) is False

    def test_cannot_delete_any_dataset(
        self, dataset_policy, anonymous_actor: Actor
    ) -> None:
        """Anonymous user cannot delete any dataset."""
        dataset = make_dataset(owner_id=OTHER_USER_ID, is_public=False)
        assert dataset_policy.can_delete(anonymous_actor, dataset) is False


class TestUserActorDatasetPermissions:
    """Regular user can read public and own datasets, upload private, delete own."""

    def test_can_read_public_dataset(self, dataset_policy, user_actor: Actor) -> None:
        """User can read public datasets."""
        dataset = make_dataset(owner_id=USER_ID, is_public=True)
        assert dataset_policy.can_read(user_actor, dataset) is True

    def test_cannot_read_private_dataset(
        self, dataset_policy, user_actor: Actor
    ) -> None:
        """User cannot read private datasets of others."""
        dataset = make_dataset(owner_id=OTHER_USER_ID, is_public=False)
        assert dataset_policy.can_read(user_actor, dataset) is False

    def test_can_read_own_dataset(self, dataset_policy, user_actor: Actor) -> None:
        """User can read their own private datasets."""
        dataset = make_dataset(owner_id=USER_ID, is_public=False)
        assert dataset_policy.can_read(user_actor, dataset) is True

    def test_can_read_public_dataset_of_others(
        self, dataset_policy, user_actor: Actor
    ) -> None:
        """User can read public datasets owned by others."""
        dataset = make_dataset(owner_id=OTHER_USER_ID, is_public=True)
        assert dataset_policy.can_read(user_actor, dataset) is True

    def test_cannot_read_private_dataset_of_others(
        self, dataset_policy, user_actor: Actor
    ) -> None:
        """User cannot read private datasets owned by others."""
        dataset = make_dataset(owner_id=OTHER_USER_ID, is_public=False)
        assert dataset_policy.can_read(user_actor, dataset) is False

    def test_cannot_read_any_dataset(self, dataset_policy, user_actor: Actor) -> None:
        """User cannot read any private dataset of others."""
        dataset = make_dataset(owner_id=OTHER_USER_ID, is_public=False)
        assert dataset_policy.can_read(user_actor, dataset) is False

    def test_cannot_upload_dataset(self, dataset_policy, user_actor: Actor) -> None:
        """User cannot upload public datasets."""
        dataset = make_dataset(owner_id=USER_ID, is_public=True)
        assert dataset_policy.can_create(user_actor, dataset) is False

    def test_can_upload_private_dataset(
        self, dataset_policy, user_actor: Actor
    ) -> None:
        """User can upload private datasets."""
        dataset = make_dataset(owner_id=USER_ID, is_public=False)
        assert dataset_policy.can_create(user_actor, dataset) is True

    def test_cannot_upload_public_dataset(
        self, dataset_policy, user_actor: Actor
    ) -> None:
        """User cannot upload public datasets (admin only)."""
        dataset = make_dataset(owner_id=USER_ID, is_public=True)
        assert dataset_policy.can_create(user_actor, dataset) is False

    def test_cannot_upload_dataset_for_others(
        self, dataset_policy, user_actor: Actor
    ) -> None:
        """User cannot upload datasets for others."""
        dataset = make_dataset(owner_id=OTHER_USER_ID, is_public=False)
        assert dataset_policy.can_create(user_actor, dataset) is False

    def test_can_delete_own_dataset(self, dataset_policy, user_actor: Actor) -> None:
        """User can delete their own datasets."""
        dataset = make_dataset(owner_id=USER_ID, is_public=True)
        assert dataset_policy.can_delete(user_actor, dataset) is True

    def test_cannot_delete_others_dataset(
        self, dataset_policy, user_actor: Actor
    ) -> None:
        """User cannot delete datasets owned by others."""
        dataset = make_dataset(owner_id=OTHER_USER_ID, is_public=False)
        assert dataset_policy.can_delete(user_actor, dataset) is False

    def test_cannot_delete_any_dataset(self, dataset_policy, user_actor: Actor) -> None:
        """User cannot delete any dataset of others."""
        dataset = make_dataset(owner_id=OTHER_USER_ID, is_public=False)
        assert dataset_policy.can_delete(user_actor, dataset) is False


class TestAdminActorDatasetPermissions:
    """Admin can read/delete any dataset, upload only for self."""

    def test_can_read_public_dataset(self, dataset_policy, admin_actor: Actor) -> None:
        """Admin can read public datasets."""
        dataset = make_dataset(owner_id=USER_ID, is_public=True)
        assert dataset_policy.can_read(admin_actor, dataset) is True

    def test_can_read_private_dataset(self, dataset_policy, admin_actor: Actor) -> None:
        """Admin can read private datasets of others."""
        dataset = make_dataset(owner_id=OTHER_USER_ID, is_public=False)
        assert dataset_policy.can_read(admin_actor, dataset) is True

    def test_can_read_own_dataset(self, dataset_policy, admin_actor: Actor) -> None:
        """Admin can read their own datasets."""
        dataset = make_dataset(owner_id=ADMIN_USER_ID, is_public=False)
        assert dataset_policy.can_read(admin_actor, dataset) is True

    def test_can_read_public_dataset_of_others(
        self, dataset_policy, admin_actor: Actor
    ) -> None:
        """Admin can read public datasets of others."""
        dataset = make_dataset(owner_id=OTHER_USER_ID, is_public=True)
        assert dataset_policy.can_read(admin_actor, dataset) is True

    def test_can_read_private_dataset_of_others(
        self, dataset_policy, admin_actor: Actor
    ) -> None:
        """Admin can read private datasets of others."""
        dataset = make_dataset(owner_id=OTHER_USER_ID, is_public=False)
        assert dataset_policy.can_read(admin_actor, dataset) is True

    def test_can_read_any_dataset(self, dataset_policy, admin_actor: Actor) -> None:
        """Admin can read any dataset."""
        dataset = make_dataset(owner_id=OTHER_USER_ID, is_public=False)
        assert dataset_policy.can_read(admin_actor, dataset) is True

    def test_can_upload_dataset(self, dataset_policy, admin_actor: Actor) -> None:
        """Admin can upload datasets for self."""
        dataset = make_dataset(owner_id=ADMIN_USER_ID, is_public=True)
        assert dataset_policy.can_create(admin_actor, dataset) is True

    def test_can_upload_private_dataset(
        self, dataset_policy, admin_actor: Actor
    ) -> None:
        """Admin can upload private datasets for self."""
        dataset = make_dataset(owner_id=ADMIN_USER_ID, is_public=False)
        assert dataset_policy.can_create(admin_actor, dataset) is True

    def test_can_upload_public_dataset(
        self, dataset_policy, admin_actor: Actor
    ) -> None:
        """Admin can upload public datasets for self."""
        dataset = make_dataset(owner_id=ADMIN_USER_ID, is_public=True)
        assert dataset_policy.can_create(admin_actor, dataset) is True

    def test_cannot_upload_dataset_for_others(
        self, dataset_policy, admin_actor: Actor
    ) -> None:
        """Admin cannot upload datasets for others."""
        dataset = make_dataset(owner_id=OTHER_USER_ID, is_public=False)
        assert dataset_policy.can_create(admin_actor, dataset) is False

    def test_can_delete_own_dataset(self, dataset_policy, admin_actor: Actor) -> None:
        """Admin can delete their own datasets."""
        dataset = make_dataset(owner_id=ADMIN_USER_ID, is_public=True)
        assert dataset_policy.can_delete(admin_actor, dataset) is True

    def test_can_delete_others_dataset(
        self, dataset_policy, admin_actor: Actor
    ) -> None:
        """Admin can delete datasets of others."""
        dataset = make_dataset(owner_id=OTHER_USER_ID, is_public=False)
        assert dataset_policy.can_delete(admin_actor, dataset) is True

    def test_can_delete_any_dataset(self, dataset_policy, admin_actor: Actor) -> None:
        """Admin can delete any dataset."""
        dataset = make_dataset(owner_id=OTHER_USER_ID, is_public=False)
        assert dataset_policy.can_delete(admin_actor, dataset) is True
