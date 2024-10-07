import os


def has_import_from(file_path, module_name):
    """Checks whether the specified module is imported in the file."""
    with open(file_path, "r") as f:
        for line in f:
            if f"import {module_name}" in line or f"from {module_name}" in line:
                return True
    return False


def check_dependencies(module_path):
    depends_on_domain = False
    depends_on_usecase = False
    depends_on_dto = False
    depends_on_infrastructure = False
    depends_on_repository = False
    depends_on_worker = False
    depends_on_rest = False
    depends_on_uow = False

    for root, _, files in os.walk(module_path):
        for file in files:
            if file.endswith(".py"):
                file_path = os.path.join(root, file)

                if has_import_from(file_path, "internal.domain"):
                    depends_on_domain = True

                if has_import_from(file_path, "internal.usecase"):
                    depends_on_usecase = True

                if has_import_from(file_path, "internal.dto"):
                    depends_on_dto = True

                if has_import_from(file_path, "internal.infrastructure"):
                    depends_on_infrastructure = True

                if has_import_from(file_path, "internal.repository"):
                    depends_on_repository = True

                if has_import_from(file_path, "internal.worker"):
                    depends_on_worker = True

                if has_import_from(file_path, "internal.rest"):
                    depends_on_rest = True

                if has_import_from(file_path, "internal.uow"):
                    depends_on_uow = True

    return {
        "depends_on_domain": depends_on_domain,
        "depends_on_usecase": depends_on_usecase,
        "depends_on_dto": depends_on_dto,
        "depends_on_infrastructure": depends_on_infrastructure,
        "depends_on_repository": depends_on_repository,
        "depends_on_worker": depends_on_worker,
        "depends_on_rest": depends_on_rest,
        "depends_on_uow": depends_on_uow,
    }


def test_domain_is_independent():
    domain_path = "internal/domain"
    domain = check_dependencies(domain_path)

    assert not domain["depends_on_usecase"]
    assert not domain["depends_on_dto"]
    assert not domain["depends_on_infrastructure"]
    assert not domain["depends_on_repository"]
    assert not domain["depends_on_worker"]
    assert not domain["depends_on_rest"]
    assert not domain["depends_on_uow"]


def test_usecase_dependencies():
    usecase_path = "internal/usecase"
    usecase = check_dependencies(usecase_path)

    assert usecase["depends_on_domain"]
    assert usecase["depends_on_dto"]
    assert usecase["depends_on_uow"]
    assert not usecase["depends_on_infrastructure"]
    assert not usecase["depends_on_repository"]
    assert not usecase["depends_on_worker"]
    assert not usecase["depends_on_rest"]


def test_infrastructure_dependencies():
    infrastructure_path = "internal/infrastructure"
    infrastructure = check_dependencies(infrastructure_path)

    assert infrastructure["depends_on_domain"]
    assert infrastructure["depends_on_usecase"]
    assert infrastructure["depends_on_dto"]
    assert not infrastructure["depends_on_rest"]


def test_data_storage_dependencies():
    data_storage_path = "internal/infrastructure/data_storage"
    data_storage = check_dependencies(data_storage_path)

    assert data_storage["depends_on_dto"]
    assert not data_storage["depends_on_repository"]
    assert not data_storage["depends_on_uow"]
    assert not data_storage["depends_on_rest"]


def test_repository_dependencies():
    repository_path = "internal/repository"
    repository = check_dependencies(repository_path)

    assert repository["depends_on_dto"]
    assert repository["depends_on_infrastructure"]
    assert not repository["depends_on_uow"]
    assert not repository["depends_on_worker"]
    assert not repository["depends_on_rest"]


def test_worker_dependencies():
    worker_path = "internal/worker"
    worker = check_dependencies(worker_path)

    assert worker["depends_on_dto"]
    assert worker["depends_on_infrastructure"]
    assert not worker["depends_on_uow"]
    assert not worker["depends_on_repository"]
    assert not worker["depends_on_rest"]


def test_dto_dependencies():
    dto_path = "internal/dto"
    dto = check_dependencies(dto_path)

    assert dto["depends_on_domain"]
    assert not dto["depends_on_usecase"]
    assert not dto["depends_on_infrastructure"]
    assert not dto["depends_on_worker"]
    assert not dto["depends_on_uow"]
    assert not dto["depends_on_repository"]
    assert not dto["depends_on_rest"]
