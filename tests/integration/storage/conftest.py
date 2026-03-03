from typing import Callable

import pytest

from .helpers import make_file as make_file_helper


@pytest.fixture
def make_file() -> Callable[..., object]:
    """Factory for File-protocol compatible objects."""
    return make_file_helper
