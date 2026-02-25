from unittest.mock import MagicMock

import pytest
from fastapi import Request


@pytest.fixture
def request_mock() -> MagicMock:
    return MagicMock(spec=Request)
