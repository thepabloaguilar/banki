from pathlib import Path

import pytest
from fastapi import status
from fastapi.testclient import TestClient

_DATA_FOLDER = Path(__file__).parent.joinpath('data')


@pytest.mark.integration()
def test_create_debts(client_app: TestClient) -> None:
    expected_status = status.HTTP_201_CREATED

    with open(_DATA_FOLDER.joinpath('example.csv'), 'rb') as csv_file:
        rep = client_app.post(
            '/api/v1/debts/file',
            files={
                'file': ('example.csv', csv_file, 'text/csv'),
            },
        )

    assert rep.status_code == expected_status
