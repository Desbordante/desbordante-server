import time
from fastapi.testclient import TestClient
from uuid import UUID, uuid4

from internal.domain.task.value_objects import FdTaskConfig, PrimitiveName
from internal.domain.task.value_objects.fd.algo_name import FdAlgoName
from internal.domain.task.value_objects.fd.algo_config import AidConfig
from internal.infrastructure.data_storage.relational.model.task import TaskORM
from tests.integration.common_requests import upload_csv_dataset, set_task


def test_retrieve_task(client: TestClient, context):
    dataset_response = upload_csv_dataset(
        client, "university_fd.csv", "text/csv", ".", [0]
    )
    assert dataset_response.status_code == 200
    dataset_id = UUID(dataset_response.json())

    algo_config = AidConfig(algo_name=FdAlgoName.Aid, max_lhs=1)
    task_config = FdTaskConfig(primitive_name=PrimitiveName.fd, config=algo_config)

    task_response = set_task(client, dataset_id, task_config)
    assert task_response.status_code == 200
    task_id = UUID(task_response.json())

    time.sleep(1)

    response = client.get(f"api/task/{task_id}")
    assert response.status_code == 200

    response_data = response.json()
    assert response_data["dataset_id"] == str(dataset_id)

    task = context.postgres_context.get(TaskORM, task_id)
    assert task is not None
    assert response_data["dataset_id"] == str(task.dataset_id)
    assert response_data["status"] == task.status
    assert response_data["config"] == task.config
    assert response_data["result"] == task.result
    assert response_data["raised_exception_name"] == task.raised_exception_name
    assert response_data["failure_reason"] == task.failure_reason
    assert response_data["traceback"] == task.traceback

    if response_data["status"] == "completed":
        assert response_data["result"] is not None
    if response_data["status"] == "failure":
        assert response_data["raised_exception_name"] is not None
        assert response_data["failure_reason"] is not None
        assert response_data["traceback"] is not None


def test_retrieve_non_existent_task(client: TestClient):
    task_id = uuid4()  # non existen task

    response = client.get(f"api/task/{task_id}")

    assert response.status_code == 404
    assert response.json()["detail"] == "Task not found"
