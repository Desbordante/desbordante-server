from typing import Type

import pytest
from pytest_mock import MockerFixture

from src.exceptions import IncorrectFileFormatException
from src.schemas.dataset_schemas import File
from src.usecases.dataset.check_content_type import CheckContentTypeUseCase


@pytest.fixture
def check_content_type() -> CheckContentTypeUseCase:
    return CheckContentTypeUseCase()


@pytest.mark.parametrize(
    "content_type, expected_exception",
    [
        ("text/csv", None),
        ("application/json", IncorrectFileFormatException),
        ("", IncorrectFileFormatException),
    ],
)
def test_check_content_type(
    check_content_type: CheckContentTypeUseCase,
    mocker: MockerFixture,
    content_type: str,
    expected_exception: Type[IncorrectFileFormatException] | None,
):
    upload_file = mocker.Mock(spec=File)
    upload_file.content_type = content_type

    if expected_exception:
        with pytest.raises(expected_exception):
            check_content_type(file=upload_file)
    else:
        check_content_type(file=upload_file)
