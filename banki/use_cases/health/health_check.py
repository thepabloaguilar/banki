from typing import Protocol

from pydantic import BaseModel


class DbGateway(Protocol):
    def is_health(self) -> bool:
        ...  # noqa: WPS428


class HealthCheckInput(BaseModel):
    ...  # noqa: WPS428, WPS604


class HealthCheckOutput(BaseModel):
    health: bool


class HealthCheckUseCase:
    _db: DbGateway

    def __init__(self, db: DbGateway) -> None:
        self._db = db

    def __call__(self, inp: HealthCheckInput) -> HealthCheckOutput:
        return HealthCheckOutput(
            health=self._db.is_health(),
        )
