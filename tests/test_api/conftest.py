import pytest
from fastapi.testclient import TestClient

from banki.main import app


@pytest.fixture(scope='session')
def client_app() -> TestClient:
    return TestClient(app)
