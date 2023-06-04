import csv
from io import StringIO
from typing import Any

import pytest
from fastapi import status
from fastapi.testclient import TestClient


@pytest.mark.integration()
def test_create_debts(client_app: TestClient) -> None:
    expected_status = status.HTTP_201_CREATED
    data = [
        {
            'name': 'John Doe',
            'governmentId': '1111111111',
            'email': 'johndoe@test.com',
            'debtAmount': 1000000,
            'debtDueDate': '2022-10-12',
            'debtId': 8291,
        },
    ]
    rep = client_app.post(
        '/api/v1/debts',
        headers={
            'Content-Type': 'text/csv',
        },
        data=_dict_to_csv(data),  # type: ignore[arg-type]
    )

    assert rep.status_code == expected_status


def _dict_to_csv(items: list[dict[str, Any]]) -> str:
    in_memory_file = StringIO()
    fieldnames = list(items[0].keys()) if items else []

    writer = csv.DictWriter(in_memory_file, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(items)

    return in_memory_file.getvalue()
