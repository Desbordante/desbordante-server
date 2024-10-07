from fastapi.testclient import TestClient
from uuid import UUID, uuid4

from internal.infrastructure.data_storage.relational.model.file import DatasetORM
from tests.integration.common_requests import upload_csv_dataset


def test_retrieve_dataset(client: TestClient, context):
    file_name = "university_fd.csv"
    mime_type = "text/csv"
    separator = ","
    header = [0]

    response = upload_csv_dataset(client, file_name, mime_type, separator, header)
    assert response.status_code == 200

    dataset_id = UUID(response.json())

    response = client.post(f"api/file/dataset/{dataset_id}")

    assert response.status_code == 200

    response_data = response.json()
    assert response_data["id"] == str(dataset_id)

    dataset = context.postgres_context.get(DatasetORM, dataset_id)
    assert dataset is not None
    assert response_data["file_id"] == str(dataset.file_id)
    assert response_data["separator"] == dataset.separator
    assert response_data["header"] == dataset.header


def test_retrieve_non_existent_dataset(client: TestClient):
    dataset_id = uuid4()  # non existen dataset

    response = client.post(f"api/file/dataset/{dataset_id}")

    assert response.status_code == 404
    assert response.json()["detail"] == "Dataset not found"
