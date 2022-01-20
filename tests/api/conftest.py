from typing import Generator

import pytest
from fastapi.testclient import TestClient
from app import application
from tests.api.test_base import TestHelper


@pytest.fixture(scope="session")
def test_helper() -> Generator:
    base_url = 'http://127.0.0.1:8080'
    client = TestClient(application)
    test_helper = TestHelper(client=client, base_url=base_url)
    yield test_helper
