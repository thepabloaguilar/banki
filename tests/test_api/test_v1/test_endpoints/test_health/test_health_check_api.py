import pytest
from fastapi.testclient import TestClient
from starlette import status


@pytest.mark.integration()
def test_health_check(client_app: TestClient) -> None:
    expected_value = {'health': True}
    expected_status = status.HTTP_200_OK

    response = client_app.get('/api/v1/health/check')

    assert response.status_code == expected_status
    assert response.json() == expected_value
