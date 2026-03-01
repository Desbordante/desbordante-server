import re

import pytest

from src.exceptions import (
    ConflictException,
    ForbiddenException,
    PayloadTooLargeException,
)
from src.schemas.dataset_schemas import DatasetStatus, DatasetType
from src.usecases.dataset.upload_dataset import UploadDatasetUseCase
from tests.unit.usecases.dataset.constants import (
    FAKE_FILE_NAME,
    FAKE_FILE_SIZE,
    FAKE_USER_ID,
    FORBIDDEN_CREATE_DATASET_MESSAGE,
    PAYLOAD_TOO_LARGE_MESSAGE,
    STORAGE_LIMIT,
    STORAGE_LIMIT_REACHED_MESSAGE,
)

pytestmark = pytest.mark.asyncio


async def test_upload_dataset_success(
    upload_dataset_use_case: UploadDatasetUseCase,
    dataset_crud_mock,
    storage_mock,
    actor,
    file,
    upload_params,
    created_dataset,
) -> None:
    result = await upload_dataset_use_case(
        actor=actor,
        file=file,
        params=upload_params,
        is_public=False,
    )

    assert result == created_dataset
    dataset_crud_mock.create_with_storage_check.assert_awaited_once()
    storage_mock.upload.assert_awaited_once()
    dataset_crud_mock.update.assert_awaited_once_with(
        entity=created_dataset, status=DatasetStatus.READY
    )
    dataset_crud_mock.delete.assert_not_called()


async def test_upload_dataset_raises_payload_too_large_when_file_exceeds_limit(
    upload_dataset_use_case: UploadDatasetUseCase,
    dataset_crud_mock,
    storage_mock,
    actor,
    file,
    upload_params,
) -> None:
    file.size = STORAGE_LIMIT + 1

    with pytest.raises(PayloadTooLargeException) as exc_info:
        await upload_dataset_use_case(
            actor=actor,
            file=file,
            params=upload_params,
            is_public=False,
        )

    assert exc_info.value.detail == PAYLOAD_TOO_LARGE_MESSAGE
    dataset_crud_mock.create_with_storage_check.assert_not_called()
    storage_mock.upload.assert_not_called()


async def test_upload_dataset_raises_conflict_when_storage_limit_reached(
    upload_dataset_use_case: UploadDatasetUseCase,
    dataset_crud_mock,
    storage_mock,
    actor,
    file,
    upload_params,
) -> None:
    dataset_crud_mock.create_with_storage_check.side_effect = ConflictException(
        STORAGE_LIMIT_REACHED_MESSAGE
    )

    with pytest.raises(ConflictException) as exc_info:
        await upload_dataset_use_case(
            actor=actor,
            file=file,
            params=upload_params,
            is_public=False,
        )

    assert exc_info.value.detail == STORAGE_LIMIT_REACHED_MESSAGE
    dataset_crud_mock.create_with_storage_check.assert_awaited_once()
    storage_mock.upload.assert_not_called()


async def test_upload_dataset_raises_forbidden_when_policy_denies(
    upload_dataset_use_case: UploadDatasetUseCase,
    dataset_crud_mock,
    dataset_policy_mock,
    actor,
    file,
    upload_params,
) -> None:
    dataset_policy_mock.can_create.return_value = False

    with pytest.raises(ForbiddenException) as exc_info:
        await upload_dataset_use_case(
            actor=actor,
            file=file,
            params=upload_params,
            is_public=False,
        )

    assert exc_info.value.detail == FORBIDDEN_CREATE_DATASET_MESSAGE
    dataset_crud_mock.create_with_storage_check.assert_not_called()


async def test_upload_dataset_deletes_created_dataset_when_storage_upload_fails(
    upload_dataset_use_case: UploadDatasetUseCase,
    dataset_crud_mock,
    storage_mock,
    actor,
    file,
    upload_params,
    created_dataset,
) -> None:
    storage_mock.upload.side_effect = Exception("Storage unavailable")

    with pytest.raises(Exception):
        await upload_dataset_use_case(
            actor=actor,
            file=file,
            params=upload_params,
            is_public=False,
        )

    dataset_crud_mock.delete.assert_awaited_once_with(entity=created_dataset)
    dataset_crud_mock.update.assert_not_called()


async def test_upload_dataset_creates_entity_with_correct_data(
    upload_dataset_use_case: UploadDatasetUseCase,
    dataset_crud_mock,
    storage_mock,
    actor,
    file,
    upload_params,
) -> None:
    await upload_dataset_use_case(
        actor=actor,
        file=file,
        params=upload_params,
        is_public=True,
    )

    call_args = dataset_crud_mock.create_with_storage_check.await_args
    entity = call_args.kwargs["entity"]
    assert call_args.kwargs["user_id"] == FAKE_USER_ID
    assert call_args.kwargs["storage_limit"] == STORAGE_LIMIT
    assert entity.type == DatasetType.TABULAR
    assert entity.name == FAKE_FILE_NAME
    assert entity.size == FAKE_FILE_SIZE
    assert entity.owner_id == FAKE_USER_ID
    assert entity.is_public is True
    assert re.match(rf"^{FAKE_USER_ID}/[0-9a-f-]{{36}}$", entity.path)
    assert "has_header" in entity.params
    assert "separator" in entity.params
    assert "type" not in entity.params


async def test_upload_dataset_calls_storage_upload_with_correct_path(
    upload_dataset_use_case: UploadDatasetUseCase,
    dataset_crud_mock,
    storage_mock,
    actor,
    file,
    upload_params,
) -> None:
    await upload_dataset_use_case(
        actor=actor,
        file=file,
        params=upload_params,
        is_public=False,
    )

    create_entity = dataset_crud_mock.create_with_storage_check.await_args.kwargs[
        "entity"
    ]
    storage_mock.upload.assert_awaited_once_with(
        file=file,
        path=create_entity.path,
    )
