from unittest.mock import AsyncMock

import pytest

from turtled_backend.repository.example import ExampleRepository
from turtled_backend.schema.example import Example
from turtled_backend.service.example import ExampleService


@pytest.fixture
def mock_repo():
    example_repository = AsyncMock(spec=ExampleRepository)

    return {
        "example": example_repository
    }


@pytest.fixture
def example_service(mock_repo: dict):
    return ExampleService(
        mock_repo["example"]
    )


@pytest.fixture
def example_fixture():
    yield Example(
        id=1,
        name="test"
    )
