import pytest
from pytest_mock import MockerFixture

from internal.dto.repository.file import File
from internal.usecase.file import CheckContentType
from internal.usecase.file.exception import IncorrectFileFormatException


@pytest.fixture
def check_content_type() -> CheckContentType:
    return CheckContentType()


@pytest.mark.parametrize(
    "content_type, expected_exception",
    [
        ("text/csv", None),
        ("application/json", IncorrectFileFormatException),
        ("", IncorrectFileFormatException),
    ],
)
def test_check_content_type(
    check_content_type: CheckContentType,
    mocker: MockerFixture,
    content_type: str,
    expected_exception: IncorrectFileFormatException | None,
):
    upload_file = mocker.Mock(spec=File)
    upload_file.content_type = content_type

    if expected_exception:
        with pytest.raises(expected_exception):
            check_content_type(upload_file=upload_file)
    else:
        check_content_type(upload_file=upload_file)
