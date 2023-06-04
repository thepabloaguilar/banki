from unittest.mock import Mock

import pytest

from banki.use_cases.health.health_check import (
    DbGateway,
    HealthCheckInput,
    HealthCheckOutput,
    HealthCheckUseCase,
)


@pytest.mark.parametrize('is_health', [True, False])
def test_health_check(is_health: bool) -> None:
    db = Mock(spec=DbGateway)
    uc = HealthCheckUseCase(db=db)
    inp = HealthCheckInput()
    expected_value = HealthCheckOutput(health=is_health)

    db.is_health.return_value = is_health

    assert uc(inp) == expected_value
