from uuid import uuid4

import pytest

from src.crud.dataset_crud import DatasetCrud
from src.exceptions import ResourceNotFoundException
from src.models.dataset_models import DatasetModel
from src.models.user_models import UserModel
from tests.integration.crud.dataset_crud.helpers import make_dataset_entity

pytestmark = pytest.mark.asyncio


async def test_create(
    dataset_crud: DatasetCrud,
    user: UserModel,
) -> None:
    entity = make_dataset_entity(
        owner_id=user.id,
        name="new_dataset.csv",
        size=256,
    )

    created = await dataset_crud.create(entity=entity)

    assert created.id is not None
    assert created.name == "new_dataset.csv"
    assert created.size == 256
    assert created.owner_id == user.id


@pytest.mark.parametrize(
    "filter_keys",
    [
        ["id"],
        ["id", "owner_id"],
        ["id", "type"],
        ["id", "is_public"],
        ["id", "owner_id", "type"],
    ],
)
async def test_get_by(
    dataset_crud: DatasetCrud,
    dataset: DatasetModel,
    filter_keys: list[str],
) -> None:
    kwargs = {key: getattr(dataset, key) for key in filter_keys}
    found = await dataset_crud.get_by(**kwargs)

    assert found.id == dataset.id
    assert found.name == dataset.name
    assert found.owner_id == dataset.owner_id


async def test_get_by_raises_when_not_found(
    dataset_crud: DatasetCrud,
) -> None:
    with pytest.raises(ResourceNotFoundException):
        await dataset_crud.get_by(id=uuid4())


async def test_update(
    dataset_crud: DatasetCrud,
    dataset: DatasetModel,
) -> None:
    assert dataset.is_uploaded is False

    updated = await dataset_crud.update(entity=dataset, is_uploaded=True)

    assert updated.is_uploaded is True
    assert updated.id == dataset.id

    # Verify persistence
    found = await dataset_crud.get_by(id=dataset.id)
    assert found.is_uploaded is True


async def test_delete(
    dataset_crud: DatasetCrud,
    user: UserModel,
) -> None:
    entity = make_dataset_entity(owner_id=user.id)
    created = await dataset_crud.create(entity=entity)

    await dataset_crud.delete(entity=created)

    with pytest.raises(ResourceNotFoundException):
        await dataset_crud.get_by(id=created.id)
