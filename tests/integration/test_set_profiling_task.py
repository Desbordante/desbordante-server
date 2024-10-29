from fastapi.testclient import TestClient
from uuid import UUID, uuid4

from internal.domain.task.value_objects import FdTaskConfig, PrimitiveName
from internal.domain.task.value_objects.fd.algo_name import FdAlgoName
from internal.domain.task.value_objects.fd.algo_config import AidConfig
from internal.infrastructure.data_storage.relational.model.task import TaskORM
from tests.integration.common_requests import upload_csv_dataset, set_task


def test_set_profiling_task(client: TestClient, context):
    dataset_response = upload_csv_dataset(
        client, "university_fd.csv", "text/csv", ".", [0]
    )
    assert dataset_response.status_code == 200
    dataset_id = UUID(dataset_response.json())

    algo_config = AidConfig(algo_name=FdAlgoName.Aid, max_lhs=1)
    task_config = FdTaskConfig(primitive_name=PrimitiveName.fd, config=algo_config)

    response = set_task(client, dataset_id, task_config)

    assert response.status_code == 200

    task_id = UUID(response.json())

    task_data = context.postgres_context.get(TaskORM, task_id)

    assert task_data is not None
    assert task_data.config == task_config.model_dump()
    assert task_data.dataset_id == dataset_id


def test_set_profiling_task_with_non_existent_dataset(client: TestClient):
    dataset_id = uuid4()
    algo_config = AidConfig(algo_name=FdAlgoName.Aid, max_lhs=1)
    task_config = FdTaskConfig(primitive_name=PrimitiveName.fd, config=algo_config)

    response = set_task(client, dataset_id, task_config)

    assert response.status_code == 404
    assert response.json()["detail"] == "Dataset not found"
