import os
import pytest
from fastapi.testclient import TestClient

from uuid import UUID

from internal.infrastructure.data_storage.relational.model.file import DatasetORM
from tests.integration.common_requests import upload_csv_dataset


@pytest.mark.asyncio
async def test_upload_csv_dataset(client: TestClient, context, tmp_upload_dir):
    file_name = "university_fd.csv"
    file_path = f"tests/datasets/{file_name}"
    mime_type = "text/csv"
    separator = ","
    header = [0]

    response = upload_csv_dataset(client, file_name, mime_type, separator, header)

    assert response.status_code == 200

    dataset_id = UUID(response.json())

    data = context.postgres_context.get(DatasetORM, dataset_id)
    assert data is not None
    assert data.id == dataset_id
    assert data.separator == separator
    assert data.header == header
    assert data.related_tasks == []

    file = data.file_metadata
    assert file.original_file_name == "university_fd.csv"
    assert file.mime_type == mime_type

    saved_file_path = os.path.join(tmp_upload_dir, str(file.file_name))
    assert os.path.exists(saved_file_path)

    with open(saved_file_path, "rb") as saved_file, open(
        file_path, "rb"
    ) as original_file:
        saved_file_content = saved_file.read()
        original_file_content = original_file.read()
        assert saved_file_content == original_file_content


@pytest.mark.asyncio
async def test_upload_csv_dataset_with_incorrect_mime_type(client: TestClient):
    file_name = "university.txt"
    mime_type = "text/plain"
    separator = ","
    header = [0]

    response = upload_csv_dataset(client, file_name, mime_type, separator, header)

    assert response.status_code == 400
    assert response.json()["detail"] == "File is not CSV"
