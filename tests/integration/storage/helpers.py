"""Helper functions for storage integration tests."""

from io import BytesIO
from uuid import uuid4

from .constants import (
    DEFAULT_FILE_CONTENT,
    DEFAULT_FILE_CONTENT_TYPE,
    DEFAULT_FILE_NAME,
    TEST_PATH_PREFIX,
)


def make_file(
    *,
    name: str = DEFAULT_FILE_NAME,
    content: bytes = DEFAULT_FILE_CONTENT,
    content_type: str = DEFAULT_FILE_CONTENT_TYPE,
) -> object:
    """Create a File-protocol compatible object for testing."""
    data = BytesIO(content)
    return type(
        "File",
        (),
        {
            "name": name,
            "data": data,
            "size": len(content),
            "content_type": content_type,
        },
    )()


def make_test_path(filename: str = "file.csv") -> str:
    """Create a unique test path to avoid conflicts between tests."""
    return f"{TEST_PATH_PREFIX}/{uuid4().hex}/{filename}"
