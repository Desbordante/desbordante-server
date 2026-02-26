from src.domain.authorization.entities import Actor
from src.models.dataset_models import DatasetModel


class DatasetPolicy:
    """Access policy for datasets."""

    def can_read(self, actor: Actor, dataset: DatasetModel) -> bool:
        if actor.is_admin:
            return True

        return dataset.is_public or dataset.owner_id == actor.user_id

    def can_create(self, actor: Actor, dataset: DatasetModel) -> bool:
        if actor.is_admin:
            return True

        is_anonymous = actor.user_id is None

        if is_anonymous:
            return False

        return dataset.owner_id == actor.user_id and not dataset.is_public

    def can_delete(self, actor: Actor, dataset: DatasetModel) -> bool:
        if actor.is_admin:
            return True

        return dataset.owner_id == actor.user_id
