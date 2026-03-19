from uuid import uuid4

import pytest

from src.crud.dataset_crud import DatasetCrud
from src.exceptions import ConflictException
from src.models.dataset_models import DatasetModel
from src.models.user_models import UserModel

from tests.integration.crud.dataset_crud.helpers import make_dataset_entity

pytestmark = pytest.mark.asyncio


async def test_get_stats_empty_user(
    dataset_crud: DatasetCrud,
    user: UserModel,
) -> None:
    stats = await dataset_crud.get_stats(user_id=user.id)

    assert stats.total_count == 0
    assert stats.total_size == 0


async def test_get_stats_single_dataset(
    dataset_crud: DatasetCrud,
    dataset: DatasetModel,
) -> None:
    stats = await dataset_crud.get_stats(user_id=dataset.owner_id)

    assert stats.total_count == 1
    assert stats.total_size == dataset.size


async def test_get_stats_multiple_datasets(
    dataset_crud: DatasetCrud,
    user: UserModel,
) -> None:
    entity1 = make_dataset_entity(owner_id=user.id, size=100)
    entity2 = make_dataset_entity(owner_id=user.id, size=200)
    await dataset_crud.create(entity=entity1)
    await dataset_crud.create(entity=entity2)

    stats = await dataset_crud.get_stats(user_id=user.id)

    assert stats.total_count == 2
    assert stats.total_size == 300


async def test_get_stats_ignores_other_users_datasets(
    dataset_crud: DatasetCrud,
    user: UserModel,
) -> None:
    entity = make_dataset_entity(owner_id=user.id, size=500)
    await dataset_crud.create(entity=entity)

    # User with other id has no datasets
    stats = await dataset_crud.get_stats(user_id=user.id + 999)

    assert stats.total_count == 0
    assert stats.total_size == 0


async def test_create_with_storage_check_success_when_under_limit(
    dataset_crud: DatasetCrud,
    user: UserModel,
) -> None:
    entity = make_dataset_entity(owner_id=user.id, size=50)
    storage_limit = 1000

    created = await dataset_crud.create_with_storage_check(
        entity=entity,
        user_id=user.id,
        storage_limit=storage_limit,
    )

    assert created.id is not None
    assert created.size == 50


async def test_create_with_storage_check_success_when_exactly_at_limit(
    dataset_crud: DatasetCrud,
    user: UserModel,
) -> None:
    entity = make_dataset_entity(owner_id=user.id, size=100)
    storage_limit = 100

    created = await dataset_crud.create_with_storage_check(
        entity=entity,
        user_id=user.id,
        storage_limit=storage_limit,
    )

    assert created.id is not None
    assert created.size == 100


async def test_create_with_storage_check_raises_when_over_limit(
    dataset_crud: DatasetCrud,
    user: UserModel,
) -> None:
    existing = make_dataset_entity(owner_id=user.id, size=80)
    await dataset_crud.create(entity=existing)

    new_entity = make_dataset_entity(owner_id=user.id, size=50)
    storage_limit = 100

    with pytest.raises(ConflictException) as exc_info:
        await dataset_crud.create_with_storage_check(
            entity=new_entity,
            user_id=user.id,
            storage_limit=storage_limit,
        )

    assert "Storage limit reached" in str(exc_info.value)


async def test_get_by_ids_empty_list(
    dataset_crud: DatasetCrud,
    dataset: DatasetModel,
) -> None:
    result = await dataset_crud.get_by_ids(ids=[])

    assert result == []


async def test_get_by_ids_single_id(
    dataset_crud: DatasetCrud,
    dataset: DatasetModel,
) -> None:
    result = await dataset_crud.get_by_ids(ids=[dataset.id])

    assert len(result) == 1
    assert result[0].id == dataset.id


async def test_get_by_ids_multiple_ids(
    dataset_crud: DatasetCrud,
    user: UserModel,
) -> None:
    entity1 = make_dataset_entity(owner_id=user.id, name="a.csv")
    entity2 = make_dataset_entity(owner_id=user.id, name="b.csv")
    created1 = await dataset_crud.create(entity=entity1)
    created2 = await dataset_crud.create(entity=entity2)

    result = await dataset_crud.get_by_ids(ids=[created1.id, created2.id])

    assert len(result) == 2
    ids = {d.id for d in result}
    assert ids == {created1.id, created2.id}


async def test_get_by_ids_skips_non_existent(
    dataset_crud: DatasetCrud,
    dataset: DatasetModel,
) -> None:
    fake_id = uuid4()
    result = await dataset_crud.get_by_ids(ids=[dataset.id, fake_id])

    assert len(result) == 1
    assert result[0].id == dataset.id


async def test_get_by_ids_with_owner_filter(
    dataset_crud: DatasetCrud,
    user: UserModel,
) -> None:
    entity = make_dataset_entity(owner_id=user.id)
    created = await dataset_crud.create(entity=entity)

    result = await dataset_crud.get_by_ids(
        ids=[created.id],
        owner_id=user.id,
    )

    assert len(result) == 1
    assert result[0].id == created.id


async def test_get_by_ids_with_owner_filter_excludes_other_owner(
    dataset_crud: DatasetCrud,
    user: UserModel,
) -> None:
    entity = make_dataset_entity(owner_id=user.id)
    created = await dataset_crud.create(entity=entity)

    result = await dataset_crud.get_by_ids(
        ids=[created.id],
        owner_id=user.id + 999,
    )

    assert result == []
