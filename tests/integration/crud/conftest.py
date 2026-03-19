"""Shared fixtures for CRUD tests."""

from datetime import datetime, timedelta, timezone
from uuid import uuid4

import pytest_asyncio
from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession

from src.crud.dataset_crud import DatasetCrud
from src.crud.task_crud import TaskCrud
from src.crud.user_crud import UserCrud
from src.models.dataset_models import DatasetModel
from src.models.user_models import UserModel
from src.schemas.dataset_schemas import DatasetType
from tests.integration.crud.dataset_crud.helpers import make_dataset_entity


@pytest_asyncio.fixture
async def dataset(
    dataset_crud: DatasetCrud,
    user: UserModel,
) -> DatasetModel:
    entity = make_dataset_entity(owner_id=user.id)
    return await dataset_crud.create(entity=entity)


@pytest_asyncio.fixture
async def many_datasets(
    dataset_crud: DatasetCrud,
    user: UserModel,
    second_user: UserModel,
) -> list[DatasetModel]:
    entities = [
        make_dataset_entity(
            owner_id=user.id, name="alpha.csv", size=100, is_public=True
        ),
        make_dataset_entity(
            owner_id=user.id, name="beta.csv", size=200, is_public=False
        ),
        make_dataset_entity(
            owner_id=user.id, name="gamma.csv", size=300, is_public=True
        ),
        make_dataset_entity(
            owner_id=user.id,
            name="delta.csv",
            size=150,
            is_public=False,
            type=DatasetType.TRANSACTIONAL,
        ),
        make_dataset_entity(owner_id=user.id, name="epsilon.csv", size=250),
        make_dataset_entity(owner_id=second_user.id, name="zeta.csv", size=50),
    ]
    created = [await dataset_crud.create(entity=e) for e in entities]
    base = datetime(2025, 1, 1, 12, 0, 0, tzinfo=timezone.utc)
    for i, ds in enumerate(created):
        await dataset_crud._session.execute(
            update(DatasetModel)
            .where(DatasetModel.id == ds.id)
            .values(
                created_at=base + timedelta(seconds=i),
                updated_at=base + timedelta(seconds=i),
            )
        )
    await dataset_crud._session.commit()
    return created


@pytest_asyncio.fixture
async def user(session: AsyncSession) -> UserModel:
    user_crud = UserCrud(session=session)
    return await user_crud.create(UserModel(email=f"test-{uuid4()}@example.com"))


@pytest_asyncio.fixture
async def second_user(session: AsyncSession) -> UserModel:
    user_crud = UserCrud(session=session)
    return await user_crud.create(UserModel(email=f"test-{uuid4()}@example.com"))


@pytest_asyncio.fixture
async def dataset_crud(session: AsyncSession) -> DatasetCrud:
    return DatasetCrud(session=session)


@pytest_asyncio.fixture
async def task_crud(session: AsyncSession) -> TaskCrud:
    return TaskCrud(session=session)
